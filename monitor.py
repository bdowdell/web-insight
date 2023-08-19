#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 11:27:05 2023

@author: bendowdell

This program gets the HTML content from a specified web page, processes it by
stripping script and meta tags, hashes the result, and then compares the hash
to the previous hash saved to file. If the hashes are the same, no change has
occurred. If the hashes are different, then the web page has been updated. The
program is designed to run a single time at execution. The process is then
automated using a crontab file to check twice daily for updates.

Helpful resources:
1. (https://medium.com/swlh/tutorial-creating-a-webpage-monitor-using-python-
    and-running-it-on-a-raspberry-pi-df763c142dac)
2. (https://www.geeksforgeeks.org/python-script-to-monitor-website-changes/)
"""
import requests
import os
import hashlib
from bs4 import BeautifulSoup
import logging
import smtplib
import ssl
import email


def process_html(string):
    """
    Extract text out of tags using beautiful-soup.

    Specifically, it is possible that there are script and meta tags
    which always are different and as a result, the page contents are
    always different.

    Parameters
    ----------
    string : str
        string text from requests.get().text

    Returns
    -------
    string

    """
    # instantiate a BS4 object
    soup = BeautifulSoup(string, features="html.parser")

    # prettify
    soup.prettify()

    # remove script tags
    for tag in soup.select('script'):
        tag.extract()

    # remove meta tags
    for tag in soup.select('meta'):
        tag.extract()

    # convert to a string, remove '\r', and return
    return str(soup).replace('\r', '')


def get_secrets():
    """
    Read environmental secrets from .env file.
    
    Expects each line of .env to be of the form key: value
    ex: URL_TO_MONITOR: https://www.google.com

    Returns
    -------
    Dictionary
    """
    # instantiate an empty dictionary
    secrets_dict = {}

    # create a list to read env contents into
    secrets = []

    # read the secrets
    try:
        with open(".env", "r") as file:
            for line in file:
                secrets.append(line.strip())
    except:
        print("Could not find expected secrets file .env")

    # add the secrets to secrets_dict
    for secret in secrets:
        # split string on ': '
        split_secrets = secret.split(': ')
        key, value = split_secrets[0], split_secrets[1]
        secrets_dict[key] = value

    return secrets_dict    


def check_for_update(url_str):
    """
    Determine whether a webpage has been updated.
    
    Parameters
    ----------
    url_str : str
        string of web page url for monitoring

    Returns
    -------
    boolean
    """
    # headers
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    # get current html content
    response = requests.get(url_str, headers=headers)

    # create previous_hash.txt file if it doesn't exist
    if not os.path.exists("previous_hash.txt"):
        with open("previous_hash.txt", "w+") as file:
            file.close()

    # get the previous hash
    previous_hash = ''
    with open("previous_hash.txt", "r") as file:
        previous_hash = file.read()

    # process the response text and encode to utf-8
    processed_response_html = str(process_html(response.text)).encode('utf-8')

    # hash the current response
    current_hash = hashlib.sha224(processed_response_html).hexdigest()

    # compare previous with current
    if previous_hash == current_hash:
        return False
    else:
        with open("previous_hash.txt", "w") as file:
            file.write(current_hash)
        return True
    
    
def send_email(secrets):
    """
    Send email using environmental secrets.

    Parameters
    ----------
    secrets : dict
        Dictionary containing environmental secrets

    Returns
    -------
    None.
    """
    # get necessary secrets
    url = secrets["URL_TO_MONITOR"]
    port = secrets["PORT"]
    host = secrets["HOST"]
    sender = secrets["SENDER"]
    password = secrets["PASSWORD"]
    receiver = secrets["RECEIVER"]
    
    # set the message
    msg = email.message.Message()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'UPDATE DETECTED!!!'
    msg.add_header('Content-Type', 'text')
    message = f'A change in the webpage {url} has been detected.'
    msg.set_payload(message)
    
    # create a context
    context = ssl.create_default_context()
    
    # open connection and send email
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        # https://stackoverflow.com/a/58318206
        server.send_message(msg)


def main(secrets):
    """
    Define main program.
    
    Parameters
    ----------
    secrets : dict
        dictionary containing environmental secrets

    Returns
    -------
    None.

    """
    # instantiate logger
    log = logging.getLogger(__name__)
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO"),
        format='%(asctime)s %(message)s'
    )
    log.info("Running Website Monitor")

    # check for changes
    try:
        if check_for_update(secrets["URL_TO_MONITOR"]):
            log.info("WEBPAGE WAS CHANGED.")
            # alert user of change via email
            send_email(secrets)
        else:
            log.info("No update.")
    except:
        # potential network error
        log.info("Error checking website.")


if __name__ == "__main__":
    # get secrets from environmental .env file
    secrets = get_secrets()
    # TODO: check for existance of logging file and create if does not exist
    main(secrets)
