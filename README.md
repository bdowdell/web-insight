# web-insight
Checks for changes in a given URL website

## Contents

1. [Python Environment Set-Up](#python-environment-set-up)
1. [.env secrets set-up](#env-secrets-set-up)
1. [Set up cron job](#set-up-cron-job)

## Python Environment Set-Up

1. Create a Python 3.11.4 virtual environment
    * conda: `conda create -n web_insight python=3.11.4`
    * venv: ...
1. Install required packages: `pip install -r requirements.txt`

## .env secrets set-up

The .env file is not tracked by git, so any secrets placed inside are safe.

The .env file is used by the function `get_secrets` in `monitory.py` and
expects for each secret to be placed on an individual line, formatted as 
`KEY: value`. For example:

```
URL_TO_MONITOR: https://www.google.com
```

The following keys need to be specified:

* `URL_TO_MONITOR`
* ...


## Set up cron job

1. Create logging file
    * `sudo touch /var/log/web_monitor.log`
    * `sudo chown o+w /var/log/web_monitor.log`
1. Create cron job
    * Open crontab file for current user: `crontab -e`
    * Define environmental variables
        * `SHELL=/usr/bin/bash`
        * `PYTHON=/path/to/python`
        * `HOME=/path/to/code/dir`
    * Add the crontab command, for example: 

`22 */1 * * * $PYTHON $HOME/monitor.py >> /var/log/web_monitor.log 2>&1`

This will run at minute 22 past every hour, every day.

