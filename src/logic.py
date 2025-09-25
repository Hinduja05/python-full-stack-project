#src/logic.py
from src.db import DatabaseManager



class TaskManager:
    """
    Acts as a bridge between frontend (streamlit?FastAPI) nad database
    """
    def __init__(self):
        #Create a database manager instanve(this will handles actual db operations)
        self.db=DatabaseManager()

# ----Create----
    def add_task(self,name,hours_studied,attendance,sleep_hours,prediction=None,created_at=None):
        """
        Add a new task to the database
        Return the sucess message if the task is added
        """
        if not name or not hours_studied:
            return{"Sucees":False,"message":"Name and hours studied required"}
        #Call DB method to insert task
        result=self.db.create_studentcreate_student(name, hours_studied, attendance, sleep_hours, prediction=None, created_at=None)
        
        if result.get("Success"):
            return{"Sucess":True,"message":"Record added successfully" }
        else:
            return{"Sucess":False,"message":f"Error:{result.get('error')}"}
        #---Read--
    def get_task(self):
        """
        Get all the task from the database
        """
        return self.db.get_all_students()
    #---update---
    def mark_complete(self,student_id):
        
        """
        Mark a task as completed
        """
        result=self.db.update_student(student_id)
        if result.get("Success"):
            return{"Succes":True,"message":"marked as completed"}
        return{"Success":False,"message":"Task markes as pending"}
    #----Delete--
    def delete_student(self,student_id):

        """
        Delete the task from database
        """
        result=self.db.delete_student(student_id)
        if result.get("Success"):
            return {"success": True, "message": "Record deleted successfully"}
        return {"success": False, "message": f"Error: {result.get('error')}"}
#-----------------------
#Student user table
#------------------
class UserManager:
    """


    """
    def __init__(self):
        self.db=DatabaseManager()
    #create
    def add_user(self,username, password, role="student"):
        if not username or not password:
            return{"Success":False,"message":"Username and password required"}
        result=self.db.create_user(username, password, role="student")
        return{"Success":True,"message":"Username and password added succesfully"}if result.get("Success")\
            else {"Success":False,"message":f"Error:{result.get('error')}"}
    #Read
    def get_all_user(self):
        return self.db.get_all_users()
    #update
    def update_users(self,user_id, updated_fields: dict) :
        result=self.db.update_user(user_id,updated_fields)
        if result.get("Success"):
            return{"Succes":True,"message":"Updated"}
        return{"Success":False,"message":f"Error:{result.get('error')}"}
    #----Delete--
    def delete_users(self,user_id):
        result=self.db.delete_user(user_id)
        if result.get("Success"):
            return {"success": True, "message": "Record deleted successfully"}
        return {"success": False, "message": f"Error: {result.get('error')}"}
#--------------
#performance table
#----------------


