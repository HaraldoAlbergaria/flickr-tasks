# Procedures of script process-photos.py
#
# Author: Haraldo Albergaria
# Date  : Jul 17, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import json
import api_credentials
import time

from common import hasTag
from common import isInSet
from common import getExif
from common import getCameraMaker
from common import getCameraModel
from common import getLensModel
from common import getFocalLength
from common import getAperture
from common import getISO

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# If photo has this tag, do not add to photoset
skip_tag = 'Exhibition'

# getExif retries
max_retries = 10
retry_wait  = 1


#===== PROCEDURES =======================================================#

# Do not edit any procedure, excepting 'isExifMissing()'
# Read the comments to know how to do it

def addPhotoToSet(set_id, photo_id, photo_title, in_set):
    try:
        set_photos = flickr.photosets.getPhotos(photoset_id=set_id, user_id=user_id)
        set_title = set_photos['photoset']['title']
        flickr.photosets.addPhoto(api_key=api_key, photoset_id=set_id, photo_id=photo_id)
        print('Added photo to \'{0}\' photoset\n'.format(set_title), end='')
    except Exception as e:
        print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, set_title))
        print(e)

def remPhotoFromSet(set_id, photo_id, photo_title, in_set):
    try:
        set_photos = flickr.photosets.getPhotos(photoset_id=set_id, user_id=user_id)
        set_title = set_photos['photoset']['title']
        flickr.photosets.removePhoto(api_key=api_key, photoset_id=set_id, photo_id=photo_id)
        print('Removed photo from \'{0}\' photoset\n'.format(set_title), end='')
    except Exception as e:
        print('ERROR: Unable to remove photo \'{0}\' from set \'{1}\''.format(photo_title, set_title))
        print(e)


# This function checks if any exif information is missing
# The defaut is camera_model, lens_model, focal_length and aperture
# If needed, add others as stated in the next comment line
def isExifMissing(photo_id, photo_title):
    if not hasTag(photo_id, skip_tag):
        try:
            exif = getExif(photo_id, 0)
            camera_maker = getCameraMaker(exif)
            camera_model = getCameraModel(exif)
            lens_model = getLensModel(exif)
            focal_length = getFocalLength(exif)
            aperture = getAperture(exif)
            iso = getISO(exif)
        except:
            print('ERROR: Unable to get information for photo \'{0}\''.format(photo_title))
            return True
        # Do not edit the next 1st, 2nd and 4th lines. Edit the 3rd line to include any additional condition
        if (camera_model == '' or lens_model == '' or focal_length == '' or aperture == '' or iso == '') \
                and (camera_maker != 'NIKON' and camera_maker != 'Vivitar' and camera_maker != 'Fujifilm') \
                and True:
            return True
        else:
            return False
    else:
        print("SKIPPED!")
        return False



### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, photo_title, user_id, set_id, set_title):
    if isExifMissing(photo_id, photo_title):
        if set_id == '':
            photoset = flickr.photosets.create(api_key=api_key, title=set_title, primary_photo_id=photo_id)
            set_id = photoset['photoset']['id']
            print('Added photo to \'{0}\' photoset\n'.format(set_title), end='')
        else:
            try:
                addPhotoToSet(set_id, photo_id, photo_title, False)
            except Exception as e:
                print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, set_title))
                print(e)
    return set_id
