import tensorflow as tf
import numpy as np
import pickle
from sqlalchemy.orm import sessionmaker
from database import engine
from models import VideoPost

# ✅ Load Model & Video Mapping
model = tf.keras.models.load_model("video_recommendation_model.h5")
with open("video_mapping.pkl", "rb") as f:
    video_ids = pickle.load(f)

# ✅ Load Data from Database
Session = sessionmaker(bind=engine)
session = Session()
videos = session.query(VideoPost).all()
session.close()

# ✅ Convert Data to NumPy Array
data = np.array([[video.id, video.category_id, video.view_count, 
                  video.upvote_count, video.rating_count, video.average_rating] 
                 for video in videos])

# ✅ Normalize Data
data[:, 2:] = data[:, 2:] / np.max(data[:, 2:], axis=0)

# ✅ Predict Recommendations
predictions = model.predict(data[:, 1:])
top_indices = np.argsort(predictions.flatten())[::-1][:10]  # Top 10 recommendations

# ✅ Get Recommended Video IDs
recommended_video_ids = [video_ids[i] for i in top_indices]

def get_recommendations():
    """
    Fetch recommended videos based on AI model predictions.
    """
    recommended_videos = [video for video in videos if video.id in recommended_video_ids]
    return [{"id": v.id, "title": v.title, "video_url": v.video_link} for v in recommended_videos]
