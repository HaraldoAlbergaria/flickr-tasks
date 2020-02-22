# Procedures of script process-photos.py
#
# Author: Haraldo Albergaria
# Date  : Jan 01, 2018
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import json
import time
import api_credentials
import data

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# getExif retries
max_retries = 10
retry_wait  = 1


#===== PROCEDURES =======================================================#

def getExif(photo_id, retry):
    try:
        exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
        if len(exif) == 0:
            while len(exif) == 0 and retry < max_retries:
                time.sleep(retry_wait)
                retry += 1
                print("ERROR when getting Exif")
                print("Retrying: {0}".format(retry))
                exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
        return exif
    except:
        if retry < max_retries:
            time.sleep(retry_wait)
            retry += 1
            print("ERROR when getting Exif")
            print("Retrying: {0}".format(retry))
            getExif(photo_id, retry)
        else:
            return ''

def getLensModel(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "LensModel" or exif[i]['tag'] == "Lens":
            return exif[i]['raw']['_content']
    return ''

def getFocalLength(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "FocalLength":
            return exif[i]['raw']['_content']
    return ''


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def isOkToAdd(photo_id):
    info = flickr.photos.getInfo(photo_id=photo_id)['photo']
    is_public = info['visibility']['ispublic']
    safety_level = info['safety_level']
    try:
        exif = getExif(photo_id, 0)
        lens_model = getLensModel(exif)
        focal_length = getFocalLength(exif)
    except:
        return False
    if is_public and safety_level == '0' and lens_model in data.lens_models and focal_length in data.focal_lengths:
        return True
    else:
        return False
