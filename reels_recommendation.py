import pandas as pd
import numpy as np
from collections import defaultdict, Counter

class ReelRecommendationSystem:
    def __init__(self, users_file, reels_file):
        
        self.users_df = pd.read_csv(users_file)
        self.reels_df = pd.read_csv(reels_file)
        
        # Hashmaps for efficient lookups
        self.user_liked_reels = {}  
        self.user_viewed_reels = {}  
        self.user_follows = {}     
        self.reel_tags = {}         
        self.tag_reels = defaultdict(set)  
        self.user_created_reels = defaultdict(set)  
        
        # Build the graph and hashmaps
        self._build_data_structures()
    
    def _build_data_structures(self):
       
        # Process reels data
        for _, row in self.reels_df.iterrows():
            reel_id = row['reel_id']
            creator_id = row['creator_id']
            tags = row['tags'].split(',') if isinstance(row['tags'], str) else []
            
            # Add to reel tags map
            self.reel_tags[reel_id] = tags
            
            # Add to user created reels
            self.user_created_reels[creator_id].add(reel_id)
            
            # Add to tag -> reels map
            for tag in tags:
                tag = tag.strip()
                self.tag_reels[tag].add(reel_id)
        
        # Process user data
        for _, row in self.users_df.iterrows():
            user_id = row['user_id']
            
            # Process followed users
            followed = row['followed_users'].split(',') if isinstance(row['followed_users'], str) else []
            self.user_follows[user_id] = set(followed)
            
            # Process liked reels
            liked = row['liked_reels'].split(',') if isinstance(row['liked_reels'], str) else []
            self.user_liked_reels[user_id] = set(liked)
            
            # Process viewed reels
            viewed = row['view_history'].split(',') if isinstance(row['view_history'], str) else []
            self.user_viewed_reels[user_id] = set(viewed)
    
    def _find_second_degree_connections(self, user_id):
        
        second_degree_connections = set()
        for followed_user in self.user_follows[user_id]:
            if followed_user in self.user_follows:
                second_degree_connections.update(self.user_follows[followed_user])
        
        # Remove the user themselves and their direct connections
        second_degree_connections -= {user_id}
        second_degree_connections -= self.user_follows[user_id]
        
        return second_degree_connections
    
    def recommend_reels(self, user_id, n=10):
        
        if user_id not in self.user_liked_reels:
            return "User not found"
        
        # Get user's liked and viewed reels
        liked_reels = self.user_liked_reels[user_id]
        viewed_reels = self.user_viewed_reels[user_id]
        
        # All reels the user has interacted with (to avoid recommending them)
        interacted_reels = liked_reels.union(viewed_reels)
        
        # Recommendation candidates with scores
        candidate_scores = defaultdict(float)
        
        # Collaborative filtering: Find reels from followed users
        for followed_user in self.user_follows[user_id]:
            for reel in self.user_created_reels[followed_user]:
                if reel not in interacted_reels:
                    candidate_scores[reel] += 3.0 
        
        # Content-based filtering: Find reels with similar tags to liked reels
        user_tag_preferences = Counter()
        for liked_reel in liked_reels:
            if liked_reel in self.reel_tags:
                for tag in self.reel_tags[liked_reel]:
                    user_tag_preferences[tag.strip()] += 1
        
        # Find reels that match the user's tag preferences
        for tag, count in user_tag_preferences.items():
            tag_weight = count / len(liked_reels) if liked_reels else 0
            for reel in self.tag_reels[tag]:
                if reel not in interacted_reels:
                    candidate_scores[reel] += tag_weight * 2.0
        
        # Graph-based recommendations: Find reels from 2nd-degree connections
        second_degree_connections = self._find_second_degree_connections(user_id)
        for connection in second_degree_connections:
            for reel in self.user_created_reels[connection]:
                if reel not in interacted_reels:
                    candidate_scores[reel] += 1.5  
        
        # Add popularity boost - fixed to properly iterate through the dataframe
        for _, row in self.reels_df.iterrows():
            reel = row['reel_id']
            if reel not in interacted_reels:
                like_count = row['like_count']
                view_count = row['view_count']
                # Normalize popularity
                popularity_score = 0.0001 * (like_count + 0.1 * view_count)
                candidate_scores[reel] += popularity_score
        
        # Sort candidates by score and return top N
        top_reels = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return [reel_id for reel_id, score in top_reels]
    
    def get_reel_details(self, reel_id):
        
        if reel_id in self.reel_tags:
            reel_data = self.reels_df[self.reels_df['reel_id'] == reel_id].iloc[0]
            return {
                'reel_id': reel_id,
                'creator_id': reel_data['creator_id'],
                'tags': self.reel_tags[reel_id],
                'like_count': reel_data['like_count'],
                'view_count': reel_data['view_count']
            }
        return None
    
    def explain_recommendation(self, user_id, reel_id):
        
        if user_id not in self.user_liked_reels or reel_id not in self.reel_tags:
            return "User or reel not found"
        
        explanation = []
        
        # Check if creator is followed
        reel_creator = self.reels_df[self.reels_df['reel_id'] == reel_id].iloc[0]['creator_id']
        if reel_creator in self.user_follows[user_id]:
            explanation.append(f"You follow the creator {reel_creator}")
        
        # Check for second-degree connection
        second_degree_connections = self._find_second_degree_connections(user_id)
        if reel_creator in second_degree_connections:
            explanation.append(f"{reel_creator} is followed by someone you follow")
        
        # Check for tag similarity
        user_liked_tags = set()
        for liked_reel in self.user_liked_reels[user_id]:
            if liked_reel in self.reel_tags:
                user_liked_tags.update([tag.strip() for tag in self.reel_tags[liked_reel]])
        
        reel_tags = set([tag.strip() for tag in self.reel_tags[reel_id]])
        common_tags = user_liked_tags.intersection(reel_tags)
        
        if common_tags:
            explanation.append(f"Contains tags you like: {', '.join(common_tags)}")
        
        # Check for popularity
        reel_data = self.reels_df[self.reels_df['reel_id'] == reel_id].iloc[0]
        if reel_data['like_count'] > 500 or reel_data['view_count'] > 3000:
            explanation.append(f"Popular content with {reel_data['like_count']} likes and {reel_data['view_count']} views")
        
        if not explanation:
            return "This reel matched your general preferences"
        
        return "Recommended because: " + "; ".join(explanation)