# web-insight
Checks for changes in a given URL website

## Contents

1. [Python Environment Set-Up](#python-environment-set-up)
1. [.env secrets set-up](#env-secrets-set-up)
1. [Set up cron job](#set-up-cron-job)

## Python Environment Set-Up

### Option 1: pyenv + venv + pip (preferred)

The following instructions for setting up a virtual environment assume you are using Linux (or Windows Subsystem for Linux 2), and specifically, Ubuntu 20.04.6 LTS. The overall sequence of steps are:

1. Install and set-up `pyenv` for managing different python versions
2. Clone the `web-insight` repository
3. Set-up a new virtual environment using `venv`
4. Install required packages using `pip` and the `requirements.txt` file

**Note**: Prior to installing anything, ensure your Ubuntu is up-to-date. Open a terminal and:

```
$ sudo apt update
$ sudo apt upgrade
```

*The following steps are all completed from within a terminal*

#### Step 1: Install and set-up `pyenv`

For full details, please refer to the `pyenv` [github repository](https://github.com/pyenv/pyenv#getting-pyenv). The steps are as follows:

1. Ensure you are in your home directory: `$ cd`
2. Clone the `pyenv` repository: `$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv`
3. Set up your shell for Pyenv:
    * `$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc`
    * `$ echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc`
    * `$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc`
4. Repeat the above for `.profile`:
    * `$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile`
    * `$ echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile`
    * `$ echo 'eval "$(pyenv init -)"' >> ~/.profile`
5. Restart the shell: `$ exec "$SHELL"`
6. Install necessary Python build dependencies:

```
$ sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```
7. Install python version 3.11.4: `$ pyenv install 3.11.4`

*Note*: This will take a few minutes. Be patient, the process is not hung. 

#### Step 2: Clone the repository

1. `$ git clone https://github.com/bdowdell/web-insight.git`


#### Step 3: Set-up `venv`

1. Change into the cloned repository: `$ cd web-insight`
2. Set the local python version: `$ pyenv local 3.11.4` $\leftarrow$ includes `venv` so we don't need to install first
3. Confirm the change: `$ python --version`
4. Create a virtual environment: `python -m venv .venv`
5. Activate the virtual environment: `$ source .venv/bin/activate`
6. When you are done working, *remember to deactivate the environment*: `$ deactivate`

#### Step 4: Install required packages

1. Update pip: `$ pip install pip update`
1. With the virtual environment active: `$ pip install -r requirements.txt`

*Note*: This will take a few minutes.

Your environment is now ready.


### Option 2: conda

This method requires installing either Anaconda or Miniconda. This method
is less preferred because the environment is open to other projects and
is not self-contained.

1. Create a Python 3.11.4 virtual environment: `conda create -n web_insight python=3.11.4`
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
* `PORT`
* `HOST`
* `SENDER`
* `PASSWORD`
* `RECEIVER`

As an example, `.env` should appear as follows:

```
URL_TO_MONITOR: https://www.rice.edu
PORT: 465
HOST: smtp.gmail.com
SENDER: my_dev_email@gmail.com
PASSWORD: 12345dogdog
RECIEVER: my_personal_email@gmail.com
```


## Set up cron job

1. Create cron job.
    * Open crontab file for current user: `crontab -e`
    * Define environmental variables
        * If using `pyenv` + `venv`
            * `SHELL=/usr/bin/bash`
            * `HOME=/home/username`
            * `CODE=/path/to/code/dir`
        * If using `conda`
            * `SHELL=/usr/bin/bash`
            * `HOME=/home/username`
            * `PYTHON=/home/username/anaconda3/envs/web-insight/python`
            * `CODE=/path/to/code/dir`
    * Add the crontab command, for example: 
        * `pyenv` + `venv`:
            * `22 */1 * * * $CODE/.venv/bin/python $CODE/monitor.py`
        * `conda`:
            * `22 */1 * * * $PYTHON $CODE/monitor.py`

This will run at minute 22 past every hour, every day.

