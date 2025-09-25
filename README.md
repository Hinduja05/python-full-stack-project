🎓 Student Performance Predictor
The Student Performance Predictor is a Python-based project designed to evaluate and classify student performance levels using simple rule-based logic. It predicts whether a student will Fail, Average, Good, or Excellent based on three key factors:
Hours studied per day
Attendance percentage
Average sleep hours per day
This project demonstrates a complete full stack application using python, supabase,streamlit,FastAPI.
## project Features
✨ Project Features – Student Performance Predictor
1.Student Data Entry:Add student details (name, hours studied, attendance, sleep hours).
Stores data securely in Supabase database.

2.Rule-Based Prediction Logic:Calculates a performance score using Core Python conditionals.
Predicts result as Fail / Average / Good / Excellent.

3.Database Integration (Supabase):All student records stored in a cloud PostgreSQL database.
Predictions automatically updated back into the database.

4.Menu-Driven CLI Application:Simple console interface with options:
Add Student
Run Predictions
Exit
5.Bulk Predictions:Runs predictions for all students at once.
Updates results for each student in Supabase.

6.Real-Time ResultsDisplays student names with predicted performance in the console.
Teacher/administrator can check updated results inside Supabase dashboard.

## project structure

student performance predictor/
|---src/ # core logic application
|   |---logic.py #business logic and task
operations
|   |_db.py #Database Operations
|
|----api/     #Backend API
|    |_main.py/    #FastAPI endpoints
|
|----frontend/  #frontend application
|    |_app.py #streamlit web interface
|
|----requirements.txt  #python Dependencies
|
|----REABME.md  #project Documentation
|
|----.env #python variables

## quick start
### prerequisites
-python 3.8 or higher 
-A supabase account
-Git (push,cloning)

### 1.Clone or Dowmload the Project
# option 1: Clone with Git
git clone<repository-url>

# option 2:Download or Extract ZIP file

### Install Dependencies
pip install -r requirements.txt

### Setup Supabase Database

1.Create a supabase project
2.Create Task table

-Go the SQL Editor in supabase dashboard
-Run this SQL command
```sql
create table if not exists students (
    id serial primary key,
    name text not null,
    hours_studied int not null,
    attendance int not null,
    sleep_hours int not null,
    prediction text,
    created_at timestamp default now()
);
create table if not exists users (
    id serial primary key,
    username text unique not null,
    password text not null,
    role text check (role in ('teacher', 'student')) not null
);
create table if not exists performance_logs (
    id serial primary key,
    student_id int references students(id) on delete cascade,
    old_prediction text,
    new_prediction text,
    updated_at timestamp default now()
);
```
3.Get your credentials
### 4.Configure Environment Variables
1.create a ".env" file in the project root
2.Add your supabase credentials to ".env":
SUPABASE_URL="https://ywwfucxfidvgiscbzzkc.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl3d2Z1Y3hmaWR2Z2lzY2J6emtjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODEzOTEsImV4cCI6MjA3MzY1NzM5MX0.Fwd8o0k2ggCiZGUSXMF6FRjC6YVn0diLj1pg3RulTYI"
### 5.Run the Application
## Streamlit Frontend
streamlit run frontend/app.py
the app will open in your browser at `http://localhost:8501`

## FastAPI Backend
cd api
python main.py
The API will be available at `http://localhost:8000`

## How to use
## Technical Details
- **Frontend** :Streamlit (python web framework)
- **Backend**: FastAPI (Python rest API freamework)
- **Database**:Supabase(PostgreSQL-backend-as- a service)
-**Language**:Python 3.8+
## Key Components
1.**`src/db.py`**:Database operations
-Handle all the CRUD operationswith supabase
2.**`src/logic.py`**:Business logic
-Task validation and processing
## Trouble Shooting
## Common Issues
1.**Module not found errors**
-Make sure you've installed all dependencies:`pip install -r requirements.txt`
-check that you're running commands from the correct directory
## Future Enhancements
Ideas for extending this Project:
**Web Interface** (Flask / FastAPI + HTML/CSS/JS or React)
Replace CLI with a user-friendly web dashboard.
Teachers can log in, add students, and view predictions.

Student Portal:
Students log in to check their own performance predictions.
Can show graphs of study hours, attendance, and progress.

**📊 Advanced Analytics & Visualization**

Data Visualization (Matplotlib / Plotly):
Show bar graphs or pie charts of predicted categories.
Track performance trends over time.

Export Reports:
Generate PDF / Excel reports of predictions.
Useful for teachers and administrators.

**🤖 Smarter Predictions**

Machine Learning Upgrade:
Train a model using scikit-learn / TensorFlow with real datasets.
Predict student marks or grade categories instead of rule-based scoring.

Personalized Suggestions:
After predicting performance, give study recommendations.
Example: “Increase study hours by 1h/day to reach ‘Good’ category”.

**☁️ Database & Integration**

Authentication & Roles:
Use Supabase Auth → Teacher vs. Student login.

Cloud Deployment:
Deploy on Render / Vercel / Heroku for public access.
Supabase already works as the backend database.

**📱 Bonus Add-Ons**

Mobile App (React Native / Flutter):
Access predictions on mobile.
Push notifications for low attendance or poor performance.

Gamification:
Reward system for students maintaining "Good" or "Excellent".
Leaderboards for motivation.


## support 
If you encounter any issues or have questions:
**Email support**:hinduja@654gmail.com

