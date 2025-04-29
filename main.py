from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kullanıcı Modeli
class User(BaseModel):
    username: str
    password: str

# Basit SQLite veritabanı oluşturma
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY, 
                      username TEXT UNIQUE, 
                      password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Kullanıcı kaydı
@app.post("/register")
def register(user: User):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      (user.username, user.password))
        conn.commit()
        conn.close()
        return {"message": f"User {user.username} registered successfully"}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

# Kullanıcı kimlik doğrulama
@app.post("/login")
def login(user: User):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
    result = cursor.fetchone()
    conn.close()

    if result:
        # Java servisinden JWT token al
        response = requests.post("http://localhost:4567/token", json={"username": user.username})
        if response.status_code == 200:
            return {"token": response.json()["token"]}
        else:
            raise HTTPException(status_code=500, detail="Token alınamadı")
    else:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")

# Root endpoint to serve index.html
@app.get("/")
def read_root():
    return FileResponse("index.html")
