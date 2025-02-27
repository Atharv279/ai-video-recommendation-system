import json

# Load JSON data
file_path = "response_1740641085360.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract the list of posts
posts = data.get("posts", [])  # Get 'posts' list, default to empty if missing

# Process and extract useful fields
processed_data = []

for post in posts:
    processed_data.append({
        "id": post.get("id"),
        "title": post.get("title", "No Title"),
        "category": post.get("category", {}).get("name", "Unknown"),
        "views": post.get("view_count", 0),
        "upvotes": post.get("upvote_count", 0),
        "video_url": post.get("video_link"),
        "thumbnail": post.get("thumbnail_url"),
        "tags": post.get("tags", [])
    })

# Save cleaned data
output_file = "processed_data.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(processed_data, file, indent=4)

print(f"✅ Processed {len(processed_data)} posts and saved them in '{output_file}'.")


from sqlalchemy.orm import Session
from database import SessionLocal
from models import VideoPost
import json

# Load processed JSON
with open("processed_data.json", "r") as file:
    data = json.load(file)

db: Session = SessionLocal()

for post in data:
    new_post = VideoPost(
        id=post["id"],
        title=post["title"],
        category=post["category"],
        views=post["views"],
        upvotes=post["upvotes"],
        video_url=post["video_url"],
        thumbnail=post["thumbnail"],
        tags=post["tags"]
    )
    db.add(new_post)

db.commit()
db.close()
print("✅ Data Stored in MySQL!")
