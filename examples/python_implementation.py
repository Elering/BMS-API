#-------------------------------------------------------------------------------
# Name:        POST data to BMS
# Purpose:     Example how to send data to Elering BMS with POST
#
# Author:      kristjan.vilgo
#
# Created:     26.10.2017
# Copyright:   (c) kristjan.vilgo 2017
# Licence:     <your licence>
# Supported python versions:       2.7, 3.X
#-------------------------------------------------------------------------------
from __future__ import print_function

import requests
import os

from tkFileDialog import askopenfilenames
from Tkinter import Tk

# --- Settings ---

username = "replace"
password = "replace"


token_url = "replace"
post_url = "replace"

root_cert_present = True
##root_cert_present = False # For testing purposes, to be used if testing system does not have correct root cert for endpoint


# --- Functions ---


def check_path(list_of_paths):
    """Tests if path/file exsists, returns true/false"""
    for path in list_of_paths:

        print (path)
        check=os.path.exists(path)
        print ("Path exsits: {}".format(check))

        return check

def select_files(file_type='.*' ,dialogue_title="Select file(s)"):
    """ Multiple files selection popup
    return: list"""

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filenames = askopenfilenames(title=dialogue_title, filetypes=[('{} file'.format(file_type),'*{}'.format(file_type))]) # show an "Open" dialog box and return the paths to selected files

    return filenames

# --- Process start ---


# Create list of files to be uploaded

files = select_files()


# Get security token

token_headers = {"Content-Type" : "application/x-www-form-urlencoded"}

token_message_body = "grant_type=password&scope=global&username={}&password={}".format(username, password)

token_data = requests.post(token_url, data=token_message_body, headers=token_headers, verify=root_cert_present) # --- POST to get TOKEN ---

#print (token_data.content) #DEBUG

try:

    access_token = eval(token_data.content).get("access_token", "") #Tries to get token from response, if no token is found returns empty string
    token_type = eval(token_data.content).get("token_type", "") #Tries to get token type from response, if no token is found returns empty string

except SyntaxError:
    access_token = ""
    print ("Evaluation of return message for token failed")


# Start sending data

if access_token != "":

    content_type_dic = {"xml":'application/xml', "xls":'application/vnd.ms-excel', "xlsx":'application/zip', "txt":'text/plain'}

    for file_path in files:

        if check_path([file_path]) == True :

            file_extension = file_path.split(".")[-1]

            if file_extension in content_type_dic:

                file = open(file_path, 'rb')

                headers={"Content-Type" : content_type_dic[file_extension],
                         "Authorization": "{} {}".format(token_type, access_token)}

                r = requests.post(post_url, data=file, headers=headers, verify=root_cert_present) # --- POST to send DATA ---

                print (r.text)


            else:
                print ("Filetype not defined {}".format(file_extension))

else:
    print("ERROR - Token is empty; Process stopped; Response from server: {}".format(token_data.content))
