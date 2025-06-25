import pickle
import pandas as pd

# Step 1: Load popular.pkl
with open('popular.pkl', 'rb') as f:
    popular_df = pickle.load(f)

# Step 2: Debug current columns
print("📄 Existing columns in popular_df:", popular_df.columns.tolist())

# Step 3: Check if rating data exists or needs mock values
if 'Book-Rating' in popular_df.columns:
    # Group by book to compute avg and count
    ratings_group = popular_df.groupby('Book-Title')['Book-Rating'].agg(['mean', 'count']).reset_index()
    ratings_group.rename(columns={'mean': 'avg_rating', 'count': 'num_ratings'}, inplace=True)

    # Merge back with original popular_df
    popular_df = pd.merge(popular_df, ratings_group, on='Book-Title', how='left')

else:
    print("⚠️ 'Book-Rating' column not found. Adding dummy values.")
    popular_df['avg_rating'] = 4.0
    popular_df['num_ratings'] = 100

# Step 4: Save fixed version
with open('popular.pkl', 'wb') as f:
    pickle.dump(popular_df, f)

print("✅ Fixed popular.pkl with avg_rating and num_ratings!")

