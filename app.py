from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import os
import os
print("📁 Current working directory:", os.getcwd())
print("📁 Files and folders:", os.listdir())
print("📁 /templates contents:", os.listdir("templates"))


app = Flask(__name__)

# Load required pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Strip column names to avoid hidden space bugs
popular_df.columns = popular_df.columns.str.strip()

# Optional: Rename for consistent access (you can skip this if your HTML expects original names)
popular_df = popular_df.rename(columns={
    'Book-Title': 'book_title',
    'Book-Author': 'book_author',
    'Image-URL-M': 'image_url'
})

# Check for required columns
required_cols = ['book_title', 'book_author', 'image_url', 'num_ratings', 'avg_rating']
missing_cols = [col for col in required_cols if col not in popular_df.columns]
if missing_cols:
    raise KeyError(f"Missing columns in popular_df: {missing_cols}")

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['book_title'].values),
                           author=list(popular_df['book_author'].values),
                           image=list(popular_df['image_url'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    try:
        index = np.where(pt.index == user_input)[0][0]
    except IndexError:
        return render_template('recommend.html', data=[], error="❌ Book not found!")

    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        temp_df = temp_df.drop_duplicates('Book-Title')
        item.extend(list(temp_df['Book-Title'].values))
        item.extend(list(temp_df['Book-Author'].values))
        item.extend(list(temp_df['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ✅ Fixed typo from os.envi
    app.run(host='0.0.0.0', port=port)
    