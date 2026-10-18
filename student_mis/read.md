# Student Management Information System (Student MIS)

A web-based Student Management Information System built with Django and Bootstrap. It lets staff manage students, courses, attendance and marks from one place.

## Features

- Staff login and logout
- Dashboard with counts of students, courses and departments
- Students: list with search, add, view details, edit, delete
- Courses: list, add, edit, delete
- Attendance: choose a course and date, mark Present or Absent for the department's students
- Marks: add, edit, delete and list marks per student, course and exam type
- Student detail page showing marks and attendance percentage
- Departments managed through the Django admin

## Tech Stack

- Python 3
- Django
- SQLite
- Bootstrap 5 (CDN)

## Project Structure

    student_mis_project/
        manage.py
        student_mis/    (project settings and URLs)
        core/           (models, views, forms, templates)

## How to Run (Windows)

1. Clone the repository

       git clone https://github.com/YOUR-USERNAME/student-mis.git
       cd student-mis

2. Create and activate a virtual environment

       python -m venv venv
       venv\Scripts\activate

3. Install dependencies

       pip install -r requirements.txt

4. Set up the database

       python manage.py makemigrations core
       python manage.py migrate

5. Create an admin user

       python manage.py createsuperuser

6. Start the server

       python manage.py runserver

7. Open http://127.0.0.1:8000/admin/ to add a Department, then http://127.0.0.1:8000/ to use the system.

## Limitations

- No separate teacher or student roles; every logged-in user has full access
- Intended for learning and local use, not production deployment

## Author

Vsb