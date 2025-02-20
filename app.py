from flask import Flask
from config import Config
from extensions import db
from modules.inquiries import inquiries_bp  # ✅ Import the inquiries blueprint

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ✅ Register Blueprint for Inquiries
app.register_blueprint(inquiries_bp, url_prefix="/inquiries")

@app.route("/")
def home():
    return "🚀 Weyoto Assist is running with Database!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Tables created successfully!")
    app.run(debug=True)
