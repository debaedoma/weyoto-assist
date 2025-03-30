from flask import Blueprint, request, jsonify
from extensions import db
from models.business import Business, BusinessDescription

business_bp = Blueprint("business", __name__)

# ✅ 1. Add a New Business
@business_bp.route("/add", methods=["POST"])
def add_business():
    data = request.json
    name = data.get("name")
    description_text = data.get("description")

    if not name or not description_text:
        return jsonify({"error": "Business name and description are required."}), 400

    # Check if the business already exists
    business = Business.query.filter_by(name=name).first()
    if not business:
        business = Business(name=name)
        db.session.add(business)
        db.session.commit()

    # Add the description
    description = BusinessDescription(business_id=business.id, description=description_text)
    db.session.add(description)
    db.session.commit()

    return jsonify({"message": "Business added successfully!", "business_id": business.id}), 201


# ✅ 2. Add a New Description to an Existing Business
@business_bp.route("/add-description", methods=["POST"])
def add_business_description():
    data = request.json
    business_id = data.get("business_id")
    description_text = data.get("description")

    if not business_id or not description_text:
        return jsonify({"error": "Business ID and description are required."}), 400

    # Check if the business exists
    business = Business.query.get(business_id)
    if not business:
        return jsonify({"error": "Business not found."}), 404

    # Add new description
    description = BusinessDescription(business_id=business.id, description=description_text)
    db.session.add(description)
    db.session.commit()

    return jsonify({"message": "New description added successfully!"}), 201


# ✅ 3. Edit an Existing Description
@business_bp.route("/update/<int:description_id>", methods=["PUT"])
def update_business_description(description_id):
    data = request.json
    new_description = data.get("new_description")

    if not new_description:
        return jsonify({"error": "New description is required."}), 400

    # Find the description entry
    description = BusinessDescription.query.get(description_id)
    if not description:
        return jsonify({"error": "Description not found."}), 404

    # Update the description
    description.description = new_description
    db.session.commit()

    return jsonify({"message": "Description updated successfully!"}), 200


# ✅ 4. Retrieve a Specific Business
@business_bp.route("/<int:business_id>", methods=["GET"])
def get_business(business_id):
    business = Business.query.get(business_id)
    if not business:
        return jsonify({"error": "Business not found."}), 404

    return jsonify({
        "id": business.id,
        "name": business.name,
        "descriptions": [{"id": desc.id, "description": desc.description} for desc in business.descriptions]
    })


# ✅ 5. Retrieve All Businesses
@business_bp.route("/", methods=["GET"])
def get_all_businesses():
    businesses = Business.query.all()
    return jsonify([
        {
            "id": business.id,
            "name": business.name,
            "descriptions": [{"id": desc.id, "description": desc.description} for desc in business.descriptions]
        }
        for business in businesses
    ])
