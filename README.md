# web-insight
Checks for changes in a given URL website

## Contents

1. [Environment Set-Up](#environment-set-up)
1. ...

## Environment Set-Up

1. Create a Python 3.11.4 virtual environment
    * conda: `conda create -n web_insight python=3.11.4`
    * venv: ...
1. Install required packages: `pip install -r requirements.txt`
1. Create logging file
    * `sudo touch /var/log/web_monitor.log`
    * `sudo chown o+w /var/log/web_monitor.log`
1. Create cron job
    * Open crontab file for current user: `crontab -e`
    * Define environmental variables
        * `SHELL=/usr/bin/bash`
        * `PYTHON=/path/to/python`
        * `HOME=/path/to/code/dir`
    * Add the crontab command: 

`22 */1 * * * $PYTHON $HOME/monitor.py >> /var/log/web_monitor.log 2>&1`

This will run at minute 22 past every hour, every day.

