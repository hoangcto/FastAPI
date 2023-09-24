from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schema
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# getting all posts
@router.get("/", response_model=List[schema.Response])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# creating a post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schema.Response)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# getting individual post
@router.get("/{id}", response_model=schema.Response )
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id:{id} not found')
    return post

@router.put("/{id}", response_model=schema.Response)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()
    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id:{id} does not exist')
    
    post_query.update( post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id:{id} does not exist')
    
    post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)