from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from typing import List
from ..oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


# ************ USERS *************
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # hash the password- user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        return Response(
            content="Duplicate data", status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found.",
        )
    return user


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def get_users(
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    users = db.query(models.User).all()
    return users
