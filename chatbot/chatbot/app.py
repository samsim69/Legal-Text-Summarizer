from flask import Flask, render_template, request, jsonify
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

import re

with open("C:/Users/KIIT/OneDrive/Desktop/chatbot/raw.txt", encoding="utf-8") as f:
    raw_doc = f.read().lower()

# Remove citation references like [84], [10]
raw_doc = re.sub(r'\[\d+\]', '', raw_doc)

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

sentence_tokens = nltk.sent_tokenize(raw_doc)
word_tokens = nltk.word_tokenize(raw_doc)
lemmer = nltk.stem.WordNetLemmatizer()
remove_punc_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punc_dict)))

greet_inputs = ('hello', 'hi', 'wassup', 'how are you')
greet_responses = ('hi', 'hey', 'hello', 'I am fine')

def greet(sentence):
    for word in sentence.split():
        if word.lower() in greet_inputs:
            return random.choice(greet_responses)
    return None

def generate_response(user_response):
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    temp_sentence_tokens = sentence_tokens + [user_response]
    tfidf = TfidfVec.fit_transform(temp_sentence_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    vals_list = vals.flatten()

    if len(vals_list) <= 1:
        return "I am sorry. Unable to understand"

    idx = vals_list.argsort()[-2]
    req_tfidf = vals_list[idx]

    if req_tfidf == 0:
        return "I am sorry. Unable to understand"
    else:
        return sentence_tokens[idx]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_text = request.json.get("message")
    if not user_text:
        return jsonify({"response": "Please say something!"})
    user_text = user_text.lower()

    if user_text in ["bye"]:
        return jsonify({"response": "Goodbye! Have a nice day!"})
    elif user_text in ["thank you", "thanks"]:
        return jsonify({"response": "You are welcome!"})
    else:
        greet_resp = greet(user_text)
        if greet_resp is not None:
            return jsonify({"response": greet_resp})
        else:
            bot_resp = generate_response(user_text)
            return jsonify({"response": bot_resp})

if __name__ == "__main__":
    app.run(debug=True)
