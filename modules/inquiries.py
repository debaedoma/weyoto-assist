from flask import Blueprint, request, jsonify
from extensions import db
from models.inquiries import Inquiry  # ✅ Ensure Inquiry model is imported

# ✅ Create Blueprint
inquiries_bp = Blueprint("inquiries", __name__)

# ✅ Route to Add Inquiry
@inquiries_bp.route("/add", methods=["POST"])
def add_inquiry():
    data = request.json
    if not data or not all(k in data for k in ("name", "email", "message")):
        return jsonify({"error": "Missing required fields"}), 400

    new_inquiry = Inquiry(name=data["name"], email=data["email"], message=data["message"])
    db.session.add(new_inquiry)
    db.session.commit()

    return jsonify({"message": "Inquiry added successfully!"}), 201

# ✅ Route to Fetch All Inquiries
@inquiries_bp.route("/", methods=["GET"])
def get_inquiries():
    inquiries = Inquiry.query.all()
    return jsonify([
        {"id": i.id, "name": i.name, "email": i.email, "message": i.message}
        for i in inquiries
    ]), 200
