from flask import Flask
from config import Config
from extensions import db  # Ensure db is correctly imported
from modules.business import business_bp  # ✅ Import business routes
from modules.inquiries import inquiries_bp  # ✅ Ensure inquiries blueprint is also included

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config.py

db.init_app(app)

# ✅ Register Blueprints (API Modules)
app.register_blueprint(business_bp, url_prefix="/business")  # Business API
app.register_blueprint(inquiries_bp, url_prefix="/inquiries")  # Inquiry API (already exists)

# ✅ Root Route for Basic Testing
@app.route("/")
def home():
    return "🚀 Weyoto Assist is running with Database!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Tables created successfully!")
    app.run(debug=True)
