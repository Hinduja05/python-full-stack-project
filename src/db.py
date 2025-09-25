# db_manager.py
import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ===============================
# STUDENTS TABLE
# ===============================

#  CREATE: Add new student
def create_student(name, hours_studied, attendance, sleep_hours, prediction=None, created_at=None):
    data = {
        "name": name,
        "hours_studied": hours_studied,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "prediction": prediction,
        "created_at": created_at or datetime.now()
    }
    return supabase.table("students").insert(data).execute()

#  READ: Get all students
def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

# UPDATE: Update student record (e.g., prediction or fields)
def update_student(student_id, updated_fields: dict):
    return supabase.table("students").update(updated_fields).eq("id", student_id).execute()

#  DELETE: Delete student by ID
def delete_student(student_id):
    return supabase.table("students").delete().eq("id", student_id).execute()


# ===============================
# USERS TABLE
# ===============================

#  CREATE: Add new user
def create_user(username, password, role="student"):
    data = {
        "username": username,
        "password": password,  #  should hash in real apps!
        "role": role
    }
    return supabase.table("users").insert(data).execute()

#  READ: Get all users
def get_all_users():
    response = supabase.table("users").select("*").execute()
    return response.data

#  READ: Get user by username (for login check)
def get_user_by_username(username):
    response = supabase.table("users").select("*").eq("username", username).execute()
    return response.data

#  UPDATE: Update user info
def update_user(user_id, updated_fields: dict):
    return supabase.table("users").update(updated_fields).eq("id", user_id).execute()

#  DELETE: Delete user
def delete_user(user_id):
    return supabase.table("users").delete().eq("id", user_id).execute()


# ===============================
# PERFORMANCE LOGS TABLE
# ===============================

#  CREATE: Add performance log
def create_performance_log(student_id, old_prediction, new_prediction):
    data = {
        "student_id": student_id,
        "old_prediction": old_prediction,
        "new_prediction": new_prediction
    }
    return supabase.table("performance_logs").insert(data).execute()

#  READ: Get logs for one student
def get_logs_by_student(student_id):
    response = supabase.table("performance_logs").select("*").eq("student_id", student_id).execute()
    return response.data

#  READ: Get all logs
def get_all_logs():
    response = supabase.table("performance_logs").select("*").execute()
    return response.data

def update_student(student_id, updated_fields: dict):
    # Automatically add updated_at timestamp
    updated_fields["updated_at"] = datetime.now()
    return supabase.table("students").update(updated_fields).eq("id", student_id).execute()

#  DELETE: Delete logs for a student
def delete_logs_by_student(student_id):
    return supabase.table("performance_logs").delete().eq("student_id", student_id).execute()

