from flask import Flask, request, abort
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy import select, func
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object("application.config.Config")
api = Api(app)
cors = CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

import application.init_db
from application.models import User, Service, ServiceRequest, Review


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
            new_user = User(username=data["username"], password_hashed=pwhash, role="customer", status="verified",
                            fullname=data["fullname"], address=data["address"], pincode=int(data["pincode"]),
                            contact_number=int(data["contact_number"]))
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
                            fullname=data["fullname"], service_type=int(data["service_type"]),
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
            "fullname": user.fullname,
            "role": user.role,
            "address": user.address,
            "pincode": user.pincode,
            "contact_number": user.contact_number,
            "created_at": user.created_at.isoformat()
        }
        return {"details": details}, 200


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
        return {"services": services_json, "professionals": professionals_json, "service_history": service_history_json}, 200


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
        service = db.session.get(Service, service_id)
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
        service = db.session.get(Service, service_id)
        if service is None:
            abort(404)
        db.session.delete(service)
        db.session.commit()
        return {"message": "Service and all associated data have been deleted successfully."}, 200


class ModifyUser(Resource):
    @role_required("admin")
    def put(self, user_id):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)
        if user.status == "verified":
            return {"message": "User is already approved!"}, 403
        user.status = "verified"
        db.session.commit()
        return {"message": "User approved successfully!"}, 200

    @role_required("admin")
    def patch(self, user_id):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)
        if user.status == "blocked":
            return {"message": "User is already blocked!"}, 403
        user.status = "blocked"
        db.session.commit()
        return {"message": "User blocked successfully!"}, 200

    @role_required("admin")
    def delete(self, user_id):
        user = db.session.get(User, user_id)
        if user is None:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully!"}, 200


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


api.add_resource(RegisterCustomer, "/api/register/customer")
api.add_resource(RegisterProfessional, "/api/register/professional")
api.add_resource(Login, "/api/login")
api.add_resource(ServicesList, "/api/services")
api.add_resource(ProfileDetails, "/api/profile")
api.add_resource(AdminHome, "/api/admin")
api.add_resource(ModifyService, "/api/service/add", "/api/service/<int:service_id>/edit", "/api/service/<int:service_id>/delete")
api.add_resource(ModifyUser, "/api/user/<int:user_id>/approve", "/api/user/<int:user_id>/block", "/api/user/<int:user_id>/delete")
api.add_resource(CustomerHome, "/api/customer")


if __name__ == "__main__":
    app.run()
