# Coderr

**Coderr** is a freelance marketplace platform connecting business users with customers for service offerings. Built with Django and Django REST Framework, it provides a comprehensive API for managing user profiles, service offers, orders, and reviews.

> ⚠️ A frontend is required for full project usage — placeholder for future GitHub repo.

---

## 📋 Project Overview

Coderr enables:
- **Business Users** to create and manage service packages with tiered pricing (Basic, Standard, Premium)
- **Customers** to browse offers, place orders, and leave reviews
- **Admins** to oversee all platform activities through the Django admin panel

### Key Features
- 🔐 User authentication with token-based API
- 👥 Dual user types: Business & Customer profiles
- 📦 Service packages with multiple offer tiers
- 🛒 Order management system with status tracking
- ⭐ Review and rating system (1-5 stars)
- 🔍 Advanced filtering and search capabilities
- 📄 Pagination with customizable page sizes

---

## 🚀 Setup Option 1 — using `uv` (uv Toolchain)

This option uses **uv** to manage your virtual environment and run your Django app.

### 🛠️ Prerequisites

Make sure **uv** is installed and available in your shell.

### 📦 Install Dependencies
```bash
uv sync
```

This will install all dependencies into the managed `.venv`.

### 📁 Activate Environment
```bash
source .venv/bin/activate     # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 🔐 Environment Configuration

Create your environment file from the template:
```bash
cp .env.template .env
```

Generate a new Django secret key at [https://djecrety.ir/](https://djecrety.ir/) and add it to your `.env` file:
```
SECRET_KEY=your-generated-secret-key-here
```

### 🗄️ Database Setup

The database is not included in this repository. You need to create it from scratch:
```bash
# Create the database and apply all migrations
uv run python manage.py migrate
```

This will create a fresh `db.sqlite3` file with all necessary tables.

### 👤 Create a Superuser (Admin)

To access the Django admin panel:
```bash
uv run python manage.py createsuperuser
```

Follow the prompts and enter a username, email, and password.

### ▶️ Run the Development Server
```bash
uv run python manage.py runserver
```

Visit the admin panel:
```
http://127.0.0.1:8000/admin/
```

Your backend API will be available at:
```
http://127.0.0.1:8000/api/
```

---

## 🐍 Setup Option 2 — using Python + .venv

This option uses a standard Python virtual environment.

### 📍 Create & Activate the Virtual Environment
```bash
python -m venv .venv
```

Activate it:
```bash
source .venv/bin/activate     # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 📥 Install Requirements
```bash
pip install -r requirements.txt
```

### 🔐 Environment Configuration

Create your environment file from the template:
```bash
cp .env.template .env
```

