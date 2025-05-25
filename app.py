import streamlit as st
import pandas as pd
import plotly.express as px
from reels_recommendation import ReelRecommendationSystem

# Initialize recommendation system
@st.cache_resource
def load_recommender():
    return ReelRecommendationSystem('Datasets/simulated_users.csv', 'Datasets/simulated_reels.csv')

def visualize_tag_distribution(recommender, user_id):
    user_tag_counts = {}
    for reel_id in recommender.user_liked_reels[user_id]:
        if reel_id in recommender.reel_tags:
            for tag in recommender.reel_tags[reel_id]:
                tag = tag.strip()
                user_tag_counts[tag] = user_tag_counts.get(tag, 0) + 1
    return pd.Series(user_tag_counts).sort_values(ascending=False)

# App
st.title("Instagram Reels Recommendation System")

# Load recommender
recommender = load_recommender()

# Sidebar
st.sidebar.title("User Selection")
user_id = st.sidebar.selectbox(
    "Select a user",
    options=list(recommender.user_liked_reels.keys())
)

if user_id:
    # User Stats
    st.header(f"User Profile: {user_id}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Followed Users", len(recommender.user_follows[user_id]))
    with col2:
        st.metric("Liked Reels", len(recommender.user_liked_reels[user_id]))
    with col3:
        st.metric("Viewed Reels", len(recommender.user_viewed_reels[user_id]))

    # Tag Distribution
    st.header("Tag Preferences")
    tag_series = visualize_tag_distribution(recommender, user_id)
    
    if not tag_series.empty:
        fig = px.bar(
            tag_series.head(10),
            title="Top Tags in Liked Reels",
            labels={'index': 'Tag', 'value': 'Count'}
        )
        st.plotly_chart(fig)
        
        # Add sample videos for top tags
        st.header("Sample Videos for Top Tags")
        top_3_tags = tag_series.head(3).index.tolist()
        
        # Create three columns for videos
        video_cols = st.columns(3)
        
        # Sample video URLs for each category
        video_samples = {
            'anime': 'assets/anime.mp4',
            'food': 'assets/food.mp4',
            'travel': 'assets/travel.mp4',
            'coding': 'assets/coding.mp4',
            'japanese songs': 'assets/japanesesongs.mp4',
            'memes': 'assets/meme.mp4',
            'cooking': 'assets/cooking.mp4',
            'asian cuties': 'assets/asiancuties.mp4'
        }
        
        # Display videos in columns
        for idx, tag in enumerate(top_3_tags):
            with video_cols[idx]:
                st.subheader(f"#{tag}")
                if tag in video_samples:
                    st.video(video_samples[tag])
                else:
                    st.info(f"No sample video available for {tag}")

    # Recommendations
    st.header("Recommended Reels")
    num_recommendations = st.slider("Number of recommendations", 5, 20, 5)
    recommendations = recommender.recommend_reels(user_id, n=num_recommendations)

    for i, reel_id in enumerate(recommendations, 1):
        details = recommender.get_reel_details(reel_id)
        with st.expander(f"{i}. {reel_id} by {details['creator_id']}"):
            st.write(f"**Tags:** {', '.join(details['tags'])}")
            st.write(f"**Likes:** {details['like_count']}")
            st.write(f"**Views:** {details['view_count']}")
            st.write(f"**Why recommended:** {recommender.explain_recommendation(user_id, reel_id)}")