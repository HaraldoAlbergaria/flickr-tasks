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
import sys
import os

def get_run_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    run_path = dir_path + '/'
    return run_path

def open_file(file_name, mode):
    file_path = get_run_path() + file_name
    return open(file_path, mode)

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


error_1 = 'Error: 1: Photo not found'
error_3 = 'Error: 3: Photo already in pool'
error_5 = 'Error: 5: Photo limit reached'
error_6 = 'Error: 6: Your Photo has been added to the Pending Queue for this Pool'
error_7 = 'Error: 7: Your Photo has already been added to the Pending Queue for this Pool'
error_10 = 'Error: 10: Maximum number of photos in Group Pool'

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

group_id = flickr.urls.lookupGroup(api_key=api_key, url=data.group_url)['group']['id']
group_name = flickr.urls.lookupGroup(api_key=api_key, url=data.group_url)['group']['groupname']['_content']

added = 0
dont_add_tag = 'DontAdd'

reached_end_path = get_run_path() + 'reached_end'
if os.path.exists(reached_end_path):
    rm_str = 'rm ' + reached_end_path
    os.system(rm_str)

maxpool_path = get_run_path() + 'maxpool'
if os.path.exists(maxpool_path):
    rm_str = 'rm ' + maxpool_path
    os.system(rm_str)

added_path = get_run_path() + 'added'
if os.path.exists(added_path):
    print("Warng: Script execution for group \'{0}\' has been aborted".format(group_name))
    print("Warng: The maximum number of photos has already been added")
    maxpool_file = open_file('maxpool', 'w')
    maxpool_file.close()
    sys.exit()

while added < data.group_limit:

    try:
        current_id_file = open_file('current_id', 'r')
    except FileNotFoundError as e:
        current_id_file = open_file('current_id', 'w')
        current_id_file.close()
        current_id_file = open_file('current_id', 'r')
    except:
        print("Error: FATAL: Can\'t open file \'current_id\'")
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
        if added == 0:
            reached_end_file = open_file('reached_end', 'w')
            reached_end_file.close()
        break

    photo_info = flickr.photos.getInfo(photo_id=photo_id)['photo']
    photo_title = photo_info['title']['_content']

    if procs.isOkToAdd(photo_id) and not hasTag(photo_id, dont_add_tag):
        try:
            flickr.groups.pools.add(group_id=group_id, photo_id=photo_id)
            print("Added: Photo \'{0}\' to the group \'{1}\'".format(photo_title, group_name))
            added = added + 1
            if data.group_full == True:
                added_file = open_file('added', 'w')
                added_file.close()
        except flickrapi.exceptions.FlickrError as e:
            if str(e) != error_6:
                print("Error: Unable to add photo \'{0}\' to the group \'{1}\'".format(photo_title, group_name))
            else:
                print("Warng: Photo \'{0}\' not added to the group \'{1}\' yet".format(photo_title, group_name))
                added = added + 1
                if data.group_full == True:
                    added_file = open_file('added', 'w')
                    added_file.close()
            print(e)
            if str(e) == error_5 or str(e) == error_10:
                maxpool_file = open_file('maxpool', 'w')
                maxpool_file.close()
            if str(e) != error_3 and str(e) != error_7:
                break
        except:
            print("Error: FATAL")
            break
    else:
        if hasTag(photo_id, dont_add_tag):
            print("Error: Photo \'{0}\' is tagged to not be added to any group. Skipped it.".format(photo_title, group_name))
        else:
            print("Error: Photo \'{0}\' is not elegible to be added to the group \'{1}\'".format(photo_title, group_name))

    is_public = photo_info['visibility']['ispublic']
    is_friend = photo_info['visibility']['isfriend']
    is_family = photo_info['visibility']['isfamily']
    if not hasTag(photo_id, dont_add_tag) and not is_public and not is_friend and not is_family:
        print("Error: Photo \'{0}\' is private. Stopped script to wait it become public until next run.".format(photo_title))
        reached_end_file = open_file('reached_end', 'w')
        reached_end_file.close()
        break

    current_id_file = open_file('current_id', 'w')
    current_id_file.write('{0}'.format(photo_id))
    current_id_file.close()

