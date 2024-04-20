from flask import Flask, render_template
import random
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)

# Sample User-Item Interaction Data
data = {
    'user_id': [1, 2, 2, 1, 4, 3, 3, 2, 4, 4,
                4, 3, 1, 2, 5, 3, 3, 5, 3, 3,
                1, 3, 5, 3, 2, 2, 2, 2, 4, 4,
                1, 5, 3, 1, 1, 3, 1, 2, 2, 5,
                4, 2, 5, 3, 1, 4, 1, 4, 4, 3,
                3, 5, 4, 4, 3, 5, 5, 1, 1, 4,
                1, 1, 4, 3, 3, 4, 5, 2, 3, 3,
                5, 1, 1, 4, 3, 1, 1, 4, 5, 1,
                5, 5, 5, 3, 3, 2, 5, 1, 5, 3,
                5, 4, 5, 5, 5, 3, 3, 5, 5, 4,
                5, 5, 1, 4, 4, 1, 1, 4, 2, 2,
                2, 2, 3, 5, 4, 3, 4, 5, 4, 3,
                3, 1, 2, 4, 2, 4, 5, 2, 2, 3,
                3, 4, 2, 5, 3, 3, 5, 1, 4, 2,
                1, 5, 3, 2, 3, 2, 2, 4, 3, 2],
    'item_id': ['Health and Medicine', 'Business and Finance',
                'Health and Medicine', 'Education',
                'Business and Finance', 'Health and Medicine',
                'Politics', 'Politics', 'Science and Technology',
                'Environment', 'Business and Finance',
                'Business and Finance', 'Education',
                'Economy', 'Arts and Culture',
                'Politics', 'Business and Finance',
                'Politics', 'Economy',
                'International Relations', 'Arts and Culture',
                'Economy', 'Arts and Culture',
                'Sports', 'Environment',
                'Arts and Culture', 'Health and Medicine',
                'Health and Medicine', 'Science and Technology',
                'Politics', 'Health and Medicine',
                'Environment', 'Arts and Culture',
                'Arts and Culture', 'Environment',
                'Business and Finance', 'Science and Technology',
                'International Relations', 'Sports',
                'International Relations', 'Business and Finance',
                'International Relations', 'International Relations',
                'Arts and Culture', 'Education',
                'Economy', 'Education',
                'Education', 'Health and Medicine',
                'Business and Finance', 'Politics',
                'Sports', 'Arts and Culture',
                'Sports', 'Business and Finance',
                'Education', 'International Relations',
                'Arts and Culture', 'Business and Finance',
                'Business and Finance', 'Arts and Culture',
                'Arts and Culture', 'International Relations', 
                'Economy', 'Business and Finance',
                'Science and Technology', 'Business and Finance',
                'Arts and Culture', 'Education',
                'Economy', 'Business and Finance',
                'International Relations', 'Environment',
                'International Relations',
                'Education', 'Politics',
                'Education', 'Science and Technology',
                'Business and Finance', 'Economy',
                'Arts and Culture', 'Environment',
                'Education', 'Science and Technology',
                'Business and Finance', 'Science and Technology',
                'Sports', 'Economy', 'Politics',
                'Education', 'Environment', 'Sports',
                'International Relations', 'Environment', 
                'Environment', 'International Relations',
                'Sports', 'Sports', 'Sports', 'Science and Technology', 
                'International Relations', 'Sports', 'Sports',
                'Politics', 'Health and Medicine', 'Business and Finance',
                'Health and Medicine', 'Business and Finance',
                'Science and Technology', 'Science and Technology',
                'Health and Medicine', 'Environment', 
                'International Relations', 'Environment',
                'Business and Finance', 'Sports', 'Business and Finance',
                'Economy', 'Arts and Culture', 'Education', 'Sports',
                'Education', 'Politics', 'International Relations',
                'International Relations', 'International Relations',
                'Arts and Culture', 'Environment', 'Health and Medicine',
                'Education', 'Sports', 'Health and Medicine', 'Sports', 
                'Science and Technology', 'Education', 'Education', 'Sports',
                'Science and Technology', 'Politics', 'Business and Finance', 
                'Business and Finance', 'International Relations', 
                'Science and Technology', 'Economy', 'Education', 
                'Environment', 'Health and Medicine', 'International Relations',
                'Science and Technology', 'Education'],
    'rating': [4, 1, 5, 3, 1, 3, 3, 5, 2, 2,
               2, 4, 5, 1, 2, 5, 4, 1, 2, 1,
               1, 3, 1, 3, 1, 1, 1, 4, 5, 3,
               2, 3, 1, 5, 1, 4, 4, 2, 1, 4, 
               3, 1, 1, 4, 5, 5, 1, 1, 2, 2,
               4, 1, 2, 5, 4, 2, 4, 3, 5, 2,
               1, 5, 3, 5, 5, 4, 5, 5, 5, 2,
               3, 5, 1, 5, 2, 1, 1, 5, 3, 5,
               4, 4, 5, 4, 2, 2, 2, 5, 2, 1,
               4, 2, 5, 2, 2, 4, 4, 4, 5, 1,
               5, 3, 4, 2, 5, 3, 3, 4, 1, 1,
               5, 1, 3, 4, 3, 1, 4, 3, 5, 1,
               2, 5, 5, 1, 5, 1, 4, 2, 1, 2,
               2, 5, 3, 5, 3, 2, 1, 1, 1, 1,
               2, 2, 2, 3, 5, 2, 3, 2, 2, 3]
}

df = pd.DataFrame(data)

# Dummy function since I don't have access to your recommendation.py file
def get_recommendations(user_id, user_item_matrix, user_similarity):
    return random.sample(user_item_matrix.columns.tolist(), 3)

# Create a user-item matrix
user_item_matrix = pd.pivot_table(df, values='rating', index='user_id', columns='item_id', fill_value=0)

# Compute user-item similarity using the cosine similarity
user_similarity = cosine_similarity(user_item_matrix)

# Define Flask route to generate recommendations
@app.route('/')
def get_recommendations_route():
    num_random_users = 3
    random_users = random.sample(user_item_matrix.index.to_list(), min(num_random_users, len(user_item_matrix.index)))
    
    recommendations = []
    for user_id in random_users:
        user_recommendations = get_recommendations(user_id, user_item_matrix, user_similarity)
        recommendations.append({'user_id': user_id, 'recommendations': user_recommendations})
    
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
