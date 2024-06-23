# Procedures of script process-photos.py
#
# Author: Haraldo Albergaria
# Date  : Jan 01, 2018
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import api_credentials
import json
import time
import data

from common import getExif
from common import getLensModel
from common import getFocalLength

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== PROCEDURES =======================================================#

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
