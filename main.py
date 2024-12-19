import asyncio
import csv
from datetime import datetime
from random import randint
from twikit import Client, TooManyRequests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Set the username of the Twitter account
userName = 'JeffBezos'  # You can modify this for different users dynamically

# Helper function to fetch tweets asynchronously
async def get_tweets(user, tweets):
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

    except Exception as e:
        print(f'{datetime.now()} - Error in get_tweets: {e}')
        return None


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


async def fetch_and_print_tweets(client, userName):
    """Fetch tweets and print their data."""
    tweets = None
    total_saved_tweets = 0  # Variable to track total number of saved tweets

    try:
        # Fetch the user object by screen name
        user = await client.get_user_by_screen_name(userName)
    except Exception as e:
        print(f'{datetime.now()} - Error fetching user by screen name: {e}')
        return

    try:
        # Open CSV file in write mode
        with open('tweets_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "Tweet ID", "Tweet Content", "Language",
                "Created At", "Source", "Retweet Count",
                "Like Count", "Reply Count",
                "Quote Count", "View Count",
                "Is Retweet", "Possibly Sensitive",
                "Media Available"
            ])
            writer.writeheader()  # Write the header row to CSV

            # Fetch tweets in batches continuously until manually stopped
            while True:
                try:
                    # Get the next batch of tweets
                    tweets = await get_tweets(user, tweets)
                    if tweets is None:
                        continue  # Skip if no tweets were fetched

                except TooManyRequests as e:
                    # Handle rate limit by waiting until the reset time
                    rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                    print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
                    wait_time = rate_limit_reset - datetime.now()
                    await asyncio.sleep(wait_time.total_seconds())
                    continue

                except Exception as e:
                    print(f'{datetime.now()} - Unexpected error while fetching tweets: {e}')
                    continue

                batch_saved_tweets = 0  # Count of saved tweets for the current batch
                for tweet in tweets:
                    try:
                        tweet_data = {
                            "Tweet ID": tweet._data['rest_id'],
                            "Tweet Content": tweet._data['legacy'].get('full_text', 'N/A'),
                            "Language": tweet._data['legacy'].get('lang', 'N/A'),
                            "Created At": tweet._data['legacy'].get('created_at', 'N/A'),
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

                        # Write the data to the CSV file
                        writer.writerow(tweet_data)

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