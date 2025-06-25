import streamlit as st
import pickle

# Load data
books = pickle.load(open('books.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("📚 Book Recommendation System")

book_list = books['book-title'].values
selected_book = st.selectbox("Choose a Book", book_list)

def recommend(book_name):
    index = books[books['title'] == book_name].index[0]
    distances = similarity[index]
    recommended_books = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    rec_titles = []
    for i in recommended_books:
        rec_titles.append(books.iloc[i[0]].title)
    return rec_titles

if st.button("Recommend"):
    recommendations = recommend(selected_book)
    st.subheader("Recommended Books:")
    for rec in recommendations:
        st.write("•", rec)
        
