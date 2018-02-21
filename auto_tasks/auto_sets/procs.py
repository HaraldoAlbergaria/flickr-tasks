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

summary_file = '/home/pi/flickr_tasks/auto_tasks/auto_sets/summary_sets.rep'


#===== PROCEDURES =======================================================#

def addPhotoToSet(photo_id, favorites):
    if favorites >= 1:
        try:
            flickr.photosets.addPhoto(api_key=api_key, photoset_id=fav_others_id, photo_id=photo_id)
            print('\nAdded photo to \'{0}\' photoset'.format(set_title), end='')
            photo_info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
            photo_title = photo_info['photo']['title']['_content']
            summary = open(summary_file, 'a')
            summary.write('Added photo \'{0}\' to \'{1}\'\n\n'.format(photo_title, set_title))
            summary.close()
        except:
            pass

def remPhotoFromSet(photo_id, favorites):
    if favorites == 0:
        try:
            flickr.photosets.removePhoto(api_key=api_key, photoset_id=fav_others_id, photo_id=photo_id)
            print('\nRemoved photo from \'{0}\' photoset\n'.format(set_title), end='')
            photo_info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
            photo_title = photo_info['photo']['title']['_content']
            summary = open(summary_file, 'a')
            summary.write('Removed photo \'{0}\' from \'{1}\'\n'.format(photo_title, set_title))
            summary.close()
        except:
            pass


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, user_id):
    info = flickr.photos.getFavorites(photo_id=photo_id)
    favorites = int(info['photo']['total'])
    print('favorites: {0}\n'.format(favorites), end='')
    addPhotoToSet(photo_id, favorites)
    remPhotoFromSet(photo_id, favorites)
