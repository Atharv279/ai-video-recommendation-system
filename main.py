from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from services import (
    get_viewed_posts, 
    get_liked_posts, 
    get_inspired_posts, 
    get_rated_posts,
    get_ai_recommendations  # ✅ Import AI recommendations
)
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
FLIC_TOKEN = os.getenv("FLIC_TOKEN")

app = FastAPI()

# ✅ Middleware: Verify Authentication Token
def verify_auth_token(flic_token: str = Header(None)):
    if not flic_token or flic_token != FLIC_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ✅ API: Get AI-Powered Recommendations (New)
@app.get("/ai-recommend", dependencies=[Depends(verify_auth_token)])
def ai_recommend():
    recommendations = get_ai_recommendations()
    return {"recommendations": recommendations}

# ✅ API: Fetch Viewed Posts
@app.get("/fetch/viewed-posts", dependencies=[Depends(verify_auth_token)])
def viewed_posts():
    return get_viewed_posts()

# ✅ API: Fetch Liked Posts
@app.get("/fetch/liked-posts", dependencies=[Depends(verify_auth_token)])
def liked_posts():
    return get_liked_posts()

# ✅ API: Fetch Inspired Posts
@app.get("/fetch/inspired-posts", dependencies=[Depends(verify_auth_token)])
def inspired_posts():
    return get_inspired_posts()

# ✅ API: Fetch Rated Posts
@app.get("/fetch/rated-posts", dependencies=[Depends(verify_auth_token)])
def rated_posts():
    return get_rated_posts()

from services import (
    get_viewed_posts, 
    get_liked_posts, 
    get_inspired_posts, 
    get_rated_posts,
    get_ai_recommendations  # ✅ Correct import
)