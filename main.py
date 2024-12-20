# updated 09:58am - K

import asyncio
import csv
from datetime import datetime
from random import randint
from twikit import Client, TooManyRequests
from dotenv import load_dotenv
import os
import requests
import time

# Load environment variables from the .env file
load_dotenv()

# Set the username of the Twitter account
userName = 'elonmusk'  # You can modify this for different users dynamically

# Function to check internet connection
def check_internet():
    try:
        # Trying to reach Google's DNS server to check for connectivity
        response = requests.get('https://www.google.com', timeout=5)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        return False

# Helper function to fetch tweets asynchronously with rate limit handling
async def get_tweets(user, tweets, retry_count=0):
    try:
        if tweets is None:
            # Get the first batch of tweets
            print(f'{datetime.now()} - Getting tweets for {user.screen_name}...')
            tweets = await user.get_tweets('Tweets')
        else:
            # Wait for a random time between 2 and 5 seconds before fetching the next batch of tweets
            wait_time = randint(2, 5)
            print(f'{datetime.now()} - Getting next batch of tweets for {user.screen_name} after {wait_time} seconds...')
            await asyncio.sleep(wait_time)
            tweets = await tweets.next()  # Await the next batch of tweets

        return tweets

    except TooManyRequests as e:
        # Handle rate limit exceeded error (429)
        print(f'{datetime.now()} - Rate limit exceeded: {e}. Retry attempt {retry_count + 1}')
        
        # Adjust wait time based on retry count
        if retry_count == 0:
            wait_time = 1020  # Wait 17 minutes (17 * 60 seconds)
        elif retry_count == 1:
            wait_time = 600  # Wait 10 minutes (10 * 60 seconds)
        else:
            wait_time = 300  # Wait 5 minutes (5 * 60 seconds)
        
        print(f'{datetime.now()} - Waiting for {wait_time / 60} minutes...')
        # Display countdown timer during the wait
        for remaining_time in range(wait_time, 0, -1):
            mins, secs = divmod(remaining_time, 60)
            print(f'{datetime.now()} - Waiting... {mins:02d}:{secs:02d} remaining', end='\r')
            await asyncio.sleep(1)
        
        print()  # Newline after countdown
        # Retry the request with an incremented retry count
        return await get_tweets(user, tweets, retry_count + 1)

    except Exception as e:
        print(f'{datetime.now()} - Error in get_tweets: {e}')
        return None

# Function to handle internet connection loss and wait until reconnected
async def wait_for_internet():
    print(f'{datetime.now()} - Internet connection lost. Waiting for reconnection...')
    while not check_internet():
        print(f'{datetime.now()} - No internet connection. Retrying in 5 minutes...')
        # Display countdown for the retry in 5-minute intervals
        for remaining_time in range(300, 0, -1):
            mins, secs = divmod(remaining_time, 60)
            print(f'{datetime.now()} - Waiting for connection... {mins:02d}:{secs:02d} remaining', end='\r')
            await asyncio.sleep(1)
        
        print()  # Newline after countdown
    print(f'{datetime.now()} - Internet connection restored.')

async def login_to_client(client):
    """Authenticate with cookies or credentials."""
    try:
        # Get credentials from environment variables
        username = os.getenv('USER_NAME')
        email = os.getenv('E-MAIL')
        password = os.getenv('PASS_WORD')

        try:
            # Try loading cookies if available
            client.load_cookies('cookies.json')
            print(f'{datetime.now()} - Loaded cookies for authentication')
        except FileNotFoundError:
            # If cookies are not available, use login credentials
            print(f'{datetime.now()} - Logging in with credentials...')
            await client.login(auth_info_1=username, auth_info_2=email, password=password)
            client.save_cookies('cookies.json')  # Save cookies for future use
            print(f'{datetime.now()} - Saved cookies after login')

    except Exception as e:
        print(f'{datetime.now()} - Error in login_to_client: {e}')


from datetime import datetime

# Define the threshold date
threshold_date = datetime(2020, 1, 1)

