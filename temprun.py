from app import db, app
from models.inquiries import Inquiry

with app.app_context():
    # ✅ Insert a test inquiry
    new_inquiry = Inquiry(name="Alice", email="alice@example.com", message="Hello, I need help!")
    db.session.add(new_inquiry)
    db.session.commit()

    # ✅ Retrieve all inquiries
    inquiries = Inquiry.query.all()
    print([{"name": i.name, "email": i.email, "message": i.message} for i in inquiries])
