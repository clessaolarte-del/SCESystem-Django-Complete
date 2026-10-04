# Student Equipment and Returning Management System

A Django version of the SCESystem project for managing school equipment borrowing and returning.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Load sample data:
   ```bash
   python manage.py seed_data
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Open:
   ```text
   http://localhost:8000
   ```

## Default accounts

- Student: `student` / `student123`
- Staff/Admin: `admin` / `admin123`
