# What does this script do?

This is a command line Python script, which retrieves the information of a GitHub User and creates a new Contact or updates an existing contact in Freshdesk, using their respective APIs.

# Prerequisites

- You will need Python 3.0+ to run the script. See here: https://www.python.org/downloads/
- You will need to add Python and pip to the Path environment variable, so you will be able to run `python` and `pip` from the command line
- You will need to add the following environment variables:<br/>
  **_GITHUB_TOKEN_** - GitHub personal access token for authentication in the GitHub REST API<br/>
  For more info: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token <br/>
  **_FRESHDESK_TOKEN_** - Freshdesk API key for authentication in the Freshdesk REST API<br/>
  For more info: https://support.freshdesk.com/support/solutions/articles/215517-how-to-find-your-api-key

# Installing libraries and dependencies

- Depending on what OS you are working on, run CMD (Windows) or shell (Linux) in the root directory of the script and type the following command:<br/>
`pip install -r requirements.txt` <br/>
  This will install the libraries that are needed in order the script to work properly.

# Running the script

- Depending on what OS you are working on, run CMD (Windows) or shell (Linux) in the root directory of the script and type the following command:<br/>
`python main.py --username <github_username> --subdomain <freshdesk_subdomain>` <br/>
  where:
  - _<github_username>_ is the GitHub username which you want to migrate to a Freshdesk contact
  - _<freshdesk_subdomain>_ is your subdomain in Freshdesk where the GitHub users will be migrated

# Running the unit tests

Depending on what OS you are working on, run CMD (Windows) or shell (Linux) in the root directory of the script and type the following command:<br/>
`python -m unittest` <br/>
This will start all the unit tests that are found.

# Examples
- How to find GitHub usernames to test the script?<br/>
  Here is a link where you can find the most active GitHub users:<br/>
  https://gist.github.com/paulmillr/2657075