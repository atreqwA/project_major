import numpy as np

def get_recommendations(user_id, user_item_matrix, user_similarity, n=5):
    if user_id not in user_item_matrix.index or user_id >= len(user_similarity):
        print(f"User {user_id} not found in the user-item matrix or user_similarity array index out of bounds.")
        return []

    user_ratings = user_item_matrix.loc[user_id]
    similar_users = user_similarity[user_id]
    similar_users = np.argsort(similar_users)[::-1]

    recommendations = []
    for i in range(len(user_item_matrix.columns)):
        if user_ratings.iloc[i] == 0:
            prediction = 0
            for j in similar_users:
                if user_item_matrix.iloc[j, i] != 0:
                    prediction = user_item_matrix.iloc[j, i]
                    break
            recommendations.append((user_item_matrix.columns[i], prediction))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:n]
