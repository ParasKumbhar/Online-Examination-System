# Online Examination System

## Introduction
The Online Examination System is a digital platform designed to simplify the examination process, allowing students to take exams from anywhere at any time. It is developed using Python, Django, CSS, HTML, and JavaScript. The system includes separate interfaces for students, professors, and administrators, ensuring a smooth and efficient exam management experience.

## Main Features
- **Auto-Submit Form**: Exams are automatically submitted when the timer runs out.
- **Focus Monitoring**: If a student's window goes out of focus five times during an exam, the professor receives an email alert.
- **Automatic Mark Calculation**: Marks are calculated automatically once the student submits the exam.
- **User Types**: The system supports two types of users - Professors and Students.
- **Control Panels**: Separate control panels for administrators and students.
- **MCQ Exams**: Students can take multiple-choice exams, view their scores, and see the correct answers.
- **Superuser Account**: Separate superuser account for account validations.

## Project Overview
![Project Overview](https://user-images.githubusercontent.com/47894634/117118618-9c1d1b00-adae-11eb-8b61-a6e87578f8da.png)

---

# Installation Guide

## Prerequisites
- **Python** (version 3.6 or higher) - (Required)
- **pip** (Python package manager) - (Required, usually comes with Python)
- **Pipenv** (virtual environment manager) - (Required)
- **Git** (for cloning the repository) - (Required if cloning from repo)

## System Requirements
- Windows, macOS, or Linux
- At least 500 MB free disk space
- Internet connection for package installation

**Note:** This guide assumes a fresh installation. If you already have the project cloned and set up, you may skip steps related to cloning, dependency installation, and database migrations if everything is already configured. Always run `python manage.py migrate` to ensure the database is up to date.

---

## Complete Step-by-Step Installation

### **Phase 1: Project Setup**

#### Step 1: Download or Clone the Repository (Required if not already done)
Open CMD/Terminal and run:
```
bash
git clone https://github.com/ParasKumbhar/Online-Examination-System-New
cd Online-Examination-System-New
```

---

#### Step 2: Verify Python Installation (Required)
Open CMD and run:
```
bash
python --version
```
Expected output: `Python 3.x.x`

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

---

#### Step 3: Verify PIP Installation (Required)
Open CMD and run:
```
bash
pip --version
```

OR

```
bash
python -m pip --version
```

Expected output: `pip x.x.x from ...`

---

#### Step 4: Install Pipenv (Required)
Open CMD and run:
```
bash
pip install pipenv
```

---

#### Step 5: Verify Pipenv Installation (Required)
Open CMD and run:
```
bash
pipenv --version
```

Expected output: `pipenv, version x.x.x`

---

#### Step 6: Set Up Python Scripts in Environment Variables (Windows Only) (Optional - may not be needed if Pipenv works without it)

**Step 6.1:** Identify your Python Scripts path by running:
```
bash
python -m site --user-site
```

**Step 6.2:** Copy the output (example: `C:\Users\paras\AppData\Roaming\Python\Python38\site-packages`)

**Step 6.3:** Add this path to your Windows Environment Variables:
- Open Environment Variables (Search "Environment Variables" in Windows Search)
- Click "Edit Environment Variables for your account"
- Click "New" and paste the path
- Click "OK" to save

---

### **Phase 2: Virtual Environment & Dependencies**

#### Step 7: Create Virtual Environment (Required)
Open VS Code Terminal and run:
```
bash
pipenv install
```

This creates a virtual environment and installs dependencies from `Pipfile`.

---

#### Step 8: Activate Pipenv Shell (Required)
Open VS Code Terminal and run:
```
bash
pipenv shell
```

**Important:** You must run this command every time you open a new terminal before working with the project.

---

#### Step 9: Install Project Requirements (Optional - Pipenv install should cover this, but run if needed)
In VS Code Terminal (with pipenv shell activated), run:
```
bash
pip install -r requirements.txt
```

This installs all necessary packages including Django, database drivers, and other dependencies.

---

### **Phase 3: Environment Configuration**

#### Step 10: Configure Email Settings (Required for email functionality)
Create a file named `.env` in the project root folder (same directory as `manage.py`).

**For Windows**, add the following content:
```
bash
# Django Settings
DEBUG=False
SECRET_KEY=django-insecure-your-generated-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (SQLite for development - not used in current settings.py)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# Email Configuration (Gmail SMTP - required for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@example.com

# Site URL for notifications (required by notifications/models.py)
SITE_URL=http://localhost:8000

# 2FA Configuration  
TWO_FACTOR_ENABLED=True
OTP_EXPIRY_TIME=600

# Redis Cache Configuration (optional - comment out if not using Redis)
REDIS_HOST=localhost  
REDIS_PORT=6379  
REDIS_DB=0
  
# Logging Configuration  
LOG_LEVEL=INFO
```


**For Linux/macOS**, create `env.sh` instead:
```
bash
export EMAIL_HOST_PASSWORD=your_email_password
export EMAIL_HOST_USER=your_email@example.com
export EMAIL_HOST=smtp.gmail.com
export DEFAULT_FROM_EMAIL=your_email@example.com
```

---

#### Step 11: Load Environment Variables (Automatic with python-dotenv - no action needed)
In VS Code Terminal, run:

**For Windows:**
```
bash
# The .env file is automatically loaded by Django's python-dotenv
# No manual loading needed - just run your Django commands
# Example: python manage.py runserver
```

**For Linux/macOS:**
```
bash
# The .env file is automatically loaded by Django's python-dotenv
# No manual loading needed - just run your Django commands
# Example: python manage.py runserver

# Alternative: If using env.sh (legacy method)
source env.sh
```

---

#### Step 12: Navigate to Project Directory (Required)
In VS Code Terminal, run:
```
bash
cd Exam
```

---

### **Phase 4: Database Setup**

#### Step 13: Run Initial Migrations (Required)
In VS Code Terminal, run:
```
bash
python manage.py migrate
```

This applies all database migrations and creates the necessary tables.

---

#### Step 14: Create New Migrations (Optional - only if models have been changed)
If you've made changes to models, generate new migrations:
```
bash
python manage.py makemigrations
```

---

#### Step 15: Apply Migrations Again (Required after Step 14 if done)
After creating new migrations, apply them:
```
bash
python manage.py migrate
```

---

#### Step 16: Collect Static Files (Optional - for production deployment)
For production deployment, collect static files:
```
bash
python manage.py collectstatic --noinput
```

---

### **Phase 5: User & Group Setup**

#### Step 17: Create Superuser Account (Required)
In VS Code Terminal, run:
```
bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- **Username**: (e.g., admin)
- **Email**: (e.g., admin@example.com)
- **Password**: (Choose a strong password)

---

#### Step 18: Run the Development Server (Required to start the application)
In VS Code Terminal, run:
```
bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

---

### **Phase 6: Post-Deployment Configuration (Required for full functionality)**

#### Step 19: Access the Application (Required)
Open a web browser and navigate to:
- **Homepage**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

Log in with your superuser credentials.

---

#### Step 20: Create User Groups (Optional - groups are auto-created on migration)
1. Go to **Admin Panel** → `http://127.0.0.1:8000/admin/`
2. Navigate to **Authentication and Authorization** → **Groups**
3. Click **Add Group** button
4. Create **Group 1**:
   - **Name**: Professor
   - **Permissions** (search and select all):
     - `questions | question_db | Can add question_db`
     - `questions | question_db | Can change question_db`
     - `questions | question_db | Can delete question_db`
     - `questions | question_db | Can view question_db`
     - `questions | question_paper | Can add question_paper`
     - `questions | question_paper | Can change question_paper`
     - `questions | question_paper | Can delete question_paper`
     - `questions | question_paper | Can view question_paper`
     - `questions | exam_model | Can add exam_model`
     - `questions | exam_model | Can change exam_model`
     - `questions | exam_model | Can delete exam_model`
     - `questions | exam_model | Can view exam_model`
     - `questions | questioncategory | Can add questioncategory`
     - `questions | questioncategory | Can change questioncategory`
     - `questions | questioncategory | Can delete questioncategory`
     - `questions | questioncategory | Can view questioncategory`
     - `questions | questiontag | Can add questiontag`
     - `questions | questiontag | Can change questiontag`
     - `questions | questiontag | Can delete questiontag`
     - `questions | questiontag | Can view questiontag`
     - `questions | questionversion | Can add questionversion`
     - `questions | questionversion | Can change questionversion`
     - `questions | questionversion | Can delete questionversion`
     - `questions | questionversion | Can view questionversion`
     - `questions | questionstatistics | Can add questionstatistics`
     - `questions | questionstatistics | Can change questionstatistics`
     - `questions | questionstatistics | Can delete questionstatistics`
     - `questions | questionstatistics | Can view questionstatistics`
     - `questions | examassignment | Can add examassignment`
     - `questions | examassignment | Can change examassignment`
     - `questions | examassignment | Can delete examassignment`
     - `questions | examassignment | Can view examassignment`
     - `questions | examfocuslog | Can add examfocuslog`
     - `questions | examfocuslog | Can change examfocuslog`
     - `questions | examfocuslog | Can delete examfocuslog`
     - `questions | examfocuslog | Can view examfocuslog`
     - `questions | examsecurityalert | Can add examsecurityalert`
     - `questions | examsecurityalert | Can change examsecurityalert`
     - `questions | examsecurityalert | Can delete examsecurityalert`
     - `questions | examsecurityalert | Can view examsecurityalert`
     - `questions | examsession | Can add examsession`
     - `questions | examsession | Can change examsession`
     - `questions | examsession | Can delete examsession`
     - `questions | examsession | Can view examsession`
     - `questions | focuslossevent | Can add focuslossevent`
     - `questions | focuslossevent | Can change focuslossevent`
     - `questions | focuslossevent | Can delete focuslossevent`
     - `questions | focuslossevent | Can view focuslossevent`
     - `faculty | facultyinfo | Can add facultyinfo`
     - `faculty | facultyinfo | Can change facultyinfo`
     - `faculty | facultyinfo | Can delete facultyinfo`
     - `faculty | facultyinfo | Can view facultyinfo`
     - `course | course | Can add course`
     - `course | course | Can change course`
     - `course | course | Can delete course`
     - `course | course | Can view course`
     - `course | session | Can add session`
     - `course | session | Can change session`
     - `course | session | Can delete session`
     - `course | session | Can view session`
     - `course | courseregistration | Can add courseregistration`
     - `course | courseregistration | Can change courseregistration`
     - `course | courseregistration | Can delete courseregistration`
     - `course | courseregistration | Can view courseregistration`
     - `course | grade | Can add grade`
     - `course | grade | Can change grade`
     - `course | grade | Can delete grade`
     - `course | grade | Can view grade`
     - `course | studentacceptance | Can add studentacceptance`
     - `course | studentacceptance | Can change studentacceptance`
     - `course | studentacceptance | Can delete studentacceptance`
     - `course | studentacceptance | Can view studentacceptance`
     - `resultprocessing | configmarks | Can add configmarks`
     - `resultprocessing | configmarks | Can change configmarks`
     - `resultprocessing | configmarks | Can delete configmarks`
     - `resultprocessing | configmarks | Can view configmarks`
     - `resultprocessing | score | Can view score`
     - `resultprocessing | student | Can view student`
     - `resultprocessing | program | Can view program`
     - `notifications | notification | Can view notification`
     - `notifications | notificationpreference | Can view notificationpreference`
   - Click **Save**

5. Create **Group 2**:
   - **Name**: Student
   - **Permissions** (search and select all):
     - `student | studentinfo | Can add studentinfo`
     - `student | studentinfo | Can change studentinfo`
     - `student | studentinfo | Can delete studentinfo`
     - `student | studentinfo | Can view studentinfo`
     - `student | stu_question | Can add stu_question`
     - `student | stu_question | Can change stu_question`
     - `student | stu_question | Can delete stu_question`
     - `student | stu_question | Can view stu_question`
     - `student | stuexam_db | Can add stuexam_db`
     - `student | stuexam_db | Can change stuexam_db`
     - `student | stuexam_db | Can delete stuexam_db`
     - `student | stuexam_db | Can view stuexam_db`
     - `student | sturesults_db | Can add sturesults_db`
     - `student | sturesults_db | Can change sturesults_db`
     - `student | sturesults_db | Can delete sturesults_db`
     - `student | sturesults_db | Can view sturesults_db`
     - `student | focusevent | Can add focusevent`
     - `student | focusevent | Can change focusevent`
     - `student | focusevent | Can delete focusevent`
     - `student | focusevent | Can view focusevent`
     - `questions | question_db | Can view question_db`
     - `questions | question_paper | Can view question_paper`
     - `questions | exam_model | Can view exam_model`
     - `questions | questioncategory | Can view questioncategory`
     - `questions | questiontag | Can view questiontag`
     - `questions | questionversion | Can view questionversion`
     - `questions | questionstatistics | Can view questionstatistics`
     - `questions | examassignment | Can view examassignment`
     - `questions | examsession | Can view examsession`
     - `course | course | Can view course`
     - `course | session | Can view session`
     - `course | courseregistration | Can view courseregistration`
     - `course | grade | Can view grade`
     - `course | studentacceptance | Can view studentacceptance`
     - `resultprocessing | score | Can view score`
     - `studentPreferences | studentpreferencemodel | Can add studentpreferencemodel`
     - `studentPreferences | studentpreferencemodel | Can change studentpreferencemodel`
     - `studentPreferences | studentpreferencemodel | Can delete studentpreferencemodel`
     - `studentPreferences | studentpreferencemodel | Can view studentpreferencemodel`
     - `notifications | notificationpreference | Can add notificationpreference`
     - `notifications | notificationpreference | Can change notificationpreference`
     - `notifications | notificationpreference | Can view notificationpreference`
     - `notifications | notification | Can view notification`
     - `tuition | studentwallet | Can add studentwallet`
     - `tuition | studentwallet | Can change studentwallet`
     - `tuition | studentwallet | Can view studentwallet`
     - `tuition | librarybook | Can view librarybook`
     - `tuition | studentinvolvement | Can view studentinvolvement`
     - `tuition | resultapproval | Can view resultapproval`
   - Click **Save**

---

#### Step 21: Manage User Groups (Required)
1. Go to **Admin Panel** → **Users**
2. Select a user to edit
3. In the **Groups** section, select the appropriate group:
   - Select **Professor** for faculty members
   - Select **Students** for student users
4. Click **Save**

---

#### Step 22: Verify Email Configuration (Optional - for testing email functionality)
To test if email is working:
1. Go to **Admin Panel**
2. Perform an action that triggers an email (e.g., student focus loss alert)
3. Check if the email is received

If emails are not being sent, verify your `.env` file settings and ensure you've enabled "Less secure apps" in your Gmail settings (if using Gmail).

---

## Troubleshooting

### Issue: Pipenv shell not activating
**Solution**: Make sure pipenv is installed and added to PATH. Run `pip install --user pipenv`

### Issue: Port 8000 already in use
**Solution**: Run server on a different port:
```
bash
python manage.py runserver 8001
```

### Issue: Database migration errors
**Solution**: Delete `db.sqlite3` and run migrations again:
```
bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Run:
```
bash
python manage.py collectstatic --noinput
```

### Issue: Email not being sent
**Solution**: 
- Verify `.env` variables are correct
- For Gmail, enable "Less secure apps" in account settings
- Check email logs in Django admin

---

## Project Structure
```
Online-Examination-System/
├── Exam/                          # Main Django project
│   ├── manage.py                  # Django management script
│   ├── db.sqlite3                 # SQLite database
│   ├── admission/                 # Admission management app
│   ├── api/                       # API endpoints app
│   ├── core/                      # Core functionality and middleware
│   ├── course/                    # Course management app
│   ├── faculty/                   # Faculty management app
│   ├── notifications/             # Notification system
│   ├── questions/                 # Question paper management app
│   ├── resultprocessing/          # Result processing app
│   ├── student/                   # Student management app
│   ├── studentPreferences/        # Student preferences app
│   ├── tuition/                   # Tuition and financial management app
│   ├── examProject/               # Django configuration
│   │   ├── static/                # Static files for examProject
│   ├── templates/                 # HTML templates
│   ├── static/                    # Static files (CSS, JS, images)
│   ├── logs/                      # Application log files
│   ├── management/                # Custom management commands
│   ├── scripts/                   # Utility scripts
│   ├── final_status_report.py     # Final status report script
│   └── verify_groups.py           # Group verification script
├── requirements.txt               # Python dependencies
├── Pipfile                        # Pipenv dependencies
└── README.md                      # This file
```

---

## Accessing Different Sections

- **Homepage**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **Student Portal**: `http://127.0.0.1:8000/student/`
- **Faculty Portal**: `http://127.0.0.1:8000/faculty/`

---

## Support & Documentation

For more information, visit the [GitHub Repository](https://github.com/ParasKumbhar/Online-Examination-System)

---

## License
This project is open source and available under the MIT License.
