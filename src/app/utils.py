from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi import HTTPException
from app.db import ActiveSession
from sqlalchemy.orm import Session
from app.auth import get_current_active_user
from app.settings import UserSchema