# Procedures of script process-photos.py
#
# Author: Haraldo Albergaria
# Date  : Sep 3, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import json
import api_credentials
import data

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

photoset_id = data.photoset_id
camera_tags = data.camera_tags
lens_tags = data.lens_tags


#===== PROCEDURES =======================================================#

def getExif(photo_id):
    try:
        exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
        if len(exif) == 0:
            retry = 0
            while len(exif) == 0 and retry < 10:
                time.sleep(1)
                exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
                retry = retry + 1
    except:
        try:
            exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
            if len(exif) == 0:
                retry = 0
                while len(exif) == 0 and retry < 10:
                    time.sleep(1)
                    exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
                    retry = retry + 1
        except:
            exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
    return exif

def getCameraModel(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "Model":
            return exif[i]['raw']['_content']
    return ''

def getLensModel(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "LensModel":
            return exif[i]['raw']['_content']
    return ''



### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, user_id):
    exif = getExif(photo_id)
    camera = getCameraModel(exif).replace(' ', '')
    lens = getLensModel(exif).replace(' ', '')
    tags = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)['photo']['tags']['tag']

    current_tags = ''

    for tag in tags:
        current_tags = current_tags + ' ' + tag['raw']

    camera_tag = camera_tags[camera]
    lens_tag = lens_tags[lens]
    gear_tags = camera_tag + ' ' + lens_tag

    new_tags = gear_tags + ' ' + current_tags
    flickr.photos.setTags(api_key=api_key, photo_id=photo_id, tags=new_tags)
    print("Added tags: {0}".format(gear_tags))
    print(' ')

