import asyncio
import csv
from datetime import datetime, timedelta
from random import randint
from twikit import Client, TooManyRequests
from dotenv import load_dotenv, set_key
import os
import requests

# Function to dynamically create or update the .env file with user input
def create_env_file():
    env_file = ".env"
    
    print("Enter your Twitter credentials:")
    username = input("Twitter Username: ")
    email = input("Email Address: ")
    password = input("Password: ")

    with open(env_file, "w") as file:
        file.write(f"TWITTER_USERNAME={username}\n")
        file.write(f"TWITTER_EMAIL={email}\n")
        file.write(f"TWITTER_PASSWORD={password}\n")
    
    print(f"{datetime.now()} - Credentials saved to .env file.")

# Check internet connectivity
def check_internet():
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Wait for internet reconnection
async def wait_for_internet():
    print(f'{datetime.now()} - Internet connection lost. Waiting for reconnection...')
    while not check_internet():
        print(f'{datetime.now()} - No internet. Retrying in 5 minutes...')
        await asyncio.sleep(300)  # Wait 5 minutes
    print(f'{datetime.now()} - Internet connection restored.')

# Countdown timer for rate limiting
async def countdown_timer(seconds):
    while seconds > 0:
        print(f'{datetime.now()} - Rate limit reached. Retrying in {seconds} seconds...', end="\r")
        await asyncio.sleep(1)
        seconds -= 1
    print()  # Clear the line after the countdown ends

# Authenticate with the Twitter client
async def login_to_client(client):
    try:
        username = os.getenv('TWITTER_USERNAME')
        email = os.getenv('TWITTER_EMAIL')
        password = os.getenv('TWITTER_PASSWORD')
        
        try:
            client.load_cookies('cookies.json')
            print(f'{datetime.now()} - Loaded cookies for authentication.')
        except FileNotFoundError:
            print(f'{datetime.now()} - Logging in with credentials...')
            await client.login(auth_info_1=username, auth_info_2=email, password=password)
            client.save_cookies('cookies.json')
            print(f'{datetime.now()} - Cookies saved for future use.')
    except Exception as e:
        print(f'{datetime.now()} - Login error: {e}')

# Fetch tweets with rate-limit handling
async def fetch_tweets(user, cursor=None):
    try:
        if cursor is None:
            print(f'{datetime.now()} - Fetching first batch of tweets...')
            return await user.get_tweets('Tweets')
        else:
            await asyncio.sleep(randint(2, 5))  # Random delay
            print(f'{datetime.now()} - Fetching next batch of tweets...')
            return await cursor.next()
    except TooManyRequests as e:
        print(f'{datetime.now()} - Rate limit hit: {e}')
        await countdown_timer(900)  # Wait for 15 minutes with a countdown
        return await fetch_tweets(user, cursor)
    except Exception as e:
        print(f'{datetime.now()} - Fetch error: {e}')
        return None

# Fetch and save tweets to CSV
async def fetch_and_save_tweets(client, username):
    tweets = None
    total_saved = 0
    file_mode = 'w'  # Default to 'w' to create a new file

    try:
        user = await client.get_user_by_screen_name(username)
    except Exception as e:
        print(f'{datetime.now()} - User fetch error: {e}')
        return

    # Check if the file exists to decide between 'w' or 'a' mode
    if os.path.exists('tweets_data.csv'):
        file_mode = 'a'
    
    with open('tweets_data.csv', mode=file_mode, newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Tweet ID", "Content", "Created At", "Language",
            "Source", "Retweets", "Likes", "Replies",
            "Quotes", "Views", "Sensitive"
        ])

        # Write header only if the file is being created (i.e., in 'w' mode)
        if file_mode == 'w':
            writer.writeheader()

        while True:
            if not check_internet():
                await wait_for_internet()

            tweets = await fetch_tweets(user, tweets)
            if not tweets or len(tweets) == 0:
                print(f'{datetime.now()} - No more tweets to fetch.')
                break

            for tweet in tweets:
                try:
                    created_at = tweet._data['legacy'].get('created_at', 'N/A')
                    tweet_data = {
                        "Tweet ID": tweet._data['rest_id'],
                        "Content": tweet._data['legacy'].get('full_text', 'N/A'),
                        "Created At": created_at,
                        "Language": tweet._data['legacy'].get('lang', 'N/A'),
                        "Source": tweet._data['source'],
                        "Retweets": tweet._data['legacy'].get('retweet_count', 0),
                        "Likes": tweet._data['legacy'].get('favorite_count', 0),
                        "Replies": tweet._data['legacy'].get('reply_count', 0),
                        "Quotes": tweet._data['legacy'].get('quote_count', 0),
                        "Views": tweet._data['views'].get('count', 0),
                        "Sensitive": tweet._data['legacy'].get('possibly_sensitive', False),
                    }
                    writer.writerow(tweet_data)
                    total_saved += 1
                except Exception as e:
                    print(f'{datetime.now()} - Error processing tweet: {e}')

            print(f'{datetime.now()} - Progress: {total_saved} tweets saved so far.')

async def main():
    create_env_file()  # Create or update the .env file
    load_dotenv()  # Reload environment variables after creating the .env file

    twitter_username = input("Enter the Twitter username to scrape tweets from: ")

    client = Client(language='en-US')
    await login_to_client(client)
    await fetch_and_save_tweets(client, twitter_username)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print(f'{datetime.now()} - Script interrupted. Exiting gracefully.')
except Exception as e:
    print(f'{datetime.now()} - Unexpected error: {e}')
