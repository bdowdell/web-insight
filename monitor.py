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


URL_TO_MONITOR = "https://commencement.rice.edu/"


def process_html(string):
    """
    Extract text out of tags using beautiful-soup.

    Specifically, it is possible that there are script and meta tags
    which always are different and as a result, the page contents are
    always different.

    Parameters
    ----------
    string : TYPE
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


def check_for_update():
    """
    Determine whether a webpage has been updated.

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
    response = requests.get(URL_TO_MONITOR, headers=headers)

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


def main():
    """
    Define main program.

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
        if check_for_update():
            log.info("WEBPAGE WAS CHANGED.")
        else:
            log.info("No update.")
    except:
        # potential network error
        log.info("Error checking website.")


if __name__ == "__main__":
    main()
