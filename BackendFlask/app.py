from datetime import datetime, timezone, timedelta
from flask import Flask, request, abort
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object("application.config.Config")
api = Api(app)
cors = CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

from application import init_db, tasks, workers
from application.models import User, Service, ServiceRequest, Review

celery = workers.celery
celery.Task = workers.ContextTask
app.app_context().push()


def role_required(role):
    def decorator(func):
        @jwt_required()
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_role = get_jwt()["role"]
            if current_role != role:
                return {"message": f"You are not supposed to be there {current_role}", "role": current_role}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


class RegisterCustomer(Resource):
    def post(self):
        data = request.json
        user = db.session.scalars(select(User).filter_by(username=data["username"])).first()
        if user:
            return {"message": "User already exists!"}, 401
        if not user:
            pwhash = generate_password_hash(data["password"])
            new_user = User(username=data["username"], password_hashed=pwhash, role="customer", status="verified", email=data["email"],
                            fullname=data["fullname"], address=data["address"], pincode=int(data["pincode"]), contact_number=int(data["contact_number"]))
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Registration successful! Please log in."}, 200


class RegisterProfessional(Resource):
    def post(self):
        data = request.json
        user = db.session.scalars(select(User).filter_by(username=data["username"])).first()
        if user:
            return {"message": "User already exists!"}, 401
        if not user:
            pwhash = generate_password_hash(data["password"])
            new_user = User(username=data["username"], password_hashed=pwhash, role="professional", status="pending",
                            email=data["email"], fullname=data["fullname"], service_type=int(data["service_type"]),
                            experience=int(data["experience"]), address=data["address"], pincode=int(data["pincode"]),
                            contact_number=int(data["contact_number"]))
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Registration successful! Please wait for admin verification."}, 200


class Login(Resource):
    def post(self):
        data = request.json
        user = db.session.scalars(select(User).filter_by(username=data["username"])).first()

        if not user:
            return {"message": "Incorrect username or password"}, 401

        if not check_password_hash(user.password_hashed, data["password"]):
            return {"message": "Incorrect password"}, 403

        if user:
            if check_password_hash(user.password_hashed, data["password"]):
                if user.role == "admin":
                    access_token = create_access_token(identity=str(user.id),
                                                       additional_claims={"username": user.username, "role": user.role})
                    return {"token": access_token, "role": user.role, "message": "Logged in Successfully"}, 200

                elif user.role == "customer":
                    if user.status != "blocked":
                        access_token = create_access_token(identity=str(user.id),
                                                           additional_claims={"username": user.username, "role": user.role})
                        return {"token": access_token, "role": user.role, "message": "Logged in Successfully"}, 200
                    elif user.status == "blocked":
                        return {"message": "You are not authorised to login!"}, 403

                elif user.role == "professional":
                    if user.status == "verified":
                        access_token = create_access_token(identity=str(user.id),
                                                           additional_claims={"username": user.username, "role": user.role})
                        return {"token": access_token, "role": user.role, "message": "Logged in Successfully"}, 200
                    elif user.status == "pending":
                        return {"message": "Profile is under verification, Please try later!"}, 403
                    elif user.status == "blocked":
                        return {"message": "You are not authorised to login!"}, 403


class ServicesList(Resource):
    def get(self):
        services = db.session.scalars(select(Service).order_by(Service.name.asc())).all()
        services_json = []
        for service in services:
            services_json.append({"id": service.id, "name": service.name})
        return {"services": services_json}, 200


