#!/usr/bin/python3

# This script executes tasks in all photos on a photostrean
# according to rules defined by the user. Can be used to add
# tags or add photos to groups according to views, favorites, etc.,
# for example.
#
# Author: Haraldo Albergaria
# Date  : Jul 17, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


####################################################
# !!!DO NOT MODIFY THIS FILE!!!                    #
# Implement the procedures in file procs.py        #
####################################################


import flickrapi
import json
import api_credentials
import procs
import os

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== MAIN CODE ==============================================================#

os.system('cp /home/pi/flickr_tasks/generate_kml/header.kml /home/pi/flickr_tasks/generate_kml/my_flickr_photos.kml')

photos = flickr.people.getPhotos(user_id=user_id)

npages = int(photos['photos']['pages'])
ppage = int(photos['photos']['perpage'])
total = int(photos['photos']['total'])

print('=============================================')
print('Pages: {0} | Per page: {1} | Total: {2}'.format(npages, ppage, total))
print('=============================================')

for pg in range(1, npages+1):
    page = flickr.people.getPhotos(user_id=user_id, page=pg)
    if pg == npages:
        pp = (npages - 1) * ppage
        ppage = total - pp
    print('\n\n\nPage: {0}/{1} | Photos: {2}'.format(pg, npages, ppage))
    print('---------------------------------------------')

    for ph in range(0, ppage):
        photo_id = page['photos']['photo'][ph]['id']
        photo_title = page['photos']['photo'][ph]['title']
        print(u'\nid: {0}\ntitle: {1}'.format(photo_id, photo_title))
        set_id = procs.processPhoto(photo_id, photo_title, user_id)

print('\n\n')

output = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.kml", "a")
output.write("    </Folder>\n</Document>\n</kml>\n")
output.close()