async def fetch_and_print_tweets(client, userName):
    """Fetch tweets and print their data."""
    tweets = None
    total_saved_tweets = 0  # Variable to track total number of saved tweets
    tweets_saved_in_batch = 0  # Track tweets saved in the current batch
    no_tweets_counter = 0  # Track consecutive batches with no tweets

    try:
        # Fetch the user object by screen name
        user = await client.get_user_by_screen_name(userName)
    except Exception as e:
        print(f'{datetime.now()} - Error fetching user by screen name: {e}')
        return

    try:
        # Open CSV file in write mode
        with open('tweets_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[  # Define column names
                "Tweet ID", "Tweet Content", "Language",
                "Created At", "Source", "Retweet Count",
                "Like Count", "Reply Count", "Quote Count",
                "View Count", "Is Retweet", "Possibly Sensitive",
                "Media Available"
            ])
            writer.writeheader()  # Write the header row to CSV

            # Fetch tweets in batches continuously until manually stopped
            while True:
                try:
                    # Check if the internet connection is available
                    if not check_internet():
                        await wait_for_internet()

                    # Get the next batch of tweets
                    tweets = await get_tweets(user, tweets)
                    if tweets is None:
                        continue  # Skip if no tweets were fetched

                    # If no tweets are fetched in the current batch, increment the no_tweets_counter
                    if len(tweets) == 0:
                        no_tweets_counter += 1
                    else:
                        no_tweets_counter = 0  # Reset if tweets are fetched

                    # If no tweets were fetched for 3 consecutive attempts, treat it like rate limiting and wait
                    if no_tweets_counter >= 3:
                        print(f'{datetime.now()} - No tweets fetched for 3 consecutive attempts. Treating as rate limit hit.')
                        wait_time = 900  # Wait for 15 minutes (15 * 60 seconds)
                        print(f'{datetime.now()} - Waiting for {wait_time / 60} minutes...')
                        for remaining_time in range(wait_time, 0, -1):
                            mins, secs = divmod(remaining_time, 60)
                            print(f'{datetime.now()} - Waiting... {mins:02d}:{secs:02d} remaining', end='\r')
                            await asyncio.sleep(1)
                        print()  # Newline after countdown
                        no_tweets_counter = 0  # Reset the counter after waiting
                        continue  # Continue to the next iteration

                except Exception as e:
                    print(f'{datetime.now()} - Unexpected error while fetching tweets: {e}')
                    continue

                batch_saved_tweets = 0  # Count of saved tweets for the current batch
                for tweet in tweets:
                    try:
                        created_at = tweet._data['legacy'].get('created_at', 'N/A')
                        
                        # Convert the created_at to datetime object
                        if created_at != 'N/A':
                            tweet_date = datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
                        else:
                            tweet_date = None
                        
                        # Check if the tweet's created_at is before the threshold
                        if tweet_date and tweet_date < threshold_date:
                            print(f'{datetime.now()} - Tweet from {created_at} is earlier than the threshold date. Stopping script.')
                            return  # Stop the script if the tweet's date is earlier than the threshold

                        tweet_data = {
                            "Tweet ID": tweet._data['rest_id'],
                            "Tweet Content": tweet._data['legacy'].get('full_text', 'N/A'),
                            "Language": tweet._data['legacy'].get('lang', 'N/A'),
                            "Created At": created_at,
                            "Source": tweet._data['source'],
                            "Retweet Count": tweet._data['legacy'].get('retweet_count', 0),
                            "Like Count": tweet._data['legacy'].get('favorite_count', 0),
                            "Reply Count": tweet._data['legacy'].get('reply_count', 0),
                            "Quote Count": tweet._data['legacy'].get('quote_count', 0),
                            "View Count": tweet._data['views'].get('count', 0),
                            "Is Retweet": tweet._data['legacy'].get('is_quote_status', False),
                            "Possibly Sensitive": tweet._data['legacy'].get('possibly_sensitive', False),
                            "Media Available": 'yes' if 'media' in tweet._data['legacy']['entities'] else 'no',
                        }

                        # Increment count for saved tweets in the current batch
                        batch_saved_tweets += 1
                        total_saved_tweets += 1
                        tweets_saved_in_batch += 1

                        # Write the data to the CSV file
                        writer.writerow(tweet_data)

                        # If we've saved 900 tweets, take a 20-minute break
                        if tweets_saved_in_batch >= 900:
                            print(f'{datetime.now()} - Saved 900 tweets. Pausing for 20 minutes...')
                            await asyncio.sleep(1200)  # Wait for 20 minutes (1200 seconds)
                            tweets_saved_in_batch = 0  # Reset batch counter

                    except Exception as e:
                        print(f'{datetime.now()} - Error processing tweet {tweet._data["rest_id"]}: {e}')

                print(f'{datetime.now()} - Batch processed with {batch_saved_tweets} saved tweets')
                print(f'{datetime.now()} - Total tweets saved so far: {total_saved_tweets}')

    except Exception as e:
        print(f'{datetime.now()} - Error writing to CSV file: {e}')


async def main():
    client = Client(language='en-US')

    try:
        # Authenticate to the client
        await login_to_client(client)

        # Fetch tweets and save to CSV
        await fetch_and_print_tweets(client, userName)

    except Exception as e:
        print(f'{datetime.now()} - Error in main: {e}')


# Run the main async function
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print(f'{datetime.now()} - Script was interrupted by user. Exiting gracefully...')
except Exception as e:
    print(f'{datetime.now()} - Unexpected error occurred: {e}')