class ProfileDetails(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt()["username"]
        user = db.session.scalars(select(User).filter_by(username=username)).first()
        details = {
            "username": user.username,
            "email": user.email,
            "fullname": user.fullname,
            "role": user.role,
            "service_name": user.provider.name if user.role == "professional" else None,
            "experience": user.experience if user.role == "professional" else None,
            "address": user.address,
            "pincode": user.pincode,
            "contact_number": user.contact_number,
            "created_at": user.created_at.isoformat()
        }
        return {"details": details}, 200


class EditProfile(Resource):
    @jwt_required()
    def put(self, username):
        data = request.json
        user = db.session.scalars(select(User).filter_by(username=username)).first()
        if user.role == "professional":
            user.experience = data["experience"]
        user.email = data["email"]
        user.fullname = data["fullname"]
        user.address = data["address"]
        user.pincode = data["pincode"]
        user.contact_number = data["contact_number"]
        db.session.commit()
        return {"message": "Profile edited successfully!"}, 200


# ---------------------------------------------- ADMIN --------------------------------------------


class AdminHome(Resource):
    @role_required("admin")
    def get(self):
        services = db.session.scalars(select(Service).order_by(Service.name.asc())).all()
        services_json = []
        for service in services:
            services_json.append({
                "id": service.id,
                "name": service.name,
                "price": str(service.price),
                "time_required": service.time_required,
                "description": service.description,
                "created_at": service.created_at.isoformat()
            })
        professionals = db.session.scalars(select(User).filter_by(role="professional").order_by(User.fullname.asc())).all()
        avg_ratings = dict(db.session.execute(select(Review.professional_id, func.avg(Review.rating)).group_by(Review.professional_id)).all())
        professionals_json = []
        for professional in professionals:
            professionals_json.append({
                "id": professional.id,
                "username": professional.username,
                "email": professional.email,
                "fullname": professional.fullname,
                "role": professional.role,
                "service_name": professional.provider.name,
                "rating": avg_ratings[professional.id] if professional.id in avg_ratings.keys() else 0,
                "status": professional.status,
                "experience": professional.experience,
                "address": professional.address,
                "pincode": professional.pincode,
                "contact_number": professional.contact_number,
                "created_at": professional.created_at.isoformat()
            })
        customers = db.session.scalars(select(User).filter_by(role="customer").order_by(User.fullname.asc())).all()
        customers_json = []
        for customer in customers:
            customers_json.append({
                "id": customer.id,
                "username": customer.username,
                "email": customer.email,
                "fullname": customer.fullname,
                "role": customer.role,
                "status": customer.status,
                "address": customer.address,
                "pincode": customer.pincode,
                "contact_number": customer.contact_number,
                "created_at": customer.created_at.isoformat()
            })
        service_history = db.session.scalars(select(ServiceRequest).order_by(ServiceRequest.time_of_request.desc())).all()
        service_history_json = []
        for service_request in service_history:
            service_history_json.append({
                "id": service_request.id,
                "service": service_request.service.name,
                "customer": service_request.customer.fullname,
                "professional": service_request.professional.fullname,
                "time_of_request": service_request.time_of_request.isoformat(),
                "time_of_completion": service_request.time_of_completion.isoformat() if service_request.time_of_completion else None,
                "task": service_request.task,
                "service_status": service_request.service_status
            })
        return {"services": services_json, "professionals": professionals_json, "customers": customers_json, "service_history": service_history_json}, 200


class ModifyService(Resource):
    service_parser = reqparse.RequestParser()
    service_parser.add_argument("name", required=True, type=str, help="Name of the service cannot be blank!")
    service_parser.add_argument("price", required=True, type=float, help="Price of the service cannot be blank!")
    service_parser.add_argument("time_required", required=True, type=int, help="Time required for the service cannot be blank!")
    service_parser.add_argument("description", required=True, type=str, help="Description of the service cannot be blank!")

    @role_required("admin")
    def post(self):
        data = self.service_parser.parse_args()
        new_service = Service(
            name=data["name"],
            price=data["price"],
            time_required=data["time_required"],
            description=data["description"]
        )
        db.session.add(new_service)
        db.session.commit()
        return {"message": "Service added successfully!"}, 201

    @role_required("admin")
    def put(self, service_id):
        data = self.service_parser.parse_args()
        service = db.session.scalars(select(Service).filter_by(id=service_id)).first()
        if service is None:
            abort(404)
        service.name = data["name"]
        service.price = data["price"]
        service.time_required = data["time_required"]
        service.description = data["description"]
        db.session.commit()
        return {"message": "Service updated successfully!"}, 200

    @role_required("admin")
    def delete(self, service_id):
        service = db.session.scalars(select(Service).filter_by(id=service_id)).first()
        if service is None:
            abort(404)
        db.session.delete(service)
        db.session.commit()
        return {"message": "Service and all associated data have been deleted successfully."}, 200


class ModifyUser(Resource):
    @role_required("admin")
    def put(self, user_id):
        user = db.session.scalars(select(User).filter_by(id=user_id)).first()
        if user is None:
            abort(404)
        if user.status == "verified":
            abort(403, "User is already approved!")
        user.status = "verified"
        db.session.commit()
        return {"message": "User approved successfully!"}, 200

    @role_required("admin")
    def patch(self, user_id):
        user = db.session.scalars(select(User).filter_by(id=user_id)).first()
        if user is None:
            abort(404)
        if user.status == "blocked":
            abort(403, "User is already blocked!")
        user.status = "blocked"
        db.session.commit()
        return {"message": "User blocked successfully!"}, 200

    @role_required("admin")
    def delete(self, user_id):
        user = db.session.scalars(select(User).filter_by(id=user_id)).first()
        if user is None:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully!"}, 200


class AdminSearch(Resource):
    @role_required("admin")
    def get(self, search_by, search_text):
        service_history_json, customers_json, professionals_json = [], [], []
        if search_by == "service_request":
            service_history = db.session.scalars(select(ServiceRequest)
                                                 .options(selectinload(ServiceRequest.customer),
                                                          selectinload(ServiceRequest.professional),
                                                          selectinload(ServiceRequest.service))
                                                 .where(
                                                     or_(ServiceRequest.service_status.ilike(f"%{search_text}%"),
                                                         ServiceRequest.task.ilike(f"%{search_text}%"),
                                                         ServiceRequest.customer.has(User.username.ilike(f"%{search_text}%")),
                                                         ServiceRequest.customer.has(User.fullname.ilike(f"%{search_text}%")),
                                                         ServiceRequest.professional.has(User.username.ilike(f"%{search_text}%")),
                                                         ServiceRequest.professional.has(User.fullname.ilike(f"%{search_text}%")),
                                                         ServiceRequest.service.has(Service.name.ilike(f"%{search_text}%"))))
                                                 .order_by(ServiceRequest.time_of_request.desc())).all()
            if not service_history:
                return {"message": "No Service Request found!"}, 404
            for service_request in service_history:
                service_history_json.append({
                    "id": service_request.id,
                    "service": service_request.service.name,
                    "customer": service_request.customer.fullname,
                    "professional": service_request.professional.fullname,
                    "time_of_request": service_request.time_of_request.isoformat(),
                    "time_of_completion": service_request.time_of_completion.isoformat() if service_request.time_of_completion else None,
                    "task": service_request.task,
                    "service_status": service_request.service_status
                })
        elif search_by == "customer":
            customers = db.session.scalars(select(User)
                                           .where(User.role == "customer",
                                                  or_(User.username.ilike(f"%{search_text}%"),
                                                      User.fullname.ilike(f"%{search_text}%")
                                                      ))).all()
            if not customers:
                return {"message": "No Customer found!"}, 404
            for customer in customers:
                customers_json.append({
                    "id": customer.id,
                    "username": customer.username,
                    "email": customer.email,
                    "fullname": customer.fullname,
                    "role": customer.role,
                    "status": customer.status,
                    "address": customer.address,
                    "pincode": customer.pincode,
                    "contact_number": customer.contact_number,
                    "created_at": customer.created_at.isoformat()
                })
        elif search_by == "professional":
            professionals = db.session.scalars(select(User)
                                               .options(selectinload(User.provider))
                                               .where(User.role == "professional",
                                                      or_(User.username.ilike(f"%{search_text}%"),
                                                          User.email.ilike(f"%{search_text}%"),
                                                          User.fullname.ilike(f"%{search_text}%"),
                                                          User.address.ilike(f"%{search_text}%"),
                                                          User.pincode.ilike(f"%{search_text}%"),
                                                          User.contact_number.ilike(f"%{search_text}%"),
                                                          User.status.ilike(f"%{search_text}%"),
                                                          User.provider.has(Service.name.ilike(f"%{search_text}%"))
                                                          ))).all()
            if not professionals:
                return {"message": "No Service Professional found!"}, 404
            avg_ratings = dict(db.session.execute(select(Review.professional_id, func.avg(Review.rating)).group_by(Review.professional_id)).all())
            for professional in professionals:
                professionals_json.append({
                    "id": professional.id,
                    "username": professional.username,
                    "email": professional.email,
                    "fullname": professional.fullname,
                    "role": professional.role,
                    "service_name": professional.provider.name,
                    "rating": avg_ratings[professional.id] if professional.id in avg_ratings.keys() else 0,
                    "status": professional.status,
                    "experience": professional.experience,
                    "address": professional.address,
                    "pincode": professional.pincode,
                    "contact_number": professional.contact_number,
                    "created_at": professional.created_at.isoformat()
                })
        return {"service_history": service_history_json, "customers": customers_json, "professionals": professionals_json}, 200


# ---------------------------------------------- CUSTOMER --------------------------------------------


class CustomerHome(Resource):
    @role_required("customer")
    def get(self):
        jwt_claims = get_jwt()
        current_user = {"id": jwt_claims["sub"], "username": jwt_claims["username"], "role": jwt_claims["role"]}
        services = db.session.scalars(select(Service).order_by(Service.name.asc())).all()
        services_json = []
        for service in services:
            services_json.append({
                "id": service.id,
                "name": service.name,
                "price": str(service.price),
                "time_required": service.time_required,
                "description": service.description
            })
        service_history = db.session.scalars(select(ServiceRequest)
                                             .filter(ServiceRequest.customer_id == int(jwt_claims["sub"]))
                                             .order_by(ServiceRequest.time_of_request.desc())
                                             ).all()
        service_history_json = []
        for service_request in service_history:
            service_history_json.append({
                "id": service_request.id,
                "service": service_request.service.name,
                "professional": service_request.professional.fullname,
                "time_of_request": service_request.time_of_request.isoformat(),
                "time_of_completion": service_request.time_of_completion.isoformat() if service_request.time_of_completion else None,
                "task": service_request.task,
                "service_status": service_request.service_status
            })
        return {"current_user": current_user, "services": services_json, "service_history": service_history_json}, 200


class SelectProfessional(Resource):
    @role_required("customer")
    def get(self, service_id):
        professionals = db.session.scalars(select(User)
                                           .filter_by(role="professional", status="verified", service_type=service_id)
                                           .order_by(User.fullname.asc())).all()
        avg_ratings = dict(db.session.execute(select(Review.professional_id, func.avg(Review.rating)).group_by(Review.professional_id)).all())
        professionals_json = []
        for professional in professionals:
            professionals_json.append({
                "id": professional.id,
                "username": professional.username,
                "fullname": professional.fullname,
                "service_name": professional.provider.name,
                "rating": avg_ratings[professional.id] if professional.id in avg_ratings.keys() else 0,
                "experience": professional.experience,
                "address": professional.address,
                "pincode": professional.pincode,
                "contact_number": professional.contact_number
            })
        return professionals_json, 200


class ManageServiceRequest(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument("time_of_request", required=True, type=str, help="Time of request for the service cannot be blank!")
    request_parser.add_argument("task", required=True, type=str, help="Task of the request cannot be blank!")

    @role_required("customer")
    def post(self, service_id, professional_id):
        data = self.request_parser.parse_args()
        time_of_request = datetime.fromisoformat(data["time_of_request"]).replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
        new_entry = ServiceRequest(service_id=service_id, professional_id=professional_id, customer_id=int(get_jwt()["sub"]),
                                   service_status="requested", time_of_request=time_of_request, task=data["task"])
        db.session.add(new_entry)
        db.session.commit()
        return {"message": "Service booked successfully!"}, 201

    @role_required("customer")
    def put(self, request_id):
        data = self.request_parser.parse_args()
        history_entry = db.session.scalars(select(ServiceRequest).filter_by(id=request_id)).first()
        if history_entry is None:
            abort(404)
        if history_entry.service_status != "requested":
            abort(403, "Service isn't in requested state, can't be edited!")
        time_of_request = datetime.fromisoformat(data["time_of_request"]).replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
        history_entry.time_of_request = time_of_request
        history_entry.task = data["task"]
        db.session.commit()
        return {"message": "Service edited successfully!"}, 200

    @role_required("customer")
    def patch(self, request_id):
        history_entry = db.session.scalars(select(ServiceRequest).filter_by(id=request_id)).first()
        if history_entry is None:
            abort(404)
        if history_entry.service_status == "rejected":
            abort(403, "Service is already rejected by professional")
        if history_entry.service_status == "closed":
            abort(403, "Service is already closed")
        history_entry.time_of_completion = datetime.now(timezone(timedelta(hours=5, minutes=30)))
        history_entry.service_status = "closed"
        db.session.commit()
        return {"message": "Service closed successfully!"}, 200


class ServiceRemarks(Resource):
    remark_parser = reqparse.RequestParser()
    remark_parser.add_argument("rating", required=True, type=str, help="Rating cannot be blank!")
    remark_parser.add_argument("remarks", type=str)

    @role_required("customer")
    def put(self, request_id):
        data = self.remark_parser.parse_args()
        history_entry = db.session.scalars(select(ServiceRequest).filter_by(id=request_id)).first()
        if history_entry is None:
            abort(404)
        new_remark = Review(service_request_id=request_id, professional_id=history_entry.professional_id,
                            customer_id=history_entry.customer_id, rating=data["rating"], remarks=data["remarks"])
        history_entry.time_of_completion = datetime.now(timezone(timedelta(hours=5, minutes=30)))
        db.session.add(new_remark)
        db.session.commit()
        return {"message": "Remarks submitted successfully!"}, 201


class CustomerSearch(Resource):
    @role_required("customer")
    def get(self, search_by, search_text):
        jwt_claims = get_jwt()
        service_history_json, professionals_json  = [], []
        if search_by == "service_request":
            service_history = db.session.scalars(select(ServiceRequest)
                                                 .options(selectinload(ServiceRequest.professional), selectinload(ServiceRequest.service))
                                                 .where(ServiceRequest.customer_id == int(jwt_claims["sub"]),
                                                     or_(ServiceRequest.service_status.ilike(f"%{search_text}%"),
                                                         ServiceRequest.task.ilike(f"%{search_text}%"),
                                                         ServiceRequest.professional.has(User.username.ilike(f"%{search_text}%")),
                                                         ServiceRequest.professional.has(User.fullname.ilike(f"%{search_text}%")),
                                                         ServiceRequest.professional.has(User.address.ilike(f"%{search_text}%")),
                                                         ServiceRequest.professional.has(User.pincode.ilike(f"%{search_text}%")),
                                                         ServiceRequest.service.has(Service.name.ilike(f"%{search_text}%"))))
                                                 .order_by(ServiceRequest.time_of_request.desc())).all()
            if not service_history:
                return {"message": "No Service Request found!"}, 404
            for service_request in service_history:
                service_history_json.append({
                    "id": service_request.id,
                    "service": service_request.service.name,
                    "professional": service_request.professional.fullname,
                    "time_of_request": service_request.time_of_request.isoformat(),
                    "time_of_completion": service_request.time_of_completion.isoformat() if service_request.time_of_completion else None,
                    "task": service_request.task,
                    "service_status": service_request.service_status
                })
        elif search_by == "professional":
            professionals = db.session.scalars(select(User)
                                               .options(selectinload(User.provider))
                                               .where(User.role == "professional",
                                                      User.status == "verified",
                                                      or_(User.username.ilike(f"%{search_text}%"),
                                                          User.fullname.ilike(f"%{search_text}%"),
                                                          User.address.ilike(f"%{search_text}%"),
                                                          User.pincode.ilike(f"%{search_text}%"),
                                                          User.contact_number.ilike(f"%{search_text}%"),
                                                          User.provider.has(Service.name.ilike(f"%{search_text}%"))
                                                          ))).all()
            if not professionals:
                return {"message": "No Service Professional found!"}, 404
            avg_ratings = dict(db.session.execute(select(Review.professional_id, func.avg(Review.rating)).group_by(Review.professional_id)).all())
            for professional in professionals:
                professionals_json.append({
                    "id": professional.id,
                    "username": professional.username,
                    "fullname": professional.fullname,
                    "service_id": professional.provider.id,
                    "service_name": professional.provider.name,
                    "rating": avg_ratings[professional.id] if professional.id in avg_ratings.keys() else 0,
                    "experience": professional.experience,
                    "address": professional.address,
                    "pincode": professional.pincode,
                    "contact_number": professional.contact_number
                })
        return {"service_history": service_history_json, "professionals": professionals_json}, 200


# ---------------------------------------------- PROFESSIONAL --------------------------------------------


class ProfessionalHome(Resource):
    @role_required("professional")
    def get(self):
        jwt_claims = get_jwt()
        current_user = {"id": jwt_claims["sub"], "username": jwt_claims["username"], "role": jwt_claims["role"]}
        pending_services = db.session.scalars(select(ServiceRequest)
                                            .filter(ServiceRequest.professional_id == jwt_claims["sub"], ServiceRequest.service_status == "requested")
                                            .order_by(ServiceRequest.time_of_request.desc())).all()
        pending_services_json = []
        for service_request in pending_services:
            pending_services_json.append({
                "id": service_request.id,
                "customer": service_request.customer.fullname,
                "address": service_request.customer.address,
                "pincode": service_request.customer.pincode,
                "contact_number": service_request.customer.contact_number,
                "time_of_request": service_request.time_of_request.isoformat(),
                "time_of_completion": service_request.time_of_completion.isoformat() if service_request.time_of_completion else None,
                "task": service_request.task,
                "service_status": service_request.service_status
            })
        ongoing_services = db.session.scalars(select(ServiceRequest)
                                              .filter(ServiceRequest.professional_id == jwt_claims["sub"], ServiceRequest.service_status == "accepted")
                                              .order_by(ServiceRequest.time_of_request.desc())).all()
        ongoing_services_json = []
        for service_request in ongoing_services:
            ongoing_services_json.append({
                "id": service_request.id,
                "customer": service_request.customer.fullname,
                "address": service_request.customer.address,
                "pincode": service_request.customer.pincode,
                "contact_number": service_request.customer.contact_number,
                "time_of_request": service_request.time_of_request.isoformat(),
                "time_of_completion": service_request.time_of_completion.isoformat() if service_request.time_of_completion else None,
                "task": service_request.task,
                "service_status": service_request.service_status
            })
        closed_services = db.session.scalars(select(ServiceRequest)
                                             .filter(ServiceRequest.professional_id == jwt_claims["sub"],
                                                     or_(ServiceRequest.service_status == "rejected", ServiceRequest.service_status == "closed"))
                                             .order_by(ServiceRequest.time_of_request.desc())).all()
        closed_services_json = []
        for service_request in closed_services:
            closed_services_json.append({
                "id": service_request.id,
                "customer": service_request.customer.fullname,
                "address": service_request.customer.address,
                "pincode": service_request.customer.pincode,
                "contact_number": service_request.customer.contact_number,
                "time_of_request": service_request.time_of_request.isoformat(),
                "time_of_completion": service_request.time_of_completion.isoformat() if service_request.time_of_completion else None,
                "task": service_request.task,
                "service_status": service_request.service_status
            })
        services_json = {
            "pending_services": pending_services_json,
            "ongoing_services": ongoing_services_json,
            "closed_services": closed_services_json
        }
        return {"current_user": current_user, "services": services_json}, 200


class ServiceAction(Resource):
    @role_required("professional")
    def get(self, request_id):
        service_request = db.session.scalars(select(ServiceRequest).filter_by(id=request_id)).first()
        if service_request is None:
            abort(404)
        if service_request.service_status != "requested":
            abort(403, "Service request is not in a pending state.")
        service_request.service_status = "accepted"
        db.session.commit()
        return {"message": "Request accepted successfully."}, 200

    @role_required("professional")
    def patch(self, request_id):
        service_request = db.session.scalars(select(ServiceRequest).filter_by(id=request_id)).first()
        if service_request is None:
            abort(404)
        if service_request.service_status != "requested":
            abort(403, "Service request is not in a pending state.")
        service_request.service_status = "rejected"
        db.session.commit()
        return {"message": "Request rejected successfully."}, 200


class ProfessionalSearch(Resource):
    @role_required("professional")
    def get(self, search_by, search_text):
        jwt_claims = get_jwt()
        service_history_json = []
        if search_by == "service_request":
            service_history = db.session.scalars(select(ServiceRequest)
                                                 .options(selectinload(ServiceRequest.customer))
                                                 .where(ServiceRequest.professional_id == int(jwt_claims["sub"]),
                                                        or_(ServiceRequest.service_status.ilike(f"%{search_text}%"),
                                                            ServiceRequest.task.ilike(f"%{search_text}%"),
                                                            ServiceRequest.customer.has(User.username.ilike(f"%{search_text}%")),
                                                            ServiceRequest.customer.has(User.fullname.ilike(f"%{search_text}%")),
                                                            ServiceRequest.customer.has(User.address.ilike(f"%{search_text}%")),
                                                            ServiceRequest.customer.has(User.pincode.ilike(f"%{search_text}%"))))
                                                 .order_by(ServiceRequest.time_of_request.desc())).all()
            if not service_history:
                return {"message": "No Results found!"}, 404
            for service_request in service_history:
                service_history_json.append({
                    "id": service_request.id,
                    "customer": service_request.customer.fullname,
                    "address": service_request.customer.address,
                    "pincode": service_request.customer.pincode,
                    "contact_number": service_request.customer.contact_number,
                    "time_of_request": service_request.time_of_request.isoformat(),
                    "task": service_request.task,
                    "service_status": service_request.service_status
                })
        return {"service_history": service_history_json}, 200


api.add_resource(RegisterCustomer, "/api/register/customer")
api.add_resource(RegisterProfessional, "/api/register/professional")
api.add_resource(Login, "/api/login")
api.add_resource(ServicesList, "/api/services")
api.add_resource(ProfileDetails, "/api/profile")
api.add_resource(EditProfile, "/api/profile/edit/<string:username>")
api.add_resource(AdminHome, "/api/admin")
api.add_resource(ModifyService, "/api/service/add", "/api/service/<int:service_id>/edit", "/api/service/<int:service_id>/delete")
api.add_resource(ModifyUser, "/api/user/<int:user_id>/approve", "/api/user/<int:user_id>/block", "/api/user/<int:user_id>/delete")
api.add_resource(AdminSearch, "/api/admin/search/<string:search_by>/<string:search_text>")
api.add_resource(CustomerHome, "/api/customer")
api.add_resource(SelectProfessional, "/api/<int:service_id>/select_professional")
api.add_resource(ManageServiceRequest, "/api/book/<int:service_id>/<int:professional_id>", "/api/edit/<int:request_id>", "/api/close/<int:request_id>")
api.add_resource(ServiceRemarks, "/api/review/<int:request_id>")
api.add_resource(CustomerSearch, "/api/customer/search/<string:search_by>/<string:search_text>")
api.add_resource(ProfessionalHome, "/api/professional")
api.add_resource(ServiceAction, "/api/service_request/<int:request_id>/accept", "/api/service_request/<int:request_id>/reject")
api.add_resource(ProfessionalSearch, "/api/professional/search/<string:search_by>/<string:search_text>")


if __name__ == "__main__":
    app.run()
