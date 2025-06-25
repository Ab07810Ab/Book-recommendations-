import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load all data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Rename columns for easy access
popular_df.columns = popular_df.columns.str.strip()
popular_df = popular_df.rename(columns={
    'Book-Title': 'book_title',
    'Book-Author': 'book_author',
    'Image-URL-M': 'image_url'
})
popular_df['book_title']
popular_df['book_author']
popular_df['image_url']

# Streamlit setup
st.set_page_config(page_title="📚 Book Recommender", layout="wide")
st.title("📚 Book Recommendation System")

st.subheader("🔥 Popular Books")
for i in range(min(5, len(popular_df))):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(popular_df['image_url'].iloc[i], width=100)
    with col2:
        st.write(f"**{popular_df['book_title'].iloc[i]}**")
        st.write(f"👤 {popular_df['book_author'].iloc[i]}")
        st.write(f"⭐ {popular_df['avg_rating'].iloc[i]:.2f} | 🗳️ {popular_df['num_ratings'].iloc[i]} votes")
    st.markdown("---")

st.subheader("🔍 Get Book Recommendations")
user_input = st.text_input("Enter a book title exactly (case sensitive):")

if st.button("Recommend"):
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        st.subheader("📘 Recommended Books:")
        for i in similar_items:
            book_title = pt.index[i[0]]
            temp_df = books[books['Book-Title'] == book_title].drop_duplicates('Book-Title')
            for _, row in temp_df.iterrows():
                st.image(row['Image-URL-M'], width=100)
                st.write(f"**{row['Book-Title']}** by {row['Book-Author']}")
                st.markdown("---")
    else:
        st.error("❌ Book not found! Please enter the exact book title as shown in the dataset.")
        
