from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, utils
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
    get_current_user: int = Depends(oauth2.get_current_user_optional),
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
        # Get the owner user
        owner = db.query(models.User).filter(models.User.id == post.owner_id).first()
        
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "published": post.published,
            "created_at": post.created_at,
            "owner_id": post.owner_id,
            "owner": {
                "id": owner.id,
                "email": owner.email,
                "created_at": owner.created_at
            } if owner else None
        }
        
        results.append({
            "post": post_dict,
            "votes": vote_count,
        })

    return results

@router.post("/",status_code=201,response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user_optional)):
    # If no authenticated user, create or get a default test user
    if not get_current_user:
        existing_user = db.query(models.User).filter(models.User.id == 1).first()
        if not existing_user:
            hashed_password = utils.hash("test")
            default_user = models.User(id=1, email="test@example.com", password=hashed_password)
            db.add(default_user)
            db.commit()
        owner_id = 1
    else:
        owner_id = get_current_user.id
    
    new_post = models.Post(owner_id=owner_id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user_optional),
):
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .filter(models.Post.id == id) \
        .group_by(models.Post.id)

    result = post_query.first()

    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    post, votes = result

    # Only check authorization if user is authenticated
    if get_current_user and post.owner_id != get_current_user.id:
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