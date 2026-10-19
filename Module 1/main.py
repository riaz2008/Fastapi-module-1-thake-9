from fastapi import FastAPI 

app = FastAPI()

@app.get('/')
def hello():
    return "Hello how are you"

@app.get('/about')
def about():
    return "I was a pen"