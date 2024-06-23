#!/usr/bin/python3

# This automatically post photos to a blog
#
# Author: Haraldo Albergaria
# Date  : Nov 8, 2018
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import flickrapi
import json
import api_credentials
import os
import config

def open_file(mode):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/current_id'
    return open(file_path, mode)

error_1 = 'Error: 1: Photo not found'

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

user_blogs = flickr.blogs.getList()['blogs']['blog']

posted = 0

while posted <= config.posts_per_run:

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
        print("Warng: No more photos to post")
        print("Warng: Reached the end of the photostream")
        break

    photo_title = flickr.photos.getInfo(photo_id=photo_id)['photo']['title']['_content']
    photo_description = flickr.photos.getInfo(photo_id=photo_id)['photo']['description']['_content']

    for i in range(len(user_blogs)):
        info = flickr.photos.getInfo(photo_id=photo_id)['photo']
        is_public = info['visibility']['ispublic']
        is_friend = info['visibility']['isfriend']
        is_family = info['visibility']['isfamily']
        safety_level = info['safety_level']
        if is_public and safety_level == '0':
            try:
                flickr.blogs.postPhoto(api_key=api_key, blog_id=user_blogs[i]['id'], photo_id=photo_id, title=photo_title, description=photo_description)
                print("Postd: Succesfully posted photo \'{0}\' to \'{1}\'!".format(photo_title, user_blogs[i]['service']))
                posted = posted + 1
            except flickrapi.exceptions.FlickrError as e:
                print("Error: Failure on posting photo \'{0}\' to \'{1}\'".format(photo_title, user_blogs[i]['service']))
                print(e)

    if not is_public and not is_friend and not is_family:
        print("Error: Photo \'{0}\' is private. Stopped script to wait it become public until next run.".format(photo_title))
        break

    current_id_file = open_file('w')
    current_id_file.write('{0}'.format(photo_id))
    current_id_file.close()

