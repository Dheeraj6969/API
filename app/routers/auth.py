from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, model, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..config import settings

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = oauth2.create_access_token(data={"user_id":user.id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}