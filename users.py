from database import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import bcrypt
import uvicorn

load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")

class Simple(BaseModel):
    name: str = Field(..., example="Samuel Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
    userType: str = Field(..., example="student")

@app.post("/signup")
def signUp(input: Simple):
    try:
        # Check for duplicate email - USING 'user' TABLE
        duplicate_query = text("""
            SELECT * FROM users WHERE email = :email
        """)
        
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        # Insert new user - ALSO USING 'user' TABLE
        query = text("""
            INSERT INTO users (name, email, password, userType)
            VALUES (:name, :email, :password, :userType)
        """)

        # Hash password
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        hashed_password_str = hashedPassword.decode('utf-8')
        print(f"Hashed password: {hashed_password_str}")
        
        db.execute(query, {
            "name": input.name, 
            "email": input.email, 
            "password": hashed_password_str,
            "userType": input.userType
        })
        db.commit()
        
        return {
            "message": "User created successfully",
            "data": {"name": input.name, "email": input.email}
            # , "password": hashedPassword, "userType": input.userType
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Welcome to the API"}


class LoginRequest(BaseModel):
    email: str = Field(..., example="sammy@gmail.com")
    password: str = Field(..., example="sam123")

@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
        SELECT * FROM users WHERE email = :email
""")
        result = db.execute(query, {"email": input.email}).fetchone()

        if not result:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        verified_password = bcrypt.checkpw(
            input.password.encode('utf-8'),
            result["password"].encode('utf-8')
        )
        
        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))

        if not verified_password:
            raise HTTPException(status_code=404, detail = "Invalid email or password")
        
        return {
            "message": "Login Successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))