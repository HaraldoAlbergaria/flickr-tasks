#!/usr/bin/python3

# This script generates a kml file of all the photos on
# user's photostream that can be imported on 'Google Earth'
# and/or 'Googlee My Maps'.
#
# Author: Haraldo Albergaria
# Date  : Nov 20, 2019
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

# Id of the photoset
# to generate kml file
photoset_id = '72157704077352525'
photoset_title = flickr.photosets.getInfo(user_id=user_id, photoset_id=photoset_id)['photoset']['title']['_content']


#===== MAIN CODE ==============================================================#

os.system('cp /home/pi/flickr_tasks/generate_kml/header.earth.kml /home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml')
os.system('cp /home/pi/flickr_tasks/generate_kml/header.mymaps.kml /home/pi/flickr_tasks/generate_kml/my_flickr_photos.mymaps.kml')

earth_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml", "a")
earth_file.write("    <Folder>\n        <name>{}</name>\n        <open>1</open>\n".format(photoset_title))
earth_file.close()

mymaps_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.mymaps.kml", "a")
mymaps_file.write("    <Folder>\n        <name>{}</name>\n        <open>1</open>\n".format(photoset_title))
mymaps_file.close()

photos = flickr.photosets.getPhotos(user_id=user_id, photoset_id=photoset_id)

npages = int(photos['photoset']['pages'])
ppage = int(photos['photoset']['perpage'])
total = int(photos['photoset']['total'])

print('=============================================')
print('Pages: {0} | Per page: {1} | Total: {2}'.format(npages, ppage, total))
print('=============================================')

for pg in range(1, npages+1):
    page = flickr.photosets.getPhotos(user_id=user_id, photoset_id=photoset_id, page=pg)
    ppage = len(page['photoset']['photo'])
    print('\n\n\nPage: {0}/{1} | Photos: {2}'.format(pg, npages, ppage))
    print('---------------------------------------------')

    for ph in range(0, ppage):
        photo_id = page['photoset']['photo'][ph]['id']
        photo_title = page['photoset']['photo'][ph]['title']
        print(u'\nid: {0}\ntitle: {1}'.format(photo_id, photo_title))
        set_id = procs.processPhoto(photo_id, photo_title, user_id, 0)

print('\n\n')

earth_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml", "a")
earth_file.write("    </Folder>\n</Document>\n</kml>\n")
earth_file.close()

mymaps_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.mymaps.kml", "a")
mymaps_file.write("    </Folder>\n</Document>\n</kml>\n")
mymaps_file.close()

