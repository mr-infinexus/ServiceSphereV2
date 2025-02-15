from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
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
        user = User.query.filter_by(username=data["username"]).first()
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
        user = User.query.filter_by(username=data["username"]).first()
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
        user = User.query.filter_by(username=data["username"]).first()
        
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


class Identity(Resource):
    @jwt_required()
    def get(self):
        jwt_claims = get_jwt()
        current_user = {"id": jwt_claims["sub"], "username": jwt_claims["username"], "role": jwt_claims["role"]}
        return {"current_user": current_user}, 200


class ProfileDetails(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt()["username"]
        user = User.query.filter_by(username=username).first()
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


class ServicesList(Resource):
    def get(self):
        services = Service.query.order_by(Service.name.asc()).all()
        services_json = []
        for service in services:
            services_json.append({"id": service.id, "name": service.name})
        return {"services": services_json}, 200


class CustomerHome(Resource):
    @role_required("customer")
    def get(self):
        jwt_claims = get_jwt()
        current_user = {"id": jwt_claims["sub"], "username": jwt_claims["username"], "role": jwt_claims["role"]}
        services = Service.query.order_by(Service.name.asc()).all()
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
        service_history = ServiceRequest.query.join(Service, ServiceRequest.service_id == Service.id) \
                                        .join(User, ServiceRequest.professional_id == User.id) \
                                        .filter(ServiceRequest.customer_id == int(jwt_claims["sub"])) \
                                        .order_by(ServiceRequest.time_of_request.desc()) \
                                        .all()
        service_history_json = []
        for request in service_history:
            service_history_json.append({
                "id": request.id,
                "service_id": request.service_id,
                "professional_id": request.professional_id,
                "time_of_request": request.time_of_request.isoformat(),
                "time_of_completion": request.time_of_completion.isoformat() if request.time_of_completion else None,
                "service_status": request.service_status,
                "task": request.task or None,
                "service": {"name": request.service.name},
                "customer": {"fullname": request.customer.fullname},
                "professional": {"fullname": request.professional.fullname}
            })
        return {"current_user": current_user, "services": services_json, "service_history": service_history_json}, 200


api.add_resource(RegisterCustomer, "/api/register/customer")
api.add_resource(RegisterProfessional, "/api/register/professional")
api.add_resource(Login, "/api/login")
api.add_resource(Identity, "/api/whoami")
api.add_resource(ProfileDetails, "/api/profile")
api.add_resource(ServicesList, "/api/services")
api.add_resource(CustomerHome, "/api/customer")


if __name__ == "__main__":
    app.run()
