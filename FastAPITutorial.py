from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# define app

app = FastAPI()

# Create a database

fakedb = []


class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None


# define route

@app.get('/message')
def read_root():
    return {"greetings": "Welcome to first fastapi app"}


@app.get("/courses")
def get_courses():
    return fakedb


@app.get("/courses/{course_id}")
def get_a_course(course_id: int):
    course = course_id - 1
    return fakedb[course]


@app.post("/courses")
def add_course(course: Course):
    fakedb.append(course.dict())
    return fakedb[-1]


@app.delete("courses/{course_id}")
def delete_course(course_id: int):
    fakedb.pop(course_id - 1)
    return {"task": "deletion successful"}
