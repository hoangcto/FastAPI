from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user


models.Base.metadata.create_all(bind=engine) #only check if the table with the specific name exists or not

app = FastAPI()


## set up connection to database
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password ='9jh833f2qk', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connect was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
         return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
         return i
        

app.include_router(post.router)        
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}