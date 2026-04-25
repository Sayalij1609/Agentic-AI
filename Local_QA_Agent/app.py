from flask import Flask, render_template, request, jsonify
from chatbot import ask_question

app = Flask(__name__)

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query")

    answer = ask_question(query)

    chat_history.append({"user": query, "bot": answer})

    return jsonify({
        "answer": answer,
        "history": chat_history
    })

if __name__ == "__main__":
    app.run(debug=True)