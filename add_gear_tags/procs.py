# Procedures of script add-gear-tags.py
#
# Author: Haraldo Albergaria
# Date  : Sep 3, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import api_credentials
import json
import data

from common import getExif
from common import getCameraModel
from common import getLensModel

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

photoset_id = data.photoset_id
camera_tags = data.camera_tags
lens_tags = data.lens_tags


#===== PROCEDURES =======================================================#

### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, user_id):

    try:
        exif = getExif(photo_id, 0)
        camera = getCameraModel(exif).replace(' ', '')
        lens = getLensModel(exif).replace(' ', '')
        tags = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)['photo']['tags']['tag']

        current_tags = ''

        for tag in tags:
            current_tags = current_tags + ' \"' + tag['raw'] + '\"'

    except FlickrException as e:
        print("ERROR: Unable to retrieve EXIF data")
        print(e)
        return

    try:
        camera_tag = camera_tags[camera]
        lens_tag = lens_tags[lens]
        gear_tags = camera_tag + ' ' + lens_tag

    except Exception as e:
        print("ERROR: Unable to add tags")
        print("Key Error: {}".format(e))
        return

    new_tags = gear_tags + ' ' + current_tags
    flickr.photos.setTags(api_key=api_key, photo_id=photo_id, tags=new_tags)
    print("Added tags: {0}".format(gear_tags))
    print(' ')


