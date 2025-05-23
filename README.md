# Instagram Reels Recommendation Algorithm

A simple, clean, and easy-to-understand recommendation system for Instagram Reels that utilizes graphs and hashmaps to make personalized content recommendations.

## Overview

This project implements a recommendation algorithm that suggests Instagram Reels to users based on their preferences, social connections, and content engagement patterns. The algorithm combines multiple recommendation strategies:

1. **Graph-based Recommendations**: Uses social connections (following relationships) to recommend content
2. **Collaborative Filtering**: Recommends content based on similar users' preferences
3. **Content-based Filtering**: Recommends content with similar tags/features to what the user has liked
4. **Popularity Metrics**: Factors in overall engagement (likes and views) as a signal

## Features

- **Social Graph Analysis**: Finds first and second-degree connections in the user's social network
- **Tag-based Matching**: Recommends content with tags similar to the user's liked content
- **Recommendation Explanations**: Provides clear explanations for why content was recommended
- **Visualization Tools**: Includes tools to visualize user preferences, recommendation sources, and social networks

## Files

- `reels_recommendation.py`: Core recommendation algorithm implementation
- `demo_recommendation.py`: Interactive demo with visualizations
- `Datasets/`: Contains sample data files
  - `simulated_users.csv`: User data including follows, likes, and view history
  - `simulated_reels.csv`: Reel data including tags, creator, and engagement metrics

## Usage

### Basic Usage

```python
from reels_recommendation import ReelRecommendationSystem

# Initialize the recommendation system
recommender = ReelRecommendationSystem('Datasets/simulated_users.csv', 'Datasets/simulated_reels.csv')

# Get recommendations for a user
user_id = "user_10"
recommendations = recommender.recommend_reels(user_id, n=5)

# Display recommendations
for reel_id in recommendations:
    details = recommender.get_reel_details(reel_id)
    print(f"{reel_id} by {details['creator_id']} - Tags: {details['tags']}")
    print(recommender.explain_recommendation(user_id, reel_id))
```

### Running the Demo

To run the interactive demo with visualizations:

```
python demo_recommendation.py
```

The demo will:

1. Prompt you to enter a user ID
2. Display user information and top tags in liked content
3. Show personalized recommendations and explanations
4. Generate visualizations of tag distributions, recommendation sources, and social connections

## Requirements

- Python 3.6+
- pandas
- matplotlib
- seaborn
- networkx (optional, for social graph visualization)

## Algorithm Details

The recommendation algorithm uses several data structures for efficient lookups:

- **User Liked Reels HashMap**: Maps each user to their liked reels
- **User Viewed Reels HashMap**: Maps each user to their viewed reels
- **User Follows HashMap**: Maps each user to the users they follow
- **Reel Tags HashMap**: Maps each reel to its tags
- **Tag Reels HashMap**: Maps each tag to reels that include it
- **User Created Reels HashMap**: Maps each user to reels they created

The recommendation process:

1. Identifies reels from followed users (direct connections)
2. Finds reels from users followed by followed users (2nd-degree connections)
3. Analyzes tag preferences based on liked content
4. Recommends reels with matching tags
5. Applies popularity adjustments based on engagement metrics
6. Ranks and returns top recommendations

## Extension Ideas

- Add time-decay factors to give higher weight to recent engagements
- Implement negative feedback processing (skipped or reported content)
- Add content embedding models for deeper semantic matching
- Incorporate real-time engagement signals
- Add diversity mechanisms to avoid filter bubbles
