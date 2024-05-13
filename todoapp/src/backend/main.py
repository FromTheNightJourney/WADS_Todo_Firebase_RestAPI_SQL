from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import uvicorn

app = FastAPI()

# CORS middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# connect mysql db
def create_server_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
        return connection
    except Error as err:
        print(f"Error: '{err}'")

# connect to db
connection = create_server_connection("127.0.0.1", "root", "fallendown0", "todolist")

# pydantic
class Task(BaseModel):
    user_id: str
    title: str
    isCompleted: bool

# function for CREATE
@app.post("/tasks/")
def create_task(task: Task):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (title, user_id) VALUES (%s, %s)", (task.title, task.user_id))
    new_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    return {"id": new_id, "title": task.title, "user_id": task.user_id}

# function for READ
@app.get("/tasks/{user_id}")
def read_tasks(user_id: str):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, isCompleted FROM tasks WHERE user_id = %s", (user_id,))
        result = cursor.fetchall()
        cursor.close()
        tasks = [{"id": task[0], "title": task[1], "isCompleted": task[2]} for task in result]
        print("Fetched tasks:", tasks)  
        return tasks
    except Exception as e:
        print("There was an error in fetching your tasks:", str(e))
        return []

# function for UPDATE
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    cursor = connection.cursor()
    cursor.execute("SELECT title, isCompleted FROM tasks WHERE id = %s AND user_id = %s", (task_id, task.user_id))
    current_task = cursor.fetchone()

    if current_task:
        current_title, current_is_completed = current_task
        new_is_completed = 1 if current_is_completed == 0 else 0
        cursor.execute("UPDATE tasks SET title = %s, isCompleted = %s WHERE id = %s AND user_id = %s", 
                       (task.title, new_is_completed, task_id, task.user_id))
        connection.commit()
        cursor.close()
        return {"message": "The task has been updated."}
    else:
        raise HTTPException(status_code=404, detail="Task not found")

# function for DELETE
@app.delete("/tasks/{task_id}/{user_id}")
def delete_task(task_id: int, user_id: str):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    connection.commit()
    cursor.close()
    return {"message": "The task has been deleted."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5173)
