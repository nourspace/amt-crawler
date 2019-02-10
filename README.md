# amt-crawler

Checks service.berlin.de for bookable appointments and notifies you on Slack. 

## Setup

```
pipenv install
```

## Usage

```
python crawl.py SERVICE_URL
```

### With Docker Compose

Rename `docker-compose.example.yml` to `docker-compose.yml` and replace the environment variables

```
docker-compose up
```

## Notifications

### Google Spreadsheet
`GOOGLE_SERVICE_ACCOUNT_CREDS` env var with the credentials of a service account whose email has access to a worksheet (default: `Amt Crawls`) 

### Slack
`SLACK_API_TOKEN` env var with Slack API token that allows posting to a channel (default: `#amt-crawls`)
