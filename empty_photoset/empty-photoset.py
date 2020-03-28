#!/usr/bin/python3

# This script emptys a photoset, leaving 1 photo to avoid
# the photoset being excluded.
#
# Author: Haraldo Albergaria
# Date  : Mar 27, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import flickrapi
import json
import api_credentials
import time

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== MAIN CODE ==============================================================#

photoset_id = input("Photoset ID: ")

try:
    photoset_name = flickr.photosets.getInfo(photoset_id=photoset_id)['photoset']['title']['_content']
except flickrapi.exceptions.FlickrError as e:
    print(e)
    quit()

empty = input("Empty photoset \'{}\'? (yes/no): ".format(photoset_name))

if empty == 'yes':
    try:
        photoset = flickr.photosets.getPhotos(photoset_id=photoset_id, user_id=user_id)
    except flickrapi.exceptions.FlickrError as e:
        print(e)
        quit()

    npages = int(photoset['photoset']['pages'])
    ppage = int(photoset['photoset']['perpage'])
    total = int(photoset['photoset']['total'])

    print("Emptying photoset \'{}\'...".format(photoset_name))

    photo_ids = ''
    is_first = True

    for pg in range(1, npages+1):
        page = flickr.photosets.getPhotos(photoset_id=photoset_id, user_id=user_id, page=pg)
        ppage = len(page['photoset']['photo'])
        for ph in range(0, ppage):
            photo_id = page['photoset']['photo'][ph]['id']
            if not is_first:
                photo_ids = photo_ids + photo_id + ','
            else:
                is_first = False

    try:
        flickr.photosets.removePhotos(api_key=api_key, photoset_id=photoset_id, photo_ids=photo_ids)
    except flickrapi.exceptions.FlickrError as e:
        print(e)
        quit()

    time.sleep(1)

    try:
        total = int(flickr.photosets.getPhotos(photoset_id=photoset_id, user_id=user_id)['photoset']['total'])
    except flickrapi.exceptions.FlickrError as e:
        print(e)
        if str(e) == "Error: 1: Photoset not found":
            print("Something not functioned properly, the album has been excluded. :-(")
        quit()

    if total > 1:
        print("Unable to empty photoset. {} photos have been left.".format(total))
        quit()

    print("Photoset successfully emptied! 1 photo has been left to avoid photoset being excluded.")

