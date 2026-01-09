from flask import Flask,render_template , request
import pickle
import os


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

vector_path = os.path.join(BASE_DIR, "vectorizer.pkl")
model_path = os.path.join(BASE_DIR, "phising.pkl")

# Load vectorizer and model
with open(vector_path, "rb") as f:
    vector = pickle.load(f)

with open(model_path, "rb") as f:
    model = pickle.load(f)

@app.route("/", methods = ['GET','POST'])
def index():
    if request.method =="POST":
        pass
        url = request.form['url']
        # print(url)

        predict = model.predict(vector.transform([url]))[0]
        # print(predict)
        if predict == 'bad':
            predict= "This is a phising website ! Be Alert!! "

        elif predict == 'good' :
            predict = "This is a Good and Safe Website !!" 

        else:
            predict = "Something  went Wrong Here"   
        return render_template("final_frontend.html", predict=predict)
    


    else:
        return render_template("final_frontend.html")
if __name__ =="__main__":
    app.run(debug=True)