# ZOCO – Women's Innerwear E-Commerce Website

ZOCO is a Django-based e-commerce web application focused on women’s innerwear, built with a clean structure and scalable backend.

---

## 🚀 Features
- User authentication (login & registration)
- Product listing and product detail pages
- Shopping cart functionality
- Admin panel for managing products
- Media support for product images
- Clean static and template organization

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS
- **Database:** SQLite (development)
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```text
zoco/
├── static/
├── store/
├── zoco/ # Main Django settings module
├── db.sqlite3
├── manage.py
├── .gitignore
├── LICENSE
├── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/zoco.git
cd zoco
```

### 2. Create and activate a virtual environment
```bash
Copy code
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
Copy code
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
Copy code
python manage.py migrate
```

### 5. Run the development server
```bash
Copy code
python manage.py runserver
```

---

## 📌 Notes
Virtual environments and database files are excluded from version control

This project is under active development

---

##📄 License
This project is licensed under the MIT License.

---