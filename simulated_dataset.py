import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

# Set seed for reproducibility
random.seed(42)

# Define sample tags and audio IDs
sample_tags = ["travel", "food", "coding", "japanese songs", "cooking", "memes", "asian cuties", "anime"]
audio_ids = [f"audio_{i}" for i in range(20)]

# Generate users
num_users = 100
user_ids = [f"user_{i}" for i in range(num_users)]

users_data = []
for user in user_ids:
    followed_users = random.sample([u for u in user_ids if u != user], random.randint(5, 15))
    liked_reels = [f"reel_{random.randint(0, 299)}" for _ in range(random.randint(5, 20))]
    view_history = [f"reel_{random.randint(0, 299)}" for _ in range(random.randint(10, 30))]
    users_data.append({
        "user_id": user,
        "followed_users": ",".join(followed_users),
        "liked_reels": ",".join(liked_reels),
        "view_history": ",".join(view_history)
    })

# Generate reels
num_reels = 300
reel_ids = [f"reel_{i}" for i in range(num_reels)]

reels_data = []
for reel in reel_ids:
    creator_id = random.choice(user_ids)
    tags = random.sample(sample_tags, random.randint(1, 3))
    audio_id = random.choice(audio_ids)
    like_count = random.randint(0, 1000)
    view_count = random.randint(like_count, like_count + 5000)  # views ≥ likes
    timestamp = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
    reels_data.append({
        "reel_id": reel,
        "creator_id": creator_id,
        "tags": ",".join(tags),
        "audio_id": audio_id,
        "like_count": like_count,
        "view_count": view_count,
        "timestamp": timestamp.isoformat()
    })

# Convert to DataFrames
users_df = pd.DataFrame(users_data)
reels_df = pd.DataFrame(reels_data)

# Save to CSV
users_csv_path = "Datasets/simulated_users.csv"
reels_csv_path = "Datasets/simulated_reels.csv"
users_df.to_csv(users_csv_path, index=False)
reels_df.to_csv(reels_csv_path, index=False)

users_csv_path, reels_csv_path
