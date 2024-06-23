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
import skip

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== PROCEDURES =======================================================#


def createDeleteFile():
    delete_file = open("/home/pi/flickr_tasks/del_img_comments/delete-comments.py", 'w')
    delete_file.write('#!/usr/bin/python3\n\n')
    delete_file.write('import flickrapi\n')
    delete_file.write('import json\n')
    delete_file.write('import procs\n')
    delete_file.write('import api_credentials\n\n')
    delete_file.write('api_key = api_credentials.api_key\n')
    delete_file.write('api_secret = api_credentials.api_secret\n\n')
    delete_file.write('# Flickr api access\n')
    delete_file.write('flickr = flickrapi.FlickrAPI(api_key, api_secret, format=\'parsed-json\')\n\n\n')
    delete_file.write('### COMMENTS TO DELETE:\n')
    delete_file.close()

def findImgComments(photo_id, photo_title, photo_url):

    delete_file = open("/home/pi/flickr_tasks/del_img_comments/delete-comments.py", 'a')

    try:
        comments_list = flickr.photos.comments.getList(photo_id=photo_id)['comments']['comment']
        try:
            n_comments = len(comments_list)
        except:
            n_comments = 0

        title_written = False

        for i in range(n_comments-1, -1, -1):
            skipped = False
            for s in skip.list:
                if s in comments_list[i]['_content']:
                    skipped = True
            if not skipped and comments_list[i]['author'] != user_id and ('img src' in comments_list[i]['_content'] \
                or 'www.flickr.com/photos' in comments_list[i]['_content'] or '/in/pool' in comments_list[i]['_content']):
                img_cmt_id = comments_list[i]['id']
                img_cmt_author = comments_list[i]['author']
                img_cmt_name = comments_list[i]['authorname']
                if not title_written:
                    delete_file.write('\n# Photo Title: {0}\n# Photo URL: {1}\n'.format(photo_title, photo_url))
                    delete_file.write('# --------------------------------------------------------------------------------------------------------\n')
                    title_written = True
                delete_file.write('# Comment author: {0}\ntry:\n    flickr.photos.comments.deleteComment(api_key=api_key, comment_id=\'{1}\')\n'.format(img_cmt_name, img_cmt_id))
                delete_file.write('    print("Deleted comment by \'{0}\' from photo \'{1}\'")\n'.format(img_cmt_name, photo_title.replace("\"", "")))
                delete_file.write('except:\n    print("ERROR: Unable to delete comment by \'{0}\' from photo \'{1}\'")\n'.format(img_cmt_name, photo_title.replace("\"", "")))
                print("Delete comment \'{0}\' by \'{1}\'".format(img_cmt_id, img_cmt_name))
                # find and delete any reply to the deleted comment
                for j in range(i+1, n_comments):
                    if img_cmt_author in comments_list[j]['_content']:
                        img_cmt_id = comments_list[j]['id']
                        img_cmt_name = comments_list[j]['authorname']
                        delete_file.write('# Comment author: {0}\ntry:\n    flickr.photos.comments.deleteComment(api_key=api_key, comment_id=\'{1}\')\n'.format(img_cmt_name, img_cmt_id))
                        delete_file.write('    print("Deleted comment by \'{0}\' from photo \'{1}\'")\n'.format(img_cmt_name, photo_title.replace("\"", "")))
                        delete_file.write('except:\n    print("ERROR: Unable to delete comment by \'{0}\' from photo \'{1}\'")\n'.format(img_cmt_name, photo_title.replace("\"", "")))
                        print("Delete comment \'{0}\' by \'{1}\'".format(img_cmt_id, img_cmt_name))
    except:
        pass

    delete_file.close()


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, photo_title, photo_url):
    findImgComments(photo_id, photo_title, photo_url)

