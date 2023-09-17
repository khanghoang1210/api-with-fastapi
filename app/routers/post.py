from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List


router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) values(%s, %s, %s) 
    #                                                                     returning *""",
    #                (post.title, post.content, post.published))
    # new_posts = cursor.fetchall()
    # conn.commit()
    print(current_user.email)
    new_posts = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""select * from posts where id = %s""",(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Post with id {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id = %s returning *""",
    #                (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorize to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s
    #                                                  where id = %s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter((models.Post.id==id))
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorize to perform requested action")
    
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


