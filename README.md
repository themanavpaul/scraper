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

<br>

## **Installation:**

1. Install required packages using pip:

   ```bash
   pip install python-dotenv requests twikit

2. Create a ```.env``` file (optional) and add your Twitter API credentials:
  
   ```bash
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

<br>

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

---

<br>

# Dataset Sentiment Analysis

Your Dataset Created : [Twitter_Dataset.csv](https://github.com/themanavpaul/scraper/blob/main/combined_csv.csv)
Here is the Jupyter Notebook with all the commands and techniques : [ScrapeX_Sentiment_Analysis.ipynb](https://github.com/themanavpaul/scraper/blob/main/Tweets_analysis.ipynb)

## Step1 :  **Data Pre-Processing**

**1. Introduction**

* **Project Overview:** Briefly describe the purpose of cleaning the scraped Twitter data and the intended use of the cleaned dataset (e.g., sentiment analysis, topic modeling).
* **Data Source:** Specify how the Twitter data was obtained (e.g., Twitter API, web scraping).
* **Data Description:** Provide a high-level overview of the raw data, including:
    - Number of tweets.
    - Data fields present (e.g., tweet content, source, timestamp).
    - Data format (e.g., CSV, JSON).
    - Any initial observations about the data quality (e.g., missing values, duplicates, inconsistencies).

**2. Data Loading and Exploration**

* **Loading the Data:** Describe the steps involved in loading the Twitter data into your Jupyter Notebook environment. Mention the libraries used (e.g., pandas).
* **Initial Exploration:** Summarize key characteristics of the dataset using techniques like:
    - `df.head()` and `df.tail()` to view the first and last few rows.
    - `df.info()` to get data type information and check for missing values.
    - `df.describe()` to get summary statistics for numerical columns (if applicable).
    - Visualizations (histograms, scatter plots) to understand data distributions and relationships (if relevant).

**3. Data Cleaning Steps**

* **Handling Missing Values:**
    - Identify columns with missing values.
    - Explain the chosen strategy for handling missing data (e.g., deletion, imputation, leaving as is).
    - Justify your approach based on the data and analysis goals.
* **Removing Duplicates:**
    - Describe the criteria used to identify duplicate tweets (e.g., exact content matches, duplicates based on specific fields).
    - Explain the method used to remove duplicates (e.g., `df.drop_duplicates()`).
* **Data Transformation and Feature Engineering (if applicable):**
    - Describe any transformations applied to the data, including:
        - Data type conversions (e.g., converting strings to dates).
        - Feature engineering (creating new features based on existing ones).
    - Provide justification for each transformation.
* **Text Preprocessing (if applicable):**
    - If dealing with textual data (tweet content), describe the text cleaning techniques used:
        - Removing punctuation, stop words, URLs, mentions.
        - Tokenization (splitting text into words).
        - Stemming/lemmatization (reducing words to their base form).
    - Explain the rationale behind each preprocessing step.

**4. Data Validation and Quality Checks**

* **Data Consistency Checks:**
    - Describe how you ensured data integrity (e.g., verifying data ranges, checking for inconsistencies between related columns).
* **Data Quality Assessment (optional):**
    - Discuss any metrics used to evaluate the quality of the cleaned data (e.g., data completeness, accuracy, consistency).

**5. Saving the Cleaned Data**

* Describe how you saved the cleaned dataset (e.g., CSV, pickle file).
* Specify the file path and name.

**6. Conclusion**

* Briefly summarize the key steps involved in cleaning the Twitter data.
* Acknowledge any limitations of the cleaning process (e.g., assumptions made, data quality issues that remain).
* Discuss potential future improvements or extensions to the cleaning process.

**7. Appendix (Optional)**

* Include any supporting materials (e.g., code snippets, visualizations, detailed explanations of specific techniques).

**Additional Considerations:**

* **Clarity and Conciseness:** Use clear and concise language throughout the documentation.
* **Reproducibility:** Provide enough detail to allow others to reproduce your cleaning steps.
* **Code Comments:** Include comments within your code to explain the purpose of each step.
* **Version Control:** Consider using version control (e.g., Git) to track changes to your code and documentation.

By following this structured outline and incorporating the above considerations, you can create a comprehensive and informative documentation for your Twitter data cleaning project in your Jupyter Notebook.

---

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

