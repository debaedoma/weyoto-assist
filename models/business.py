from extensions import db

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    descriptions = db.relationship("BusinessDescription", backref="business", lazy=True, cascade="all, delete-orphan")

class BusinessDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    description = db.Column(db.Text, nullable=False)
