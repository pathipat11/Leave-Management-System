# Leave Management System

A full-featured **Leave Management System** built with **Django** for managing employee leave requests, approvals, quotas, and reporting.

This project is suitable for internal company use, academic projects, or as a portfolio demonstrating real-world backend and business logic implementation.

---

## ✨ Features

### Employee

* Submit leave requests (full day / half day)
* Automatic validation (date range, overlap, quota availability)
* View personal leave history and status
* Email notifications on request submission and approval/rejection

### Manager

* View pending leave requests from subordinates
* Approve or reject leave requests with comments
* See employee details and leave history

### HR

* Manage employees (create, edit, activate/deactivate)
* Import employees via Excel (.xlsx)
* Manage annual leave balances per employee
* View and export leave reports (CSV / Excel)

### CEO / Admin

* Dashboard summary of leave statistics
* Yearly overview, department breakdown, leave type distribution

---

## 🧰 Tech Stack

* **Backend**: Django 5
* **Database**: PostgreSQL
* **Authentication**: Django Auth
* **Frontend**: Django Templates
* **Styling**: Tailwind CSS (via CDN)
* **Email**: SMTP (Gmail App Password)
* **ORM**: Django ORM

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/leave-management-system.git
cd leave-management-system
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\\Scripts\\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=leave_mgmt
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

> ⚠️ For Gmail, you **must use an App Password**, not your normal email password.

---

## 🗄 Database Setup

```bash
python manage.py migrate
```

(Optional) Load initial data such as departments and leave types:

```bash
python manage.py loaddata leave_app/fixtures/initial_data.json
```

---

## 🚀 Run Development Server

```bash
python manage.py runserver
```

Open: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🎨 Frontend Styling (Tailwind CSS)

This project uses **Tailwind CSS** for styling the UI.

Tailwind is applied directly inside Django templates using utility classes.
No Node.js or build pipeline is required.

### Setup

Tailwind CSS is loaded via **CDN** and included in the base template.

Example (`base.html`):

```html
<script src="https://cdn.tailwindcss.com"></script>
```

This approach is lightweight and ideal for development or small-to-medium projects.

> ⚠️ Note: For large-scale production environments, a build-based Tailwind setup is recommended.

---

## 🔐 Authentication & Roles

Roles are assigned using Django Groups:

* **Employee** (default user)
* **Manager** (Group: `MANAGER`)
* **HR** (Group: `HR` or `is_staff`)
* **CEO** (Group: `CEO`)

Access control is handled via Django decorators such as:

* `@login_required`
* `@user_passes_test`

---

## 📧 Email Notifications

The system sends emails for:

* Leave request submission
* Approval / rejection results
* Password reset

Email is handled via SMTP configuration in `settings.py`.

---

## 📊 Business Logic Highlights

* Leave quota validation (including half-day logic)
* Automatic quota deduction on approval
* Cross-year and overlap checks
* Paid vs unpaid leave support

Core logic is located in:

```
leave_app/services.py
```

---

## 🧪 Development Notes

* Tailwind is CDN-based (no frontend build step)
* Suitable for demo, portfolio, or internal tooling
* Codebase structured with separation of concerns

---

## 📄 License

This project is for educational and demonstration purposes.
You may adapt it freely for your own use.

---

## 🙌 Author

Developed by **Pathipat Mattra**
