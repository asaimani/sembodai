# செம்போடையார் வன்னியர் திருமண மையம்
## Railway Deployment Guide - படிப்படியாக வழிகாட்டி

---

## 📁 Project Structure
```
sembodai/
├── manage.py
├── requirements.txt
├── Procfile
├── .env.example
├── .gitignore
├── sembodai/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── matrimony/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── management/commands/
│       ├── load_initial_data.py
│       └── send_daily_notifications.py
└── templates/matrimony/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── candidate_list.html
    ├── candidate_form.html
    ├── candidate_detail.html
    ├── candidate_print.html
    └── shadow_list.html
```

---

## STEP 1: Local Setup

### 1.1 Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 1.2 Install Requirements
```bash
pip install -r requirements.txt
```

### 1.3 Create .env file
Copy `.env.example` to `.env` and fill in your details:
```
SECRET_KEY=your-very-secret-key-here
DEBUG=True
DB_NAME=sembodai
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 1.4 Create PostgreSQL Database (Local)
```sql
CREATE DATABASE sembodai;
```

### 1.5 Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 1.6 Load Initial Data
```bash
python manage.py load_initial_data
```

### 1.7 Create Superuser
```bash
python manage.py createsuperuser
```

### 1.8 Test Locally
```bash
python manage.py runserver
```
Open: http://localhost:8000

---

## STEP 2: Push to GitHub

### 2.1 Initialize Git
```bash
git init
git add .
git commit -m "Initial commit - Sembodai Matrimony"
```

### 2.2 Push to GitHub
```bash
git remote add origin https://github.com/yourusername/sembodai.git
git branch -M main
git push -u origin main
```

---

## STEP 3: Railway Setup

### 3.1 Go to railway.app
- Login with GitHub
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository

### 3.2 Add PostgreSQL Database
- In Railway dashboard → Click "New"
- Select "Database" → "PostgreSQL"
- Railway auto-sets DATABASE_URL variable ✅

### 3.3 Add Environment Variables
Go to your service → Variables tab → Add these:

```
SECRET_KEY          = your-secret-key-here
DEBUG               = False
ALLOWED_HOSTS       = your-app.railway.app
CSRF_TRUSTED_ORIGINS = https://your-app.railway.app
EMAIL_HOST          = smtp.gmail.com
EMAIL_PORT          = 587
EMAIL_HOST_USER     = your@gmail.com
EMAIL_HOST_PASSWORD = your-gmail-app-password
```

### 3.4 Set Custom Start Command
Go to Settings → Start Command:
```
python manage.py migrate && python manage.py load_initial_data && python manage.py collectstatic --noinput && gunicorn sembodai.wsgi:application --bind 0.0.0.0:$PORT
```

### 3.5 Generate Domain
- Settings tab → Domains → Generate Domain
- Your URL: https://your-app.railway.app

### 3.6 Create Superuser (via Railway Shell or CLI)
```bash
railway run python manage.py createsuperuser
```

---

## STEP 4: Post-Deployment

### 4.1 Access Admin Panel
```
https://your-app.railway.app/admin/
```
Login and add AdminProfile for each admin user.

### 4.2 Add Admin Profile
- Admin Panel → Admin Profiles → Add
- Add location, address, phone for each admin

### 4.3 Setup Daily Email Notifications
Add to Railway Cron Jobs or use a cron service:
```bash
python manage.py send_daily_notifications
```
Schedule: Every day at 8 PM IST (14:30 UTC)

---

## STEP 5: Gmail App Password Setup

1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Go to "App Passwords"
4. Create password for "Mail"
5. Use this 16-digit password in EMAIL_HOST_PASSWORD

---

## Features Summary

| Feature | Description |
|---------|-------------|
| 🔐 Multi-Admin Login | Multiple admins from different regions |
| 👨 Male Bio Data | Complete profile with all fields |
| 👩 Female Bio Data | Complete profile with all fields |
| 🔢 Auto UID | M000001, F000001 format |
| 🔍 Advanced Search | Age, Salary, Rasi, Nachathiram filters |
| 🖨️ Print Biodata | Single-page print format |
| 💰 Shadow Table | Unpaid candidates stored separately |
| 📧 Email Alerts | Daily new entries + expiry notifications |
| ⚠️ Dashboard Alerts | Expired premium highlighted |
| 📸 3 Photos | Photo upload per candidate |
| 🌙 Tamil Font | Noto Sans Tamil throughout |

---

## Future Updates → Auto Deploy
```bash
git add .
git commit -m "update message"
git push
```
Railway auto-deploys! ✅
