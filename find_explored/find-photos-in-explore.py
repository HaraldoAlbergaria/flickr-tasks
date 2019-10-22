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
import procs

from datetime import datetime
from datetime import date


#===== CONSTANTS =================================#

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== MAIN CODE ==============================================================#

# get photos from explore
explore = flickr.interestingness.getList(api_key=api_key)
total_of_photos = int(explore['photos']['total'])
number_of_pages = int(explore['photos']['pages'])
photos_per_page = int(explore['photos']['perpage'])

# set variables
pos = 0
mail_body = "\""
hostname = socket.gethostname()
tag = 'explored'
bhl_url = "<a href=\"https://bighugelabs.com/scout.php?mode=history&id="
hst_pos = "\">Highest position: "

log = open("/home/pi/flickr_tasks/find_explored/explored.log", "w")

# get current date
now = datetime.now()

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
           if not procs.hasTag(photo_id, tag):
               try:
                   flickr.photos.addTags(api_key=api_key, photo_id=photo_id, tags=tag)
               except:
                   pass
           # add photo to photoset
           if not procs.isInSet(photo_id, procs.set_id) and hasTag(photo_id, tag):
               try:
                   flickr.photosets.addPhoto(api_key=api_key, photoset_id=procs.set_id, photo_id=photo_id)
               except:
                   pass
           # add explore annotation to photo description
           annotation = "\n\n\n<b>EXPLORE {0}</b>\n{1}{2}{3}{4}</a>".format(now.strftime("%b %d, %Y").upper(), bhl_url, photo_id, hst_pos, pos)
           try:
               description = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)['photo']['description']['_content']
               if "\n<b>EXPLORE " not in description:
                   annotated_description = description + annotation
                   flickr.photos.setMeta(api_key=api_key, photo_id=photo_id, description=annotated_description)
           except:
               pass
           # add title, url and position of the photo the the body of e-mail
           try:
               photos_url = flickr.people.getInfo(api_key=api_key, user_id=user_id)['person']['photosurl']['_content']
               thumb_url = flickr.photos.getSizes(api_key=api_key, user_id=user_id, photo_id=photo_id)['sizes']['size'][0]['source']
               mail_body = mail_body + "Title: {0}\nURL: {1}{2}/\nLast position: {3}\n".format(photo_title, photos_url, photo_id, pos)
               mail_body = mail_body + "\n----- Copy to profile --------------->\n<a href=\\\"{0}{1}/in/album-{2}/\\\" title=\\\"{3}\\\"><img src=\\\"{4}\\\" width=\\\"59\\\" height=\\\"59\\\" alt=\\\"{5}\\\" /></a> \n<---- Copy to profile ----------------".format(photos_url, photo_id, procs.set_id, photo_title, thumb_url, photo_title)
               mail_body = mail_body + "\n\n\n"
           except:
               pass

# get current time
now = datetime.strftime(datetime.now(), "%d/%m/%y %H:%M:%S")

# Sends e-mail with the photos in explore
if mail_body != '\"':
    mail_body = mail_body + "\""
    mail_send = "echo {0} | mail -s {1} -a From:\{2}\<{3}\> {4}".format(mail_body, mail.SUBJECT, hostname, mail.FROM, mail.TO)
    os.system(mail_send)
    log.write("[{0}] PHOTOS FOUND!!! An e-mail with the list was sent to {1}".format(now, mail.TO))
else:
    log.write("[{0}] No photos were found.".format(now))

log.close()

