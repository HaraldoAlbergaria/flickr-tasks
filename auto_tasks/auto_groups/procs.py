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

group_url = 'https://www.flickr.com/groups/worldsfavorite/'
group_id = flickr.urls.lookupGroup(api_key=api_key, url=group_url)['group']['id']
group_name = flickr.urls.lookupGroup(api_key=api_key, url=group_url)['group']['groupname']['_content']

summary_file = '/home/pi/flickr_tasks/auto_tasks/auto_groups/summary_groups.log'


#===== PROCEDURES =======================================================#

def addPhotoToGroup(photo_id, favorites, is_public, not_in_group):
    if favorites >= 1 and is_public == 1 and not_in_group:
        try:
            flickr.groups.pools.add(api_key=api_key, photo_id=photo_id, group_id=group_id)
            print('\nAdded photo to \'{0}\' group'.format(set_title), end='')
            photo_info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
            photo_title = photo_info['photo']['title']['_content']
            summary = open(summary_file, 'a')
            summary.write('Added photo \'{0}\' to \'{1}\'\n'.format(photo_title, group_name))
            summary.close()
        except:
            pass

def remPhotoFromGroup(photo_id, favorites):
    if favorites == 0:
        try:
            flickr.groups.pools.remove(api_key=api_key, photo_id=photo_id, group_id=group_id)
            print('\nRemoved photo from \'{0}\' group'.format(group_name), end='')
            photo_info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
            photo_title = photo_info['photo']['title']['_content']
            summary = open(summary_file, 'a')
            summary.write('Removed photo \'{0}\' from \'{1}\'\n'.format(photo_title, group_name))
            summary.close()
        except:
            pass

def isInGroup(photo_id, group_id):
    photo_groups = flickr.photos.getAllContexts(photo_id=photo_id)['set']
    for i in range(len(photo_groups)):
        if photo_groups[i]['id'] == group_id:
            return True
    return False


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, user_id):
    info = flickr.photos.getFavorites(photo_id=photo_id)
    favorites = int(info['photo']['total'])
    permissions = flickr.photos.getPerms(photo_id=photo_id)
    is_public = permissions['perms']['ispublic']
    not_in_group = not isInGroup(photo_id, group_id)
    print('favorites: {0}'.format(favorites), end='')
    addPhotoToGroup(photo_id, favorites, is_public, not_in_group)
    remPhotoFromGroup(photo_id, favorites)
