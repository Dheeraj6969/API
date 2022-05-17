from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import oauth2
from .. import model, schemas,  oauth2
from typing import List, Optional
from sqlalchemy.orm.session import Session
from ..database import get_db
from sqlalchemy import func
router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model = List[schemas.PostOut])
#@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: model.User = Depends(oauth2.get_current_user), Limit: int=10, skip: int=0, search: Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #posts = db.query(model.Post.owner_id == current_usre.id).all() for getting only my posts
    #posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(Limit).offset(skip).all()
    posts = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(model.Vote, model.Vote.post_id==model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(Limit).offset(skip).all()
    #print(results)
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    #print(**post.dict())
    new_post = model.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(model.Vote, model.Vote.post_id==model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()