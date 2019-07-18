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

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# If photo has this tag, do not add to photoset
skip_tag = 'Exhibition'


#===== PROCEDURES =======================================================#

# Do not edit any procedure, excepting 'isExifMissing()'
# Read the comments to know how to do it

def isInSet(photo_id, set_id):
    try:
        photo_sets = flickr.photos.getAllContexts(photo_id=photo_id)['set']
        for i in range(len(photo_sets)):
            if photo_sets[i]['id'] == set_id:
                return True
    except:
        pass
    return False

def hasTag(photo_id, tag):
    try:
        photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
    except:
        return False
    tags = photo_tags['photo']['tags']['tag']
    for i in range(len(tags)):
        tag_id = tags[i]['id']
        tag_raw = tags[i]['raw']
        if tag_raw == tag :
            return True
    return False

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

def getLensModel(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "LensModel" or exif[i]['tag'] == "Lens":
            return exif[i]['raw']['_content']
    return ''

def getCameraModel(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "Model":
            return exif[i]['raw']['_content']
    return ''

def getCameraMaker(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "Make":
            return exif[i]['raw']['_content']
    return ''
def getFocalLength(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "FocalLength":
            return exif[i]['raw']['_content']
    return ''

def getAperture(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "FNumber":
            return exif[i]['raw']['_content']
    return ''

def getISO(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "ISO":
            return exif[i]['raw']['_content']
    return ''

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
def isExifMissing(photo_id):
    try:
        exif = getExif(photo_id)
        camera_maker = getCameraMaker(exif)
        camera_model = getCameraModel(exif)
        lens_model = getLensModel(exif)
        focal_length = getFocalLength(exif)
        aperture = getAperture(exif)
        iso = getISO(exif)
    except:
        print('ERROR: Unable to get information for photo \'{0}\''.format(photo_title))
        pass

    # Do not edit the next 1st, 2nd and 4th lines. Edit the 3rd line to include any additional condition
    if (camera_model == '' or lens_model == '' or focal_length == '' or aperture == '' or iso == '') \
            and not hasTag(photo_id, skip_tag) \
            and (camera_maker != 'NIKON' and camera_maker != 'Vivitar' and camera_maker != 'Fujifilm') \
            and True:
        return True
    else:
        return False


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!


def processPhoto(photo_id, photo_title, user_id, set_id, set_title):
    if isExifMissing(photo_id):
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
