import pandas as pd
from reels_recommendation import ReelRecommendationSystem

def visualize_tag_distribution(recommender, user_id):
    """Visualize the distribution of tags in a user's liked reels."""
    user_tag_counts = {}
    
    # Count tags in user's liked reels
    for reel_id in recommender.user_liked_reels[user_id]:
        if reel_id in recommender.reel_tags:
            for tag in recommender.reel_tags[reel_id]:
                tag = tag.strip()
                user_tag_counts[tag] = user_tag_counts.get(tag, 0) + 1
    
    return pd.Series(user_tag_counts).sort_values(ascending=False)

def main():
    print("Instagram Reels Recommendation System Demo")
    print("==========================================")
    
    # Initialize recommendation system
    recommender = ReelRecommendationSystem('Datasets/simulated_users.csv', 'Datasets/simulated_reels.csv')
    
    while True:
        # Get user input
        user_id = input("\nEnter a user_id to analyze (or 'q' to quit): ")
        if user_id.lower() == 'q':
            break
            
        if user_id not in recommender.user_liked_reels:
            print("User not found!")
            continue
        
        # Get recommendations
        recommendations = recommender.recommend_reels(user_id, n=10)
        
        # Display user info
        print(f"\nUser: {user_id}")
        print(f"Number of followed users: {len(recommender.user_follows[user_id])}")
        print(f"Number of liked reels: {len(recommender.user_liked_reels[user_id])}")
        print(f"Number of viewed reels: {len(recommender.user_viewed_reels[user_id])}")
        
        # Visualize tag distribution
        tag_series = visualize_tag_distribution(recommender, user_id)
        print("\nTop tags in liked reels:")
        for tag, count in tag_series.head(5).items():
            print(f"- {tag}: {count}")
        
        # Display recommendations
        print("\nTop 10 Reel Recommendations:")
        for i, reel_id in enumerate(recommendations, 1):
            details = recommender.get_reel_details(reel_id)
            print(f"{i}. {reel_id} by {details['creator_id']} - Tags: {details['tags']}")
            print(f"   {recommender.explain_recommendation(user_id, reel_id)}")
        
if __name__ == "__main__":
    main() 