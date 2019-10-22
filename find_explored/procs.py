# Procedures of script process-photos.py
#
# Author: Haraldo Albergaria
# Date  : Jul 17, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import api_credentials

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# id of set to add explored photos
set_id = '72157651834915447'


#===== PROCEDURES =======================================================#

# Do not edit any procedure, excepting 'isExifMissing()'
# Read the comments to know how to do it

def hasTag(photo_id, tag):
    photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
    tags = photo_tags['photo']['tags']['tag']
    for i in range(len(tags)):
        tag_id = tags[i]['id']
        tag_raw = tags[i]['raw']
        if tag_raw == tag :
            return True
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



