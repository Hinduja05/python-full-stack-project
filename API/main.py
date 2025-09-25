from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# --------------------- Imports -----------------
# Add src folder to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Now import managers
from logic import TaskManager, UserManager, PerformanceManager

# --------------------- App setup -----------------
app = FastAPI(title="Student Performance Prediction API", version="1.0")

# ------------------ Allow frontend to access API -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ------------------ Managers -----------------
task_manager = TaskManager()
user_manager = UserManager()
performance_manager = PerformanceManager()

# ------------------ Data Models -----------------
class TaskCreate(BaseModel):
    name: str
    hours_studied: int
    attendance: int
    sleep_hours: int
    prediction: str | None = None  # prediction could be text like "Good", "Average"

class TaskUpdate(BaseModel):
    updated_fields: dict  # Example: {"prediction": "Excellent"}

class UserCreate(BaseModel):
    username: str | None = None
    password: str | None = None
    role: str = "student"

class UserUpdate(BaseModel):
    updated_fields: dict

class PerformanceCreate(BaseModel):
    student_id: int
    old_prediction: str
    new_prediction: str

class PerformanceUpdate(BaseModel):
    updated_fields: dict

# ------------------ Endpoints -----------------

# ---- Home ----
@app.get("/")
def home():
    return {"message": "Student performance prediction API is running"}

# ---- Student Endpoints ----
@app.get("/students")
def get_students():
    return task_manager.get_task()

@app.post("/students")
def create_student(task: TaskCreate):
    result = task_manager.add_task(
        task.name, task.hours_studied, task.attendance, task.sleep_hours, task.prediction
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.put("/students/{student_id}")
def update_student(student_id: int, task: TaskUpdate):
    result = task_manager.update_student(student_id, task.updated_fields)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    result = task_manager.delete_student(student_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# ---- User Endpoints ----
@app.get("/users")
def get_users():
    return user_manager.get_all_user()

@app.post("/users")
def create_user(user: UserCreate):
    result = user_manager.add_user(user.username, user.password, user.role)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    result = user_manager.update_users(user_id, user.updated_fields)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    result = user_manager.delete_users(user_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# ---- Performance Endpoints ----
@app.get("/performance")
def get_all_logs():
    return performance_manager.get_all_logs()

@app.get("/performance/{student_id}")
def get_logs_for_student(student_id: int):
    return performance_manager.get_logs_by_student(student_id)

@app.post("/performance")
def add_performance_log(log: PerformanceCreate):
    result = performance_manager.add_log_student(
        log.student_id, log.old_prediction, log.new_prediction
    )
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.put("/performance/{log_id}")
def update_performance(log_id: int, log: PerformanceUpdate):
    result = performance_manager.update_log(log_id, log.updated_fields)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.delete("/performance/student/{student_id}")
def delete_performance_logs(student_id: int):
    result = performance_manager.delete_logs_by_student(student_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# ------------------ Run -----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
