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
import api_credentials

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

fav_others_id = '72157623439971318'
fav_others_set = flickr.photosets.getPhotos(photoset_id=fav_others_id, user_id=user_id)
set_title = fav_others_set['photoset']['title']

summary_file = '/home/pi/flickr_tasks/auto_tasks/auto_sets/summary_sets.log'


#===== PROCEDURES =======================================================#

def hasTag(photo_id, tag):
    photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
    tags = photo_tags['photo']['tags']['tag']
    for i in range(len(tags)):
        tag_id = tags[i]['id']
        tag_raw = tags[i]['raw']
        if tag_raw == tag :
            return True
    return False

def addPhotoToSet(photo_id, photo_title, favorites):
    if favorites >= 1 and not hasTag(photo_id, 'DNA'):
        try:
            flickr.photosets.addPhoto(api_key=api_key, photoset_id=fav_others_id, photo_id=photo_id)
            print('Added photo to \'{0}\' photoset\n'.format(set_title), end='')
            summary = open(summary_file, 'a')
            summary.write('Added photo \'{0}\' to \'{1}\'\n'.format(photo_title, set_title))
            summary.close()
        except:
            pass

def remPhotoFromSet(photo_id, photo_title, favorites):
    if favorites == 0 or hasTag(photo_id, 'DNA'):
        try:
            flickr.photosets.removePhoto(api_key=api_key, photoset_id=fav_others_id, photo_id=photo_id)
            print('Removed photo from \'{0}\' photoset\n'.format(set_title), end='')
            summary = open(summary_file, 'a')
            summary.write('Removed photo \'{0}\' from \'{1}\'\n'.format(photo_title, set_title))
            summary.close()
        except:
            pass


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, photo_title, user_id):
    favorites = flickr.photos.getFavorites(photo_id=photo_id)
    photo_favs = int(favorites['photo']['total'])
    print('favorites: {0}\n'.format(photo_favs), end='')
    addPhotoToSet(photo_id, photo_title, photo_favs)
    remPhotoFromSet(photo_id, photo_title, photo_favs)
