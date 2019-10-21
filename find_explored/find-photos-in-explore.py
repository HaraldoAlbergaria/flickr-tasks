#!/usr/bin/python3

# This generates a report with photos that need to be removed
# or kept in a groups. It is useful for groups based in cameras,
# lenses or anything exif related.
#
# Author: Haraldo Albergaria
# Date  : Oct 21, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import socket
import mail
import flickrapi
import api_credentials

from datetime import datetime


#===== CONSTANTS =================================#

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== PROCEDURES =======================================================#

def hasTag(photo_id, tag):
    photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
    tags = photo_tags['photo']['tags']['tag']
    for i in range(len(tags)):
        tag_id = tags[i]['id']
        tag_raw = tags[i]['raw']
        if tag_raw == tag :
            flickr.photos.removeTag(api_key=api_key, tag_id=tag_id)
            return True
    return False


#===== MAIN CODE ==============================================================#

# get photos from explore
explore = flickr.interestingness.getList(api_key=api_key)
total_of_photos = int(explore['photos']['total'])
number_of_pages = int(explore['photos']['pages'])
photos_per_page = int(explore['photos']['perpage'])

# set variables
pos = 0
mail_body = ""
hostname = socket.gethostname()
tag = 'explored'

log = open("/home/pi/flickr_tasks/find_explored/explored.log", "w")

# iterate over each explore page
for page_number in range(1, number_of_pages+1):
    explore = flickr.interestingness.getList(api_key=api_key, page=page_number)
    photos_per_page = len(explore['photos']['photo'])

    # iterate over each photo in page
    for photo_number in range(photos_per_page):
        pos += 1
        photo_id = explore['photos']['photo'][photo_number]['id']
        photo_title = explore['photos']['photo'][photo_number]['title']
        owner_id = explore['photos']['photo'][photo_number]['owner']
        # if a user's photo has been found
        if owner_id == user_id:
           # add tag 'explored' to photo
           if not hasTag(photo_id, tag):
               try:
                   flickr.photos.addTags(api_key=api_key, photo_id=photo_id, tags=tag)
               except:
                   pass
           # add title, url and position of the photo the the body of e-mail
           mail_body = mail_body + "\"{0}\nhttp://www.flickr.com/photos/{1}/{2}\nLast position: {3}\n\"".format(photo_title, owner_id, photo_id, pos)


# get current time
now = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")

# Sends e-mail with the photos in explore
if mail_body != '':
    mail_send = "echo {0} | mail -s {1} -a From:\{2}\<{3}\> {4}".format(mail_body, mail.SUBJECT, hostname, mail.FROM, mail.TO)
    os.system(mail_send)
    log.write("[{0}] PHOTOS FOUND!!! An e-mail with the list was sent to {1}".format(now, mail.TO))
else:
    log.write("[{0}] No photos were found.".format(now))

log.close()

