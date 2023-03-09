from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #optional field, user doesnt need to provide, defaults to true
    rating: Optional[int] = None #another optional, must be an int if created, 

my_posts = [{"title":"title post 1", "content":"content post 1", "id":1},
{"title":"title post 2", "content":"content post 2", "id":2}]

def find_post(id):
    id = int(id)
    print("finding post")
    for p in my_posts:
        if p["id"] == id:
            print(p)
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            print("TYPE ", type(id))
            return i


@app.get("/")
async def root():
    return {"message": "welcome!"}

@app.get("/posts")
async def get_posts():
    return {"data":my_posts}#fastapi will serialize the array, turning into json

@app.post("/posts", status_code=status.HTTP_201_CREATED)#if creating sucessful, return 201
def create_posts(post: Post):#extract all the fields from the body, convent into a python dictionary, store inside a variable named payload
    #(post.dict()) #converts our pydanic model into a dictionary
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
#post.title -> top beaches in florida
#title str, content str

@app.get("/posts/{id}") #id is a path parameter, path parameters are always returned as a string. 
def get_post(id: int, response: Response): #validates and converts id into an int
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
      
    return {"post_detail": f"Here is post {post}"}

@app.delete("/posts/{id}")#don't send any data back when user deletes. send 204 status
def delete_post(id: int):
    #find index in array that has required id
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)