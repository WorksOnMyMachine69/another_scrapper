# Another Scraper Bot!

![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

## How to Use

### 1. Set Up a Virtual Environment and Install Dependencies

#### On **Windows** (tested with VS Code and Microsoft Edge):

```
> python -m venv .venv
> .venv\Scripts\activate
> pip install -r reqs.txt
````

#### On **UNIX/Linux/macOS**:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r reqs.txt
```


### 2. Configure Your Credentials

File up the credentials in the `creds.py` file.

> **Note:** Security answers must be entered exactly as they appear on the original site (case-sensitive and format-sensitive).


### 3. Run the Script

Ensure your virtual environment is activated, then execute:

```bash
> python main.py
```

> **Note:** You may safely ignore any warnings during execution.


### 4. Enter OTP

When prompted, **enter the OTP in the terminal**, not in the browser window.


### 5. Don't panic


## Privacy Notice

* The scraped files **do NOT contain any personal information**.
* Feel free to regex search over files in the `extract/` directory.
* Source code is fully open for review and audit.


## Output Details

* On successful scraping:

  * Two `.html` files with tables for both profile and notices will be created in the current directory.
  * A folder named `extract/` will be generated, containing all extracted files along with CSV versions of the tables for analysis

> Only the two `.html` files along with `extract/` directory holds all extracted data in a user readable format.

> **Tip:** Run the scraper at night for reduced server traffic.

## Contribution & Maintenance

Any modification for better functionability and maintainence of the tool is high appreciated and welcomed.


## Final Words
Use it responsibly!