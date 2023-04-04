from flask import Flask,render_template,request
import pickle
import numpy as np

popular_data = pickle.load(open("popular.pkl","rb"))
pivot_table = pickle.load(open("pivot_table.pkl", "rb"))
Books = pickle.load(open("Books.pkl","rb"))
similarity_score = pickle.load(open("similarity_score.pkl","rb"))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           book_name = list(popular_data["Book-Title"].values),
                           author=list(popular_data["Book-Author"].values),
                           image=list(popular_data["Image-URL-M"].values),
                           votes=list(popular_data["num_rating"].values),
                           rating=list(popular_data["avg_rating"].values)
                           )

@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")

@app.route("/recommend_books",methods = ["POST"])
def recommend():
    user_input = request.form.get("user_input")
    index = np.where(pivot_table.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_item:
        item = []
        temp_data = Books[Books["Book-Title"] == pivot_table.index[i[0]]]
        item.extend(list(temp_data.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_data.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_data.drop_duplicates("Book-Title")["Image-URL-M"].values))
        data.append(item)
    print(data)

    return render_template("recommend.html",data=data)



if __name__ == '__main__':
    app.run(debug=True)