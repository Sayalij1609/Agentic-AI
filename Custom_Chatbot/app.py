from flask import Flask, render_template, request, jsonify
from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

app = Flask(__name__)

llm = ChatOllama(
    model="phi3",
    temperature=0.7
)

memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = conversation.predict(input=user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)