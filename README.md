# Twitter Tweet Scraper

This Python script fetches tweets from a specified Twitter user, extracts relevant data, and saves it to a CSV file.

**Features:**

* Fetches tweets from a given Twitter user.
* Handles Twitter API rate limits with retries and exponential backoff.
* Monitors internet connectivity and resumes scraping upon reconnection.
* Saves tweet data to a CSV file with relevant fields.
* Includes a threshold date to stop scraping older tweets.
* Handles potential errors and exceptions gracefully.

**Dependencies:**

* `asyncio`
* `csv`
* `datetime`
* `dotenv`
* `requests`
* `twikit`

**Installation:**

1. Install required packages using pip:

   ```bash
   pip install python-dotenv requests twikit

2. Create a ```.env``` file (optional) and add your Twitter API credentials:
  ```
  USER_NAME=<your_twitter_username>
  E-MAIL=<your_email>
  PASS_WORD=<your_password>
  ```
  Note: This step is optional. If you don't use a .env file, you'll need to modify the login_to_client function to directly handle the authentication.
  
3. Usage:

  - Save the script: Save the provided code as `main.py`.

  - Run the script:

    ```Bash
    python main.py
    ```
---

**Script Functionality:**

Fetches tweets: Retrieves tweets from the specified Twitter user in batches.
Handles rate limits: Implements mechanisms to handle Twitter API rate limits, including exponential backoff and retries.
Checks internet connection: Monitors the internet connection and waits for reconnection if it's lost.
Stores data in CSV: Saves fetched tweets to a CSV file with relevant information (tweet ID, content, created at, etc.).
Threshold date: Allows you to specify a threshold date. The script will stop fetching tweets if it encounters tweets older than the threshold.
Error handling: Includes basic error handling for various exceptions.

**Note:**

This script uses Twitter API v1.1, which has limitations on the number of requests you can make per user. Consider the rate limits and potential consequences of using this script extensively.
You might need to adjust some aspects of the script depending on your specific needs and Twitter API usage guidelines.

**Disclaimer:**

This script is provided for educational and experimental purposes only.
Use this script responsibly and within the terms of service of the Twitter API.
The author is not responsible for any misuse or consequences of using this script.
