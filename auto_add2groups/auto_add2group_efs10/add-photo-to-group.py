#!/usr/bin/python3

# This automatically adds photos to a group pool
# according to the group rules
#
# Author: Haraldo Albergaria
# Date  : Nov 5, 2018
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


####################################################
# !!!DO NOT MODIFY THIS FILE!!!                    #
# Implement the procedures in file procs.py        #
# Include the rules in file data.py                #
####################################################


import flickrapi
import json
import api_credentials
import data
import procs
import os

def open_file(mode):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/current_id'
    return open(file_path, mode)


error_1 = 'Error: 1: Photo not found'
error_3 = 'Error: 3: Photo already in pool'
error_5 = 'Error: 5: Photo limit reached'
error_6 = 'Error: 6: Your Photo has been added to the Pending Queue for this Pool'
error_7 = 'Error: 7: Your Photo has already been added to the Pending Queue for this Pool'

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

group_id = flickr.urls.lookupGroup(api_key=api_key, url=data.group_url)['group']['id']
group_name = flickr.urls.lookupGroup(api_key=api_key, url=data.group_url)['group']['groupname']['_content']

added = 0

while added < data.group_limit:

    try:
        current_id_file = open_file('r')
    except FileNotFoundError as e:
        current_id_file = open_file('w')
        current_id_file.close()
        current_id_file = open_file('r')
    except:
        print("Error: FATAL")
        break

    current_id = current_id_file.read().replace('\n', '')
    current_id_file.close()

    error_1_id = 'Error: 1: Photo \"' + current_id + '\" not found (invalid ID)'

    try:
        flickr.photos.getInfo(photo_id=current_id)
    except flickrapi.exceptions.FlickrError as e:
        print(e)
        if str(e) == error_1 or str(e) == error_1_id:
            print("Warng: Using the last photo from the user\'s photostream")
            current_id = flickr.people.getPublicPhotos(user_id=user_id)['photos']['photo'][1]['id']
        else:
            print("Error: FATAL")
            break
    except:
        print("Error: FATAL")
        break

    photo_id = flickr.photos.getContext(photo_id=current_id)['nextphoto']['id']

    if photo_id == 0:
        print("Warng: No more photos to add to the group \'{0}\'".format(group_name))
        print("Warng: Reached the end of the photostream")
        break

    photo_title = flickr.photos.getInfo(photo_id=photo_id)['photo']['title']['_content']

    if procs.isOkToAdd(photo_id):
        try:
            flickr.groups.pools.add(group_id=group_id, photo_id=photo_id)
            print("Added: Photo \'{0}\' to the group \'{1}\'".format(photo_title, group_name))
            added = added + 1
        except flickrapi.exceptions.FlickrError as e:
            if str(e) != error_6:
                print("Error: Unable to add photo \'{0}\' to the group \'{1}\'".format(photo_title, group_name))
            else:
                print("Warng: Photo \'{0}\' not added to the group \'{1}\' yet".format(photo_title, group_name))
                added = added + 1
            print(e)
            if str(e) != error_3 and str(e) != error_7:
                break
        except:
            print("Error: FATAL")
            break
    else:
        print("Error: Photo \'{0}\' is not elegible to be added to the group \'{1}\'".format(photo_title, group_name))

    current_id_file = open_file('w')
    current_id_file.write('{0}'.format(photo_id))
    current_id_file.close()

