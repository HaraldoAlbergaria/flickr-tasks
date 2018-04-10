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

summary_file = '/home/pi/flickr_tasks/auto_tasks/auto_tags/summary_tags.log'


#===== PROCEDURES =======================================================#

def addTag(photo_id, tag):
    photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
    tags = photo_tags['photo']['tags']['tag']
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
            photo_info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
            photo_title = photo_info['photo']['title']['_content']
            summary = open(summary_file, 'a')
            summary.write('Added {0} to \'{1}\'\n'.format(tag, photo_title))
            summary.close()
        except:
            pass

def removeTag(photo_id, tag):
    photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
    tags = photo_tags['photo']['tags']['tag']
    for i in range(len(tags)):
        tag_id = tags[i]['id']
        tag_raw = tags[i]['raw']
        tag_str = '"' + tag_raw + '"'
        if tag_str == tag :
            try:
                flickr.photos.removeTag(api_key=api_key, tag_id=tag_id)
                print(' {0}'.format(tag), end='')
                photo_info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
                photo_title = photo_info['photo']['title']['_content']
                summary = open(summary_file, 'a')
                summary.write('Removed {0} from \'{1}\'\n'.format(tag, photo_title))
                summary.close()
            except:
                pass

def addViewTags(photo_id, views):
    print('\n  added tags:', end='')
    for i in range(len(view_tags)):
        v = view_tags[i][0]
        tag = view_tags[i][1]
        if views >= v:
            addTag(photo_id, tag)

def addFavoriteTags(photo_id, favorites):
    print('\n  added tags:', end='')
    for i in range(len(favorite_tags)):
        fav = favorite_tags[i][0]
        tag = favorite_tags[i][1]
        if favorites >= fav:
            addTag(photo_id, tag)

def delFavoriteTags(photo_id, favorites):
    print('\n  removed tags:', end='')
    for i in reversed(range(len(favorite_tags))):
        fav = favorite_tags[i][0]
        tag = favorite_tags[i][1]
        if favorites < fav:
            removeTag(photo_id, tag)

def addCommentTags(photo_id, comments):
    print('\n  added tags:', end='')
    for i in range(len(comment_tags)):
        cmt = comment_tags[i][0]
        tag = comment_tags[i][1]
        if comments >= cmt:
            addTag(photo_id, tag)

def delCommentTags(photo_id, comments):
    print('\n  removed tags:', end='')
    for i in reversed(range(len(comment_tags))):
        cmt = comment_tags[i][0]
        tag = comment_tags[i][1]
        if comments < cmt:
            removeTag(photo_id, tag)

def tagViews(photo_id):
    info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
    views = int(info['photo']['views'])
    print(' views: {0}'.format(views), end='')
    addViewTags(photo_id, views)

def tagFavorites(photo_id):
    info = flickr.photos.getFavorites(photo_id=photo_id)
    favorites = int(info['photo']['total'])
    print('\n favorites: {0}'.format(favorites), end='')
    addFavoriteTags(photo_id, favorites)
    delFavoriteTags(photo_id, favorites)

def tagComments(photo_id, user_id):
    comments_list = flickr.photos.comments.getList(photo_id=photo_id)
    try:
        n_comments = len(comments_list['comments']['comment'])
    except:
        n_comments = 0
    no_author_comments = n_comments
    for i in range(n_comments):
        if comments_list['comments']['comment'][i]['author'] == user_id:
            no_author_comments -= 1
    print('\n comments: {0}'.format(no_author_comments), end='')
    addCommentTags(photo_id, no_author_comments)
    delCommentTags(photo_id, no_author_comments)


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, user_id):
    tagViews(photo_id)
    tagFavorites(photo_id)
    tagComments(photo_id, user_id)


