# Slack Image Downloader

Takes an channel and downloads all images from it for the last x days provided

## Docker

Build the image
```bash
docker build . -t slack-downloader
```

## Run the image

Run the container
```bash
docker run --rm  \
    -v $PWD/images:/app/images \
    -e SLACK_TOKEN=xxxxxxxxx \
    -e DAYS=365 \
    -e WRITE_DIR=images/ \
    slack-downloader
```

## Environment

There is a couple of env variables that are available for configuration

* **SLACK_TOKEN** - The authorization token is that will be used to make the api requests 
* **DAYS**[default:365] - Number of days back to search for images
* **WRITE_DIR**[default:images/] - The directory to write to
* **SLACK_BASE_URL**[default:https://slack.com/api] - The api for slack
