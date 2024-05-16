import praw
import time
import os
import requests


def bot_login():
    print("Authenticating...")
    # reddit = praw.Reddit(username = config.username,
    #             password = config.password,
    #             client_id = config.client_id,
    #             client_secret = config.client_secret,
    #             user_agent = "My_bot v0.1")
    
    reddit = praw.Reddit("my_bot", user_agent = "My_bot v0.1")
    
    print(f"Authenticated as {reddit.user.me()}")

    return reddit

def run_bot(reddit, replied_comments, bad_users):
    n = 10
    # my_ test_zen is a custom subreddit I created to experiment in this project
    for comment in reddit.subreddit("my_test_zen").comments(limit = n):
        if "markov" in comment.body and comment.id not in replied_comments: # can also add "comment.author != reddit.user.me()" to prevent from replying to itself
            comment_reply = "I am sorry but I am going to have to downvote you Mr. Chain Bot https://imgur.com/gallery/troll-face-KpCvMuf"
            joke = requests.get("https://api.chucknorris.io/jokes/random").json()["value"]
            comment.reply(f"{comment_reply}. Oh also here is a joke: \n\n>{joke}")
            comment.downvote()
            print(f"Comment {comment.id} made by {comment.author} had \"markov\" so it was replied and downvoted!")
            
            replied_comments.append(comment.id)

            with open ("Text Files/replied_comments.txt", "a") as file:
                file.write(comment.id + "\n")
        
        # if comment.author in bad_users:
        #     comment.downvote()

    sec = 10
    print(f"Going to sleep for {sec} seconds")
    time.sleep(sec)

def get_bad_users():
    if not os.path.isfile("Text Files/bad_users.txt"):
        bad_users = []
    else:
        with open("Text Files/bad_users.txt", "r") as file:
            bad_users = file.read()
            bad_users = bad_users.split("\n")
            bad_users = filter(None, bad_users)

    return bad_users

def get_replied_comments():
    if not os.path.isfile("Text Files/replied_comments.txt"):
        replied_comments = []
    else:
        with open("Text Files/replied_comments.txt", "r") as file:
            replied_comments = file.read()
            replied_comments = replied_comments.split("\n")

    return replied_comments

def main():
    if not os.path.exists("Text Files"):
        os.makedirs("Text Files")

    reddit = bot_login()
    replied_comments = get_replied_comments()   # To prevent the bot from replying to the same comments
    bad_users = get_bad_users() # In case you want to specifically downvote these users

    while True:
        run_bot(reddit, replied_comments, bad_users)

#######################################################################

main()