from fastapi import FastAPI, Path, HTTPException, Query, Body
import json

app = FastAPI()

def load_data():
    with open('student.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('student.json','w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return "I have a plan"

@app.get("/about")
def about():
    return "What about you"

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/view/{student_id}")
def view_student_id_by(student_id : str = Path(..., description = 'Student id of the student', example = 'S001')):

    data = load_data()
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code = 404, detail = "Student not found")

@app.get("/sort")
def view_sorted_student(sorted_by: str = Query(...,description="Sort by age, class, roll, marks"), order : str = Query('asc', description = "choose order : asc or desc")):

    Valid_fields = ["age", "class", "roll", "math_marks", "english_marks", "science_marks"] 

    if sorted_by not in Valid_fields:
        raise HTTPException(status_code = 404, detail = f'Invalid_fields, select from {Valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code = 404, detail = 'Choose between asc or desc')

    data = load_data()

    if order == 'asc':
        sorted_data = list(data.values())
        sorted_data.sort(key = lambda x : x[sorted_by])
        return sorted_data
    else:
        sorted_data = list(data.values())
        sorted_data.sort(key = lambda x : x[sorted_by], reverse = True)
        return sorted_data

@app.post("/create")
def student_created(student : dict = Body()):

    data = load_data()

    student_id = student["id"]
    data[student_id] = student
    del data[student_id]["id"]

    save_data(data)

    return "Successfully student created"