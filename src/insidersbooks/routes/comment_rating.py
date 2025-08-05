from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.comment import Comment
from ..models.comment_reaction import CommentReaction
from ..schemas.comment_reaction import CommentReactionCreate, CommentReactionRead
from ..dependencies.auth import get_current_user

router = APIRouter(prefix='/comment_reaction', tags =['comment_reactions'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post('/{comment_id}', response_model = CommentReactionRead)
def react_to_comment(comment_id: int, reaction_data: CommentReactionCreate,
                     db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    
    existing = db.query(CommentReaction).filter_by(user_id = current_user.id, comment_id = comment_id).first()
    
    if existing:
        existing.is_like = reaction_data.is_like
    else:
        existing = CommentReaction(
            is_like = reaction_data.is_like,
            user_id = current_user.id,
            comment_id = comment_id
        )
        
    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing

@router.get('/{comment_id}', response_model = CommentReactionRead)
def get_reactions_summary(comment_id: int, db: Session = Depends(get_db)):
    likes = db.query(CommentReaction).filter_by(comment_id = comment_id, is_like = True).count()
    dislikes = db.query(CommentReaction).filter_by(comment_id = comment_id, is_like = False).count()
    return {"likes": likes, "dislikes": dislikes}
        
        
            