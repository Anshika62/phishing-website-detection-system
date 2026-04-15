from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

vector_path = os.path.join(BASE_DIR, "vectorizer.pkl")
model_path = os.path.join(BASE_DIR, "phising.pkl")

# Load model safely
try:
    with open(vector_path, "rb") as f:
        vector = pickle.load(f)

    with open(model_path, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print("Error loading model:", e)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        url = request.form['url']

        try:
            prediction = model.predict(vector.transform([url]))[0]

            if prediction == 'bad':
                result = "This is a phishing website! Be Alert!!"
                status = "danger"

            elif prediction == 'good':
                result = "This is a Safe Website!"
                status = "safe"

            else:
                result = "Something went wrong"
                status = "error"

        except Exception as e:
            result = "Error processing URL"
            status = "error"
            print(e)

        return render_template("index.html", predict=result, status=status)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()