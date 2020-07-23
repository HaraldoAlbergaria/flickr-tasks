# Common procedures for all scripts
#
# Author: Haraldo Albergaria
# Date  : Apr 14, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import flickrapi
import api_credentials
import time


#===== CONSTANTS =================================#

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# getExif retries
max_retries = 10
retry_wait  = 1


#===== PROCEDURES =======================================================#

def getExif(photo_id, retry, print_retry=True):
    try:
        exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
        if len(exif) == 0:
            while len(exif) == 0 and retry < max_retries:
                time.sleep(retry_wait)
                retry += 1
                if print_retry:
                    print("ERROR when getting Exif for photo id: {}".format(photo_id))
                    print("Retrying: {0}".format(retry))
                try:
                    exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
                except:
                    exif = ''
        return exif
    except:
        if retry < max_retries:
            time.sleep(retry_wait)
            retry += 1
            if print_retry:
                print("ERROR when getting Exif for photo id: {}".format(photo_id))
                print("Retrying: {0}".format(retry))
            getExif(photo_id, retry)
        else:
            print('Unable to get Exif for photo id: {}'.format(photo_id))
            return ''

def getCameraMaker(exif):
    if exif != '':
        for i in range(len(exif)):
            if exif[i]['tag'] == "Make":
                return exif[i]['raw']['_content']
    return ''

def getCameraModel(exif):
    if exif != '':
        for i in range(len(exif)):
            if exif[i]['tag'] == "Model":
                return exif[i]['raw']['_content']
    return ''

def getCameraType(exif):
    if exif != '':
        for i in range(len(exif)):
            if exif[i]['tag'] == "CameraType":
                return exif[i]['raw']['_content']
    return ''

def getLensModel(exif):
    if exif != '':
        for i in range(len(exif)):
            if exif[i]['tag'] == "LensModel" or exif[i]['tag'] == "Lens":
                return exif[i]['raw']['_content']
    return ''

def getFocalLength(exif):
    if exif != '':
        for i in range(len(exif)):
            if exif[i]['tag'] == "FocalLength":
                return exif[i]['raw']['_content']
    return ''

def getAperture(exif):
    if exif != '':
        for i in range(len(exif)):
            if exif[i]['tag'] == "FNumber":
                return exif[i]['raw']['_content']
    return ''

def getISO(exif):
    if exif != '':
        for i in range(len(exif)):
            if exif[i]['tag'] == "ISO":
                return exif[i]['raw']['_content']
    return ''

def hasTag(photo_id, tag):
    try:
        photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
        tags = photo_tags['photo']['tags']['tag']
        for i in range(len(tags)):
            tag_id = tags[i]['id']
            tag_raw = tags[i]['raw']
            if tag_raw == tag :
                return True
    except:
        pass
    return False

def hasTagRemove(photo_id, tag):
    try:
        photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
        tags = photo_tags['photo']['tags']['tag']
        for i in range(len(tags)):
            tag_id = tags[i]['id']
            tag_raw = tags[i]['raw']
            if tag_raw == tag :
                flickr.photos.removeTag(api_key=api_key, tag_id=tag_id)
                return True
    except:
        pass
    return False

def isInGroup(photo_id, group_id):
    try:
        photo_groups = flickr.photos.getAllContexts(photo_id=photo_id)['pool']
        for i in range(len(photo_groups)):
            if photo_groups[i]['id'] == group_id:
                return True
    except:
        pass
    return False

def isInSet(photo_id, set_id):
    try:
        photo_sets = flickr.photos.getAllContexts(photo_id=photo_id)['set']
        for i in range(len(photo_sets)):
            if photo_sets[i]['id'] == set_id:
                return True
    except:
        pass
    return False


