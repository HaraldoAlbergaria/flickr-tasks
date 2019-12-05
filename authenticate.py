#!/usr/bin/python3

#########################################################################################
## This code was extracted and modified from the following address:                    ##
## https://stuvel.eu/flickrapi-doc/3-auth.html#authenticating-without-local-web-server ##
#########################################################################################

import flickrapi
import api_credentials
import os
import webbrowser

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

flickr = flickrapi.FlickrAPI(api_key, api_secret)

runlevel = os.system('runlevel')

print('Authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='write'):

    print('Not have a valid token')

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms='write')
    if  runlevel == 'N 5':
        webbrowser.open_new_tab(authorize_url)
    else:
        print("Authorization URL: {}".format(authorize_url))

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = str(input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)

