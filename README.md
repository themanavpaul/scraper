# ScraperX : Twitter Tweet Scraper

This Python script fetches tweets from a specified Twitter user, extracts relevant data, and saves it to a CSV file.

## **Features:**

* Fetches tweets from a given Twitter user.
* Handles Twitter API rate limits with retries and exponential backoff.
* Monitors internet connectivity and resumes scraping upon reconnection.
* Saves tweet data to a CSV file with relevant fields.
* Includes a threshold date to stop scraping older tweets.
* Handles potential errors and exceptions gracefully.

## **Possible Use Cases (Illustrative):**

* **Data Analysis:** 
    * Analyze tweet sentiment over time.
    * Study the frequency of keywords or hashtags used by a specific user.
    * Identify trends in the user's tweeting behavior.
* **Research:** 
    * Collect data for research projects related to social media, linguistics, or political science.
* **Learning:** 
    * Understand web scraping techniques and Python programming concepts.
    * Explore data handling and manipulation with Python libraries (e.g., `pandas`).

## **Dependencies:**

* `asyncio`
* `csv`
* `datetime`
* `dotenv`
* `requests`
* `twikit`

# ScraperX with Virtual Environment Setup

This guide outlines the steps to set up a virtual environment, install dependencies, and run the Python script for fetching tweets from a specified Twitter user.

**Prerequisites:**

* Any operating system (We used Ubuntu)
* Basic understanding of terminal commands

## **Steps:**

1. **Update package lists:**

   ```bash
   sudo apt update
   ```
   This command refreshes the list of available packages from the Ubuntu repositories.

2. **Upgrade existing packages:**

   ```Bash
   sudo apt upgrade
   ```
   This command upgrades any outdated packages on your system to ensure you have the latest versions.

3. Install `python3-pip` (if not already installed):

   ```Bash
      sudo apt install python3-pip
   ```
   
   This command installs the pip package manager for Python 3, which is necessary for installing Python libraries.

4. Install python3-venv (if not already installed):

   ```Bash
      sudo apt-get install python3-venv
   ```
   
      This command installs the venv module, which is used to create virtual environments for Python projects.

5. **Create a virtual environment:**

   ```Bash
   python3 -m venv my_env_project
   ```
   
   Replace my_env_project with your desired virtual environment name. This command creates a virtual environment directory named my_env_project in your current working directory.

6. **Activate the virtual environment:**

   ```Bash
   source my_env_project/bin/activate
   ```
   
   This command activates the virtual environment. You'll see the name of the virtual environment prepended to your terminal prompt, indicating that you're now working within the isolated environment.

7. **Verify environment activation (optional):**

   ```Bash
   python
   ```
   
   This command (without arguments) will typically display the Python version within the virtual environment. If you see the correct Python 3 version, you've successfully activated the environment.

---

## **Installation:**

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

## **Script Functionality:**

- **Fetches tweets:** Retrieves tweets from the specified Twitter user in batches.
- Handles rate limits: Implements mechanisms to handle Twitter API rate limits, including exponential backoff and retries.
- **Checks internet connection:** Monitors the internet connection and waits for reconnection if it's lost.
- **Stores data in CSV:** Saves fetched tweets to a CSV file with relevant information (tweet ID, content, created at, etc.).
- **Threshold date:** Allows you to specify a threshold date. The script will stop fetching tweets if it encounters tweets older than the threshold.
- **Error handling:** Includes basic error handling for various exceptions.



**Disclaimer:**

This script is provided for **educational and experimental purposes only**.
Use this script responsibly as it does **not** utilize the official Twitter API and may become **deprecated** in the future due to potential changes in Twitter's website structure or data availability. 
The author is not responsible for any misuse or consequences of using this script.
Use this script with caution and at your own risk.

## License

This project is licensed under the [**MIT License**](https://opensource.org/licenses/MIT).

**Copyright (c) Manav Paul 2024**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
THE SOFTWARE.

