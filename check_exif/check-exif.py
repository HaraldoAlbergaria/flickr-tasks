#!/usr/bin/python3

# This script executes tasks in all photos on a photostrean
# according to rules defined by the user. Can be used to add
# tags or add photos to groups according to views, favorites, etc.,
# for example.
#
# Author: Haraldo Albergaria
# Date  : Jul 17, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


####################################################
# !!!DO NOT MODIFY THIS FILE!!!                    #
# Implement the procedures in file procs.py        #
####################################################


import os
import socket
import flickrapi
import json
import api_credentials
import procs
import mail

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== MAIN CODE ==============================================================#

photos = flickr.people.getPhotos(user_id=user_id)
set_id = ''
set_title = 'Missing Exif'

npages = int(photos['photos']['pages'])
ppage = int(photos['photos']['perpage'])
total = int(photos['photos']['total'])

print('=============================================')
print('Pages: {0} | Per page: {1} | Total: {2}'.format(npages, ppage, total))
print('=============================================')

for pg in range(1, npages+1):
    page = flickr.people.getPhotos(user_id=user_id, page=pg)
    ppage = len(page['photos']['photo'])
    print('\n\n\nPage: {0}/{1} | Photos: {2}'.format(pg, npages, ppage))
    print('---------------------------------------------')

    for ph in range(0, ppage):
        photo_id = page['photos']['photo'][ph]['id']
        photo_title = page['photos']['photo'][ph]['title']
        print(u'\nid: {0}\ntitle: {1}'.format(photo_id, photo_title))
        set_id = procs.processPhoto(photo_id, photo_title, user_id, set_id, set_title)

print('\n\n')


# Send e-mail
if set_id != '':
    try:
        #hostname     = socket.gethostname()
        hostname     = "Flickr\ Tasks"
        photos_url   = flickr.people.getInfo(api_key=api_key, user_id=user_id)['person']['photosurl']['_content']
        mail_body    = "\"Some photos are missing exif information. Open the set \'{0}\' to see them:\n{1}albums/{2}\"".format(set_title, photos_url, set_id)
        mail_send    = "echo {0} | mail -s {1} -a From:\{2}\<{3}\> {4}".format(mail_body, mail.SUBJECT, hostname, mail.FROM, mail.TO)
        os.system(mail_send)
    except:
        print("Unable to send e-mail")