Generate a new Django secret key at [https://djecrety.ir/](https://djecrety.ir/) and add it to your `.env` file:
```
SECRET_KEY=your-generated-secret-key-here
```

### 🗄️ Database Setup

The database is not included in this repository. You need to create it from scratch:
```bash
# Create the database and apply all migrations
python manage.py migrate
```

This will create a fresh `db.sqlite3` file with all necessary tables.

### 👤 Create a Superuser (Admin)

To access the Django admin panel:
```bash
python manage.py createsuperuser
```

Follow the prompts and enter a username, email, and password.

### ▶️ Run the Development Server
```bash
python manage.py runserver
```

Visit the admin panel:
```
http://127.0.0.1:8000/admin/
```

Your backend API will be available at:
```
http://127.0.0.1:8000/api/
```

---

## 👥 User Types & Permissions

### Customer Users
- Browse and search offers
- Create orders
- Write reviews (one per business user)
- View their own orders

### Business Users
- Create and manage offer packages
- Each package must have exactly 3 offers (Basic, Standard, Premium)
- Update order status
- Receive reviews
- View order statistics

### Admin/Staff
- Full access to all models via admin panel
- Can delete offers and orders
- Bulk actions for order status updates
- Review statistics and analytics

---

## 🎨 Admin Panel Features

Access at `http://127.0.0.1:8000/admin/` after creating a superuser.

### User Profiles
- Filter by user type, location, creation date
- Search by username, email, phone number
- Organized fieldsets for easy editing

### Offer Packages
- Inline editing of all 3 offers
- Automatic calculation of min price and delivery time
- Filter by date and business user
- Search by title and description

### Orders
- Filter by status, offer type, dates
- Bulk status updates (Complete, Cancel, In Progress)
- Search by customer/business username
- Detailed order information display

### Reviews
- Filter by rating and business user
- Calculate average ratings
- Search by username and content
- Truncated description in list view

---

## 🔒 Security & Validation

### Authentication
- Token-based authentication using Django REST Framework's TokenAuthentication
- Passwords securely hashed with Django's default hasher

### Permissions
- Role-based access control (Business, Customer, Admin)
- Object-level permissions for offer ownership
- Protected endpoints require authentication

### Data Validation
- Email and username uniqueness enforced
- Offer packages must have exactly 3 offers (Basic, Standard, Premium)
- Reviews limited to one per customer per business user
- Ratings validated between 1-5 stars
- Price and delivery time constraints

---

## 📝 Data Models

### UserProfile
- Extends Django User model
- Types: Customer or Business
- Fields: location, phone, description, profile picture, working hours

### OfferPackage
- Groups 3 related offers
- Belongs to a business user
- Fields: title, description, image, timestamps

### Offer
- Part of an OfferPackage
- Types: Basic, Standard, Premium
- Fields: title, price, delivery time, revisions, features

### Order
- Links customer and business users
- Statuses: in_progress, cancelled, completed
- Copies offer details at time of order

### Review
- One review per customer per business user
- Rating: 1-5 stars
- Fields: rating, description, timestamps

---

## 🧪 Testing

The project includes comprehensive test utilities:

### Test Factories
```python
from test_utils import TestDataFactory

# Create authenticated client with user
client, user = TestDataFactory.create_authenticated_client()

# Authenticate existing user
client = TestDataFactory.authenticate_user(user)
```

### Test Data Setup
```python
from test_utils import APITestCaseWithSetup

class MyTestCase(APITestCaseWithSetup):
    # Automatically provides:
    # - 2 business users with profiles and offer packages
    # - 2 customer users with profiles
    # - 6 offers (3 web dev, 3 design)
    # - 4 orders with different statuses
    # - 3 reviews with different ratings
```

---

## 📌 Notes

### 🔐 Environment Variables
- The `.env` file contains sensitive configuration like your `SECRET_KEY`.
- **Never commit your `.env` file** to version control — it should be in your `.gitignore`.
- Use the provided `.env.template` as a reference for required variables.

### 🗄️ Database
- The database file (`db.sqlite3`) is **not** included in this repository.
- You must run `python manage.py migrate` after setup to create a fresh database.
- Make sure `db.sqlite3` is in your `.gitignore` to avoid committing it.

### 🧠 Frontend
- This project requires a frontend to fully interact with the API.
- A frontend application (separate repository) will be created later.
- API documentation can be explored via Django REST Framework's browsable API.

### 🧹 Git Ignore
- Make sure your `.venv/`, `db.sqlite3`, and `.env` are not committed to version control — add them to your `.gitignore`.

### 📊 Media Files
- User-uploaded files (profile pictures, offer images) are stored in the media directory.
- Configure `MEDIA_ROOT` and `MEDIA_URL` in your Django settings for production.

---

## 🛠️ Development

### Running Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Running Tests
```bash
python manage.py test
```

### Creating Sample Data
Use the Django shell to create sample data:
```bash
python manage.py shell
```

Or use the admin panel to manually add test data.

---

## 📚 Quick Reference

| Step                | Command                              |
|---------------------|--------------------------------------|
| Create environment  | `uv sync` OR `python -m venv .venv` |
| Activate environment| `source .venv/bin/activate`          |
| **Configure .env**  | `cp .env.template .env`              |
| **Generate SECRET_KEY** | Visit https://djecrety.ir/       |
| **Create database** | `python manage.py migrate`           |
| Create superuser    | `python manage.py createsuperuser`   |
| Run server          | `python manage.py runserver`         |
| Run tests           | `python manage.py test`              |
| Access admin        | `http://127.0.0.1:8000/admin/`       |
| Access API          | `http://127.0.0.1:8000/api/`         |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Welcome to Coderr!** 💼✨

*Connecting talented professionals with clients who need their services.*