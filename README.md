# Instagram Reels Recommendation System

A recommendation system that suggests personalized Instagram Reels using graph algorithms and efficient data structures. The system combines social network analysis, content-based filtering, and engagement metrics to provide relevant recommendations.

## Project Description

This project implements a recommendation algorithm for Instagram Reels with the following key features:

1. **Multiple Recommendation Strategies**:

   - Graph-based recommendations using social connections
   - Content-based filtering using reel tags
   - Collaborative filtering based on user interactions
   - Popularity-based boosting using engagement metrics

2. **Visualization Tools**:

   - Tag distribution analysis
   - Social network visualization
   - Recommendation explanation system

3. **Interactive Interfaces**:
   - Command-line demo interface
   - Streamlit web application
   - Detailed recommendation explanations

## Data Structures Used

The system uses several efficient data structures for quick lookups and recommendations:

```python
# Core Data Structures
user_liked_reels = {}      # HashMap: user_id -> Set(liked_reel_ids)
user_viewed_reels = {}     # HashMap: user_id -> Set(viewed_reel_ids)
user_follows = {}          # HashMap: user_id -> Set(followed_user_ids)
reel_tags = {}            # HashMap: reel_id -> List(tags)
tag_reels = defaultdict(set)  # HashMap: tag -> Set(reel_ids)
user_created_reels = defaultdict(set)  # HashMap: user_id -> Set(created_reel_ids)
```

## Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/AungKyawWin20/Instagram-Reels-Recommendation-Algorithm.git
cd Instagram-Reels-Recommendation-Algorithm
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

## Running the Code

### 1. Command Line Demo

```bash
python demo_recommendation.py
```

### 2. Web Interface

```bash
streamlit run app.py
```

## Sample Usage and Output

### Command Line Interface

```python
# Input
Enter a user_id to analyze (or 'q' to quit): user_10

# Output
User: user_10
Number of followed users: 8
Number of liked reels: 11
Number of viewed reels: 16

Top tags in liked reels:
- cooking: 3
- travel: 2
- anime: 2
- food: 2
- coding: 1

Top 5 Recommendations:
1. reel_145 by user_28 - Tags: ['memes']
   Recommended because: user_28 is followed by someone you follow; Popular content with 790 likes and 3050 views

2. reel_187 by user_66 - Tags: ['asian cuties', 'memes', 'travel']
   Recommended because: Contains tags you like: travel; Popular content with 396 likes and 4624 views
```

### Web Interface

The Streamlit web interface provides:

- Interactive user selection
- Visual tag distribution analysis
- Detailed recommendations with explanations
- Sample video previews for top tags

## Data Structure Details

### 1. Graph Representation

- Uses adjacency lists through hashmaps for efficient social connection lookups
- Supports quick traversal for finding 2nd-degree connections
- Time Complexity: O(1) for direct connection lookups

### 2. Recommendation Scoring

```python
candidate_scores = defaultdict(float)
# Scoring weights:
# - Direct connections: 3.0
# - Second-degree connections: 1.5
# - Tag matches: 2.0 * (tag_frequency/total_likes)
# - Popularity: 0.0001 * (likes + 0.1 * views)
```

### 3. Data Processing Pipeline

1. Load and parse CSV data
2. Build efficient lookup structures
3. Process user interactions and social connections
4. Generate and rank recommendations

## Project Structure

```
├── Datasets/
│   ├── simulated_reels.csv
│   └── simulated_users.csv
├── app.py                 # Streamlit web interface
├── demo_recommendation.py # Command-line demo
├── reels_recommendation.py # Core algorithm
└── requirements.txt
```

## Sample Data Format

### simulated_users.csv

```csv
user_id,followed_users,liked_reels,view_history
user_0,"user_15,user_4","reel_258,reel_13","reel_142,reel_79"
```

### simulated_reels.csv

```csv
reel_id,creator_id,tags,audio_id,like_count,view_count,timestamp
reel_0,user_96,"travel,anime,memes",audio_11,456,2424,2025-04-15
```

## Future Improvements

- Add time-decay for engagement metrics
- Implement negative feedback processing
- Add content embedding models
- Add real-time recommendation updates
- Implement diversity mechanisms
