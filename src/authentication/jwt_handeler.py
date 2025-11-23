from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os 
import jwt
from fastapi import HTTPException, status

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 14

def generate_access_token(user_data: dict) -> str:
    try:
        access_token_data = user_data.copy()
        expires_in = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_data.update({ "exp": int(expires_in.timestamp()), "type": "access" })
        
        access_token = jwt.encode(access_token_data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return access_token
        
    except Exception as e:
        print(f"There was an error trying to generate the access token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to generate the access token: {str(e)}"
        )
        

def generate_refresh_token(user_data: dict) -> str:
    try:
        refresh_token_data = user_data.copy()
        expires_in = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token_data.update({ "exp": int(expires_in.timestamp()), "type": "refresh" })
        
        refresh_token = jwt.encode(refresh_token_data, JWT_SECRET, JWT_ALGORITHM)
        
        return refresh_token
        
    except Exception as e:
        print(f"There was an error trying to generate the refresh token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to generate the refresh token: {str(e)}"
        )
        
def generate_user_tokens(user_data: dict) -> dict:
    try:
        access_token = generate_access_token(user_data)
        refresh_token = generate_refresh_token(user_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        
    except Exception as e:
        print(f"There was an error trying to generate the users tokens: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to generate the users tokens: {str(e)}"
        )
        
def decode_access_token(access_token: str) -> dict:
    try:
        decoded_token = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Decoding of the token actually failed"
            )
            
        return decoded_token
        
    except Exception as e:
        print(f"There was an error trying to decode the provided token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to decode the provided token: {str(e)}"
        )
        
def refresh_access_token(refresh_token: str) -> dict:
    try:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required for us to be able to decode it champ"
            )
        
        decoded_token = decode_access_token(refresh_token)
        
        if decoded_token["type"] != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type was passed, we require you to pass the refresh token instead"
            )
        
        user_id = decoded_token["sub"]
        username = decoded_token["username"]
        
        new_tokens_data = {
            "sub": user_id,
            "username": username
        }
        
        new_access_token = generate_access_token(new_tokens_data)
        new_refresh_token = generate_refresh_token(new_tokens_data)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }
        
    except Exception as e:
        print(f"There was an error trying to decode the refresh token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to decode the refresh token: {str(e)}"
        )
        
def get_current_user_handeler(access_token: str) -> dict:
    try:
        decoded_token = decode_access_token(access_token)
        
        user_id = decoded_token["sub"]
        username = decoded_token["username"]
        
        return {
            "user_id": user_id,
            "username": username
        }
        
    except Exception as e:
        print(f"There was an error trying to get the currently logged in user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error trying to get the currently logged in user: {str(e)}"
        )