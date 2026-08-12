from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from ..database import get_db
from .. import oauth2
from typing import Optional

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str | None = None,
):
    query = db.query(models.Post)

    if search:
        query = query.filter(models.Post.title.contains(search))

    posts = query.limit(limit).offset(skip).all()

    results = []
    for post in posts:
        vote_count = (
            db.query(func.count(models.Vote.post_id))
            .filter(models.Vote.post_id == post.id)
            .scalar()
        )
        results.append(
            {
                "post": post,
                "votes": vote_count,
            }
        )

    return results

@router.post("/",status_code=201,response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cur.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id = get_current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.id == id) \
        .group_by(models.Post.id)

    result = post_query.first()

    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    post, votes = result

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    return {"post": post, "votes": votes}

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate,db:Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post =post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    if updated_post.owner_id != get_current_user.id:
            raise HTTPException(status_code=403,detail="Not authorized to perform the requested action")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{id}",status_code=204)
def delete_post(id: int,db:Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # deleted_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)  
    post = post_query.first() 
    if post == None:
       raise HTTPException(status_code=404, detail = f"Post with id {id} not found")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=403,detail="Not authorized to perform the requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

# @router.get("/posts/all/{id}",status_code=201)