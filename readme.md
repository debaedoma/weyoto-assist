# Weyoto Assist

**Weyoto Assist** is an AI-powered assistant designed to help small businesses manage customer inquiries quickly, professionally, and effortlessly. It provides a 24/7 smart support agent that leverages your business's unique details to respond accurately to customer questions — no complex setup or extra staffing needed.

## 🌟 Executive Summary

Weyoto Assist enables business owners to enter and manage essential business details like services, pricing, and policies. Powered by OpenAI GPT models, it uses this information to automatically answer customer questions in real time — making support stress-free and scalable.

### Key Goals:

* ✅ Maximize user adoption
* ♻ Drive customer retention
* 💸 Remain cost-effective and profitable

Whether you're a solo entrepreneur or a growing business, Weyoto Assist simplifies engagement, boosts professionalism, and saves time by automating repetitive interactions.

---

## 🏠 Technical Overview

### 🔧 Architecture

* **Backend:** Flask
* **Database:** SQLAlchemy with support for relational databases
* **Modules:** Modular Blueprints for `business` and `inquiries` APIs

### 📁 Project Structure

```
weyoto-assist/
├── app.py                  # Main entrypoint with app and route setup
├── config.py               # Environment-based configuration
├── extensions.py           # SQLAlchemy initialization
├── models/                 # ORM models (Business, Inquiries)
├── modules/                # API logic split into blueprints
├── requirements.txt        # Python package dependencies
```

### 🧠 Core Models

* **Business** with multiple **Descriptions**
* **Inquiry** with name, email, and message fields

---

## 🥺 API Endpoints

### `/business`

* `POST /add`: Add a new business and description.
* `POST /add-description`: Append new descriptions to an existing business.
* `PUT /update/<id>`: Modify a specific business description.
* `GET /`: List all businesses.
* `GET /<id>`: Fetch a specific business and its descriptions.

### `/inquiries`

* `POST /add`: Submit a customer inquiry.
* `GET /`: Retrieve all submitted inquiries.

---

## 🚀 Setup & Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variable:

   ```bash
   export WEYOTO_ASSIST_DATABASE_URL=<your-database-uri>
   ```
3. Launch the server:

   ```bash
   python app.py
   ```

Visit `http://localhost:5000/` to verify the app is running:

```
🚀 Weyoto Assist is running with Database!
```
