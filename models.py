from sqlalchemy import Column, Integer, String, JSON
from database import Base  # Ensure Base is imported

class VideoPost(Base):
    __tablename__ = "video_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    views = Column(Integer)
    upvotes = Column(Integer)
    video_url = Column(String)
    thumbnail = Column(String)
    tags = Column(JSON)  # Store tags as JSON
