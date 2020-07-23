#!/usr/bin/python3

# This script generates a kml file of all the photos on the
# user's photostream, that can be imported on 'Google Earth'
# and/or 'Googlee My Maps'.
#
# Author: Haraldo Albergaria
# Date  : Mar 26, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


####################################################
# !!!DO NOT MODIFY THIS FILE!!!                    #
# Implement the procedures in file procs.py        #
####################################################


import flickrapi
import json
import api_credentials
import procs
import config
import os

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
photoset_title = flickr.photosets.getInfo(user_id=user_id, photoset_id=config.photoset_id)['photoset']['title']['_content']
photos_per_page = '500'

#===== MAIN CODE ==============================================================#

os.system('cp /home/pi/flickr_tasks/generate_kml/header.earth.kml /home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml')
os.system('cp /home/pi/flickr_tasks/generate_kml/header.mymaps.kml /home/pi/flickr_tasks/generate_kml/my_flickr_photos.mymaps.kml')

earth_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml", "a")
earth_file.write("    <Folder>\n        <name>My Photostream</name>\n        <open>1</open>\n")
earth_file.close()

mymaps_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.mymaps.kml", "a")
mymaps_file.write("    <Folder>\n        <name>My Photostream</name>\n        <open>1</open>\n")
mymaps_file.close()

photos = flickr.photosets.getPhotos(api_key=api_key, user_id=user_id, photoset_id=config.photoset_id, privacy_filter='1', per_page=photos_per_page)
photos_base_url = flickr.people.getInfo(api_key=api_key, user_id=user_id)['person']['photosurl']['_content']

npages = int(photos['photoset']['pages'])
ppage = int(photos['photoset']['perpage'])
total = int(photos['photoset']['total'])

print('=============================================')
print('Pages: {0} | Per page: {1} | Total: {2}'.format(npages, ppage, total))
print('=============================================')

for pg in range(1, npages+1):
    page = flickr.photosets.getPhotos(api_key=api_key, user_id=user_id, photoset_id=config.photoset_id, privacy_filter='1', extras='geo,tags', page=pg, per_page=ppage)['photoset']['photo']
    ppage = len(page)
    print('\n\n\nPage: {0}/{1} | Photos: {2}'.format(pg, npages, ppage))
    print('---------------------------------------------')

    for ph in range(0, ppage):
        procs.processPhoto(page[ph], photos_base_url, user_id, 0)

print('\n\n')

earth_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml", "a")
earth_file.write("    </Folder>\n</Document>\n</kml>\n")
earth_file.close()

mymaps_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.mymaps.kml", "a")
mymaps_file.write("    </Folder>\n</Document>\n</kml>\n")
mymaps_file.close()

