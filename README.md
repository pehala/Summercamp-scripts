# Summer-camp scripts

Collection of scripts, usually, generating SVG or PDF, for use in summer camp games for children.
Output

## Setup

### Prerequsities
* Python 3.11+
* [poetry](https://python-poetry.org/)
* [make](https://www.gnu.org/software/make/)
* Google Cloud Application

Scripts are configured from a Google Sheet, meaning credentials for an Application that can read from Sheets are needed.
For more information see https://developers.google.com/sheets/api/quickstart/python#prerequisites.
By default, scripts expect secret in a file called `client_secrets.json`

After acquiring the secret, you can run individual scripts like this
```bash
poetry install
SPREADSHEET=<ID> make <game_name>
```

## Games

Available scripts are:
`munchkin` - Munchkin-inspired (but has actually very little common with Munchkin) tournament game
`vampires` - Vampire puzzle game