from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #optional field, user doesnt need to provide, defaults to true
    rating: Optional[int] = None #another optional, must be an int if created, 

@app.get("/")
async def root():
    return {"message": "welcome!"}

@app.get("/posts")
async def get_posts():
    return {"data":"this is a post"}

@app.post("/createposts")
def create_posts(post: Post):#extract all the fields from the body, convent into a python dictionary, store inside a variable named payload
    print(post)
    print(post.dict()) #converts our pydanic model into a dictionary
    return {"data": post}
#post.title -> top beaches in florida
#title str, content str