import tweepy
import openai
from flask import Flask, request, jsonify, render_template


# Set up Tweepy API client
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Set up OpenAI API client
openai.api_key = ""

# Define function to generate shitpost reply with customizable prompt
def generate_shitpost(tweet_text, prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt.format(tweet_text),
        temperature=0.9,
        max_tokens=100,
        n=1,
        stop=None,
    )
    if "choices" not in response or not response.choices:
        return "Error: no choices returned from OpenAI API."
    shitpost_reply = response.choices[0].text
    return shitpost_reply

# Set up Flask app
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define route for generating shitpost reply
@app.route('/generate', methods=['GET'])
def generate():
    tweet_link = request.args.get('tweet_link')
    tweet_id = tweet_link.split("/")[-1]
    tweet = api.get_status(tweet_id)
    tweet_text = tweet.text
    prompt = request.args.get('prompt', "Here's a tweet I found: {}. Write a reply tweet with max 240 characters and use a really sarcastic and ironic tone of voice")
    shitpost_reply = generate_shitpost(tweet_text, prompt)
    return jsonify({"shitpost_reply": shitpost_reply})

# Define route for serving HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)


