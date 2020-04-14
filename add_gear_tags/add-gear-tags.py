#!/usr/bin/python3

# This script executes tasks in all photos on a photostrean
# according to rules defined by the user. Can be used to add
# tags or add photos to groups according to views, favorites, etc.,
# for example.
#
# Author: Haraldo Albergaria
# Date  : Sep 3, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


####################################################
# !!!DO NOT MODIFY THIS FILE!!!                    #
# Implement the procedures in file procs.py        #
####################################################


import flickrapi
import api_credentials
import json
import procs
import data

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== MAIN CODE ==============================================================#

photoset_id = data.photoset_id

photoset = flickr.photosets.getPhotos(photoset_id=photoset_id, user_id=user_id)

npages = int(photoset['photoset']['pages'])
ppage = int(photoset['photoset']['perpage'])
total = int(photoset['photoset']['total'])

print('=============================================')
print('Pages: {0} | Per page: {1} | Total: {2}'.format(npages, ppage, total))
print('=============================================')

for pg in range(1, npages+1):
    page = flickr.photosets.getPhotos(photoset_id=photoset_id, user_id=user_id, page=pg)
    ppage = len(page['photoset']['photo'])
    print('\n\n\nPage: {0}/{1} | Photos: {2}'.format(pg, npages, ppage))
    print('---------------------------------------------')

    for ph in range(0, ppage):
        photo_id = page['photoset']['photo'][ph]['id']
        photo_title = page['photoset']['photo'][ph]['title']
        print(u'\nid: {0}\ntitle: {1}'.format(photo_id, photo_title))
        procs.processPhoto(photo_id, user_id)

print('\n\n')
