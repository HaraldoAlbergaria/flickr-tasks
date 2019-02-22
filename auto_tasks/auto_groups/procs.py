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
not_add_tag = 'DNA'

summary_file = '/home/pi/flickr_tasks/auto_tasks/auto_groups/summary_groups.log'


#===== PROCEDURES =======================================================#

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

def addPhotoToGroup(photo_id, photo_title, photo_favs, is_public, in_group):
    if photo_favs >= 1 and is_public == 1 and not in_group and not hasTag(photo_id, not_add_tag):
        try:
            flickr.groups.pools.add(api_key=api_key, photo_id=photo_id, group_id=group_id)
            print('\nAdded photo to \'{0}\' group'.format(group_name), end='')
            summary = open(summary_file, 'a')
            summary.write('Added photo \'{0}\' to \'{1}\'\n'.format(photo_title, group_name))
            summary.close()
        except Exception as e:
            print('\nERROR: Unable to add photo \'{0}\' to group \'{1}\''.format(photo_title, group_name))
            print(e)

def remPhotoFromGroup(photo_id, photo_title, photo_favs, in_group):
    if in_group and (photo_favs == 0 or hasTag(photo_id, not_add_tag)):
        try:
            flickr.groups.pools.remove(api_key=api_key, photo_id=photo_id, group_id=group_id)
            print('\nRemoved photo from \'{0}\' group'.format(group_name), end='')
            summary = open(summary_file, 'a')
            summary.write('Removed photo \'{0}\' from \'{1}\'\n'.format(photo_title, group_name))
            summary.close()
        except Exception as e:
            print('\nERROR: Unable to remove photo \'{0}\' to group \'{1}\''.format(photo_title, group_name))
            print(e)

def isInGroup(photo_id, group_id):
    try:
        photo_groups = flickr.photos.getAllContexts(photo_id=photo_id)['pool']
        for i in range(len(photo_groups)):
            if photo_groups[i]['id'] == group_id:
                return True
    except:
        pass
    return False

### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, photo_title, user_id):
    try:
        favorites = flickr.photos.getFavorites(photo_id=photo_id)
        permissions = flickr.photos.getPerms(photo_id=photo_id)
        is_public = permissions['perms']['ispublic']
        in_group = isInGroup(photo_id, group_id)
        photo_favs = int(favorites['photo']['total'])
        print('favorites: {0}'.format(photo_favs), end='')
        addPhotoToGroup(photo_id, photo_title, photo_favs, is_public, in_group)
        remPhotoFromGroup(photo_id, photo_title, photo_favs, in_group)
        print(' ')
    except:
        print('ERROR: Unable to get information for photo \'{0}\''.format(photo_title))

