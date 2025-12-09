# Leave Management System (Django)

A complete **Leave Management System** built with **Django** and **Tailwind CSS**, designed to handle employee leave workflows in a real-world organization.

This project supports multiple roles (Employee, Manager, HR, CEO), leave validation, quota management, approval workflows, email notifications, and reporting.

---

## ✨ Features Overview

### 👤 Employee

* Submit leave requests (full day / half day)
* Upload supporting documents (medical certificate, etc.)
* Automatic validation:

  * Cannot select past dates
  * Cannot select invalid date ranges
  * Cannot overlap existing leave
  * Cannot exceed leave quota
* View personal leave history
* Cancel pending leave requests
* Reset password via email

### 👔 Manager

* View pending leave requests from direct subordinates
* Approve / reject leave requests
* Add approval comments
* Automatic quota deduction upon approval
* View approval history

### 🧑‍💼 HR

* View and filter all leave requests
* Export leave data (CSV / Excel)
* Create employees manually
* Bulk import employees from Excel (.xlsx)
* Enable / disable user accounts
* Manage leave quotas per employee and year
* Manage departments and leave types

### 🧑‍💻 CEO

* Company-wide dashboard
* Yearly statistics:

  * Total employees
  * Total leave requests
  * Approved / Pending / Rejected / Cancelled
* Charts:

  * Monthly leave count
  * Leave by department
  * Leave by type

---

## 🧠 Core Business Logic (`services.py`)

### Leave Validation

* Validates date order and prevents past dates
* Prevents overlapping leave requests
* Supports half-day leave (only if allowed by leave type)
* Skips quota check for unpaid leave
* Uses working-day calculation (excluding weekends and holidays)

### Leave Approval

* Deducts quota **only when approved**
* Handles half-day leave correctly
* Ensures quota is sufficient before approval
* Records approver and comment

### Leave Balance

* Automatically creates leave balances per year
* Handles multiple leave types
* Supports cross-year initialization

### Email Notifications

* Employee receives confirmation after submitting leave
* Manager receives notification for pending approval
* Employee receives status update after approval/rejection
* Password reset handled via Django auth system

---

## 🏗 Project Structure

```
Leave-Management-System/
│
├── config/                 # Django project settings
├── leave_app/              # Main application
│   ├── models.py
│   ├── templates/          # Global auth templates
│   ├── views.py
│   ├── services.py
│   ├── forms.py
│   ├── fixtures/
│   │   └── initial_data.json
│   ├── templates/
│   │   └── leave_app/
│   └── static/
├── static/                 # Tailwind / assets
├── .env
├── manage.py
└── README.md
```

---

## ⚙️ Tech Stack

* **Backend:** Django 5
* **Frontend:** Django Templates + Tailwind CSS
* **Database:** PostgreSQL
* **Auth:** Django Authentication
* **Email:** SMTP (Gmail App Password)
* **Charts:** Chart.js

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Leave-Management-System.git
cd Leave-Management-System
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
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
python manage.py createsuperuser
```

---

## 📦 Load Initial Data (Fixtures)

Fixtures make it easy to move machines or reset environments.

### Create fixture directory

```bash
mkdir leave_app/fixtures
```

### Dump data

```bash
python manage.py dumpdata leave_app.Department leave_app.LeaveType \
  --indent 2 > leave_app/fixtures/initial_data.json
```

### Load data

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

## ✉️ Email & Password Reset

* Password reset uses Django auth URLs
* Emails are sent via SMTP
* During development, you can use console backend:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

---

## 🧪 Usage Flow

1. HR creates or imports employees
2. Leave balances are auto-created
3. Employee submits leave request
4. Manager approves / rejects
5. System deducts quota and sends email
6. HR and CEO can view reports and dashboards

---

## 🔮 Future Improvements

* Public holidays management UI
* Slack / LINE notification
* Multi-level approval
* Carry-over leave rules
* REST API + React frontend
* Docker support

---

## ✅ Project Status

✅ Core leave workflow complete
✅ Email notifications enabled
✅ Role-based access implemented
✅ Production-ready architecture

---

## 📄 License

This project is for educational and internal use.
You are free to modify and extend it.

---

## 🙌 Author

Developed by **Pathipat Mattra**
