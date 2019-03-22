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
import data

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

view_tags = data.view_tags
favorite_tags = data.favorite_tags
comment_tags = data.comment_tags
gallery_tags = data.gallery_tags

summary_file = '/home/pi/flickr_tasks/auto_tasks/auto_tags/summary_tags.log'


#===== PROCEDURES =======================================================#

def addTag(photo_id, photo_title, tag, tags):
    already_tagged = False
    for i in range(len(tags)):
        tag_id = tags[i]['id']
        tag_raw = tags[i]['raw']
        tag_str = '"' + tag_raw + '"'
        if tag_str == tag :
            already_tagged = True
    if already_tagged == False:
        try:
            flickr.photos.addTags(api_key=api_key, photo_id=photo_id, tags=tag)
            print(' {0}'.format(tag), end='')
            summary = open(summary_file, 'a')
            summary.write('Added {0} to \'{1}\'\n'.format(tag, photo_title))
            summary.close()
        except Exception as e:
            print(' ERROR: Unable to add tag \'{0}\''.format(tag))
            print(' ' + e)

def removeTag(photo_id, photo_title, tag, tags):
    for i in range(len(tags)):
        tag_id = tags[i]['id']
        tag_raw = tags[i]['raw']
        tag_str = '"' + tag_raw + '"'
        if tag_str == tag :
            try:
                flickr.photos.removeTag(api_key=api_key, tag_id=tag_id)
                print(' {0}'.format(tag), end='')
                summary = open(summary_file, 'a')
                summary.write('Removed {0} from \'{1}\'\n'.format(tag, photo_title))
                summary.close()
            except Exception as e:
                print(' ERROR: Unable to remove tag \'{0}\''.format(tag))
                print(' ' + e)

def addTagsToPhoto(photo_id, photo_title, n_count, available_tags, photo_tags):
    print('\n  added tags:', end='')
    tags = photo_tags['photo']['tags']['tag']
    for i in range(len(available_tags)):
        num = available_tags[i][0]
        tag = available_tags[i][1]
        if n_count >= num:
            addTag(photo_id, photo_title, tag, tags)

def delTagsFromPhoto(photo_id, photo_title, n_count, available_tags, photo_tags):
    print('\n  removed tags:', end='')
    tags = photo_tags['photo']['tags']['tag']
    for i in reverse(range(len(available_tags))):
        num = available_tags[i][0]
        tag = available_tags[i][1]
        if n_count < num:
            removeTag(photo_id, photo_title, tag, tags)

def tagViews(photo_id, photo_title):
    try:
        info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
        views = int(info['photo']['views'])
        photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
        print(' views: {0}'.format(views), end='')
        addTagsToPhoto(photo_id, photo_title, views, view_tags, photo_tags)
    except:
        pass

def tagFavorites(photo_id, photo_title):
    try:
        info = flickr.photos.getFavorites(photo_id=photo_id)
        favorites = int(info['photo']['total'])
        photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
        print('\n favorites: {0}'.format(favorites), end='')
        addTagsToPhoto(photo_id, photo_title, favorites, favorite_tags, photo_tags)
        delTagsFromPhotos(photo_id, photo_title, favorites, favorite_tags, photo_tags)
    except:
        pass

def tagComments(photo_id, photo_title, user_id):
    try:
        comments_list = flickr.photos.comments.getList(photo_id=photo_id)
        try:
            n_comments = len(comments_list['comments']['comment'])
        except:
            n_comments = 0
        no_author_comments = n_comments
        for i in range(n_comments):
            if comments_list['comments']['comment'][i]['author'] == user_id:
                no_author_comments -= 1
        photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
        print('\n comments: {0}'.format(no_author_comments), end='')
        addTagsToPhotos(photo_id, photo_title, no_author_comments, comment_tags, photo_tags)
        delTagsFromPhotos(photo_id, photo_title, no_author_comments, comment_tags, photo_tags)
    except:
        pass

def tagGalleries(photo_id, photo_title):
    try:
        info = flickr.galleries.getListForPhoto(photo_id=photo_id)
        galleries = int(info['galleries']['total'])
        photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
        print('\n galleries: {0}'.format(galleries), end='')
        addTagsToPhotos(photo_id, photo_title, galleries, gallery_tags, photo_tags)
        delTagsFromPhotos(photo_id, photo_title, galleries, gallery_tags, photo_tags)
    except:
        pass


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, photo_title, user_id):
    tagViews(photo_id, photo_title)
    tagFavorites(photo_id, photo_title)
    tagComments(photo_id, photo_title, user_id)
    tagGalleries(photo_id, photo_title)
    print(' ')

