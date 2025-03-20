from app import app, db
from application.models import User, Service
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        pwhashed = generate_password_hash("adminIIT")
        admin = User(username="admin", password_hashed=pwhashed, email="admin@email.com", role="admin",
                     status="verified", fullname="admin", address="admin", pincode=999999, contact_number=9999999999)
        db.session.add(admin)
        db.session.commit()

    if not Service.query.first():
        services = [
            Service(name="Appliance Repair Technician", price=1000, time_required=90,
                    description="Fast, reliable repairs for all your home appliances—keeping your household running smoothly."),
            Service(name="Carpenter", price=1200, time_required=600,
                    description="Expert craftsmanship for custom woodwork, furniture, and home improvements."),
            Service(name="Cleaner", price=500, time_required=50,
                    description="Thorough cleaning services for a spotless home or office—every corner shines, every time!"),
            Service(name="Electrician", price=2000, time_required=120,
                    description="Safe, efficient electrical solutions for your home or business—installations, repairs, and troubleshooting."),
            Service(name="Gardener", price=1000, time_required=190,
                    description="Transform your outdoor space with expert gardening and landscaping services—vibrant, healthy gardens year-round."),
            Service(name="Laundry Service", price=100, time_required=30,
                    description="Hassle-free laundry service—clean, fresh, and folded, right to your door!"),
            Service(name="Pest Control Specialist", price=660, time_required=90,
                    description="Effective pest control that keeps your home safe from unwanted invaders—peace of mind guaranteed."),
            Service(name="Plumber", price=550, time_required=50,
                    description="Quick, reliable plumbing services—fixing leaks, clogs, and installations with no mess or stress!")
        ]
        db.session.add_all(services)
        db.session.commit()
