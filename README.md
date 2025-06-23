# Summer-camp scripts

Collection of scripts, usually, generating SVG or PDF, for use in summer camp games for children.

## Setup

### Prerequsities
* Python 3.11+
* [poetry](https://python-poetry.org/)
* [make](https://www.gnu.org/software/make/)
* Google Cloud Application

Scripts are configured from a Google Sheet, meaning credentials for an Application that can read from Sheets are needed.
For more information see https://developers.google.com/sheets/api/quickstart/python#prerequisites.
By default, scripts expect secret in a file called `client_secret.json`

After acquiring the secret, you can run individual scripts like this
```bash
poetry install
SPREADSHEET=<ID> make <script_name>
```

## Scripts
Available scripts are:

* `munchkin` - Munchkin-inspired (but has actually very little common with Munchkin) tournament game
* `vampires` - Vampire puzzle game
* `program` - Creates program summary for the entire camp
   * Usage: `SPREADSHEET=<ID> DATE=<DATE> make summary`

## Windows instalation

* Run in Terminal/Powershell
  ```bash
  winget install python
  winget install Git.Git
  winget install -e --id GnuWin32.Make
  ```
* Restart terminal
  ```bash
  pip install poetry
  git clone https://github.com/pehala/Summercamp-scripts.git
  cd Summercamp-scripts
  poetry install
  SPREADSHEET=<ID> make <script_name>
  ```