# UGAHacks-sponsor-Emailer

Email automation for cold emails

## Documentation for Automatic Emailer Project

This project is designed to automatically email potential sponsors for events by scraping data, cleaning it, and then using that data to send personalized emails. The project consists of two main Python files:

- **clean.py**: Processes data to identify new entries.
- **main.py**: Uses processed data to send emails through a Gmail account.

### Prerequisites

- Python 3.x
- pip
- Access to the internet
- A Google account with the Gmail API enabled(Sponsor Team should ask me to add them)

### Installation

1. **Clone the repository or download the project files to your local machine.**

2. **Install required Python libraries:**
   Navigate to the project directory in your terminal and run the following command to install dependencies from the `requirements.txt` file:
   `pip install -r requirements.txt`

3. **Set up Google API credentials:(Skip if part of sponsorship team and ask me for secrets file)**
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Gmail API under “APIs & Services > Library”.
   - Create credentials:
     - Choose “OAuth client ID”.
     - Application type should be “Web application”.
     - Add a redirect URI of `http://localhost:8080/`.
   - Download the JSON file and rename it to `client_secrets.json`. Place this file in your project directory.

### File Setup

Ensure the following files are in the correct directories:

- **check.csv**: Should exist in `data/check.csv`.
- **batch.csv**: Will be generated in `data/batch.csv`.
- **client_secrets.json**: Should be placed in the project root directory.

### Configuration

Customize the behavior of the scripts by modifying the constants in `main.py`:

- **SENDER_EMAIL**: Set this to the Gmail address you will use to send emails.
- **CC_EMAILS**: Add any constant CC addresses here, separated by commas.
- **EMAIL_TEMPLATE**: Modify this HTML template to personalize the content of the emails sent out.

Customize the filename of the csv you are using in clean.py

### Running the Scripts

1. **Scrape emails from apollo**
   make ure you have the following extention installed https://apolloexporter.scrapejob.net/
   On apollo enter search criteria and hit the extension's button on the bar above the search results
   - If you are not seeing it, try enabling the extension to run in incognito and try in an anonymous browser.
2. **Process new data entries**:
   Run `clean.py` to update `data/batch.csv` with new entries:
   `python clean.py`

3. **Send emails**:
   Execute `main.py` to send emails to the updated list:
   `python main.py`

### Notes

- check.csv will version itself
- Review the entries in batch.csv before you send emails and note that the company names will be shown in the email
- Remember to regularly backup your `check.csv` to avoid accidental loss of data.
- The email sending function includes a delay of 5 seconds between emails to avoid spam filters.

### Conclusion

This documentation covers the setup and use of the Automatic Emailer project. Ensure you follow the steps carefully and customize the scripts as needed for your specific requirements.

Please contact me with any questions/suggestions
