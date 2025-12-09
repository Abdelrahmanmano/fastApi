from fastapi import APIRouter, status, HTTPException, Depends
from ..database import get_db
from .. import models, oauth2, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/like",
    tags=["Likes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReturnLikes)
def toggle_like(likes: schemas.Likes, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    like_query = db.query(models.Likes).filter(models.Likes.user_id == current_user.id, models.Likes.post_id == likes.post_id)
    like_obj = like_query.first()
    if likes.vote_dir == 1:
        if like_obj:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User Likes Before")
        new_like = models.Likes(post_id=likes.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like
    else:
        if like_obj:
            like_obj.delete(synchorize_session=False)
            # db.delete(like_obj)
            db.commit()
            return like_obj
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Like On Post not found")