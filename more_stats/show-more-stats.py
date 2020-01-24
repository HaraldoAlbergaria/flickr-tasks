#!/usr/bin/python3

# This script calculates additional stats for the user's photostream
#
# Author: Haraldo Albergaria
# Date  : Jan 19, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import flickrapi
import json
import api_credentials

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== MAIN CODE ==============================================================#

photos = flickr.people.getPhotos(user_id=user_id)

npages = int(photos['photos']['pages'])
ppage = int(photos['photos']['perpage'])

total_photos = int(photos['photos']['total'])

total_views = 0
total_favorites = 0
total_comments = 0

print("Calculating stats... Please, wait.")

photo = 0

for pg in range(1, npages+1):
    page = flickr.people.getPhotos(user_id=user_id, page=pg)
    if pg == npages:
        pp = (npages - 1) * ppage
        ppage = total_photos - pp
    for ph in range(0, ppage):
        photo += 1
        photo_id = page['photos']['photo'][ph]['id']
        try:
            photo_info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
            photo_favorites = flickr.photos.getFavorites(photo_id=photo_id)
        except:
            try:
                photo_info = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)
                photo_favorites = flickr.photos.getFavorites(photo_id=photo_id)
            except:
                print("Unable to get stats for photo \'{}\'")
        views = int(photo_info['photo']['views'])
        favorites = int(photo_favorites['photo']['total'])
        comments = int(photo_info['photo']['comments']['_content'])
        total_views = total_views + views
        total_favorites = total_favorites + favorites
        total_comments = total_comments + comments
        print("Processed photo {0}/{1}".format(photo, total_photos), end='\r')

views_per_photo = int(total_views/total_photos)
favorites_per_photo = int(total_favorites/total_photos)
comments_per_photo = int(total_comments/total_photos)

print("\nSTATS:")
print("Total number of photos: {}".format(total_photos))
print("Total number of views: {}".format(total_views))
print("Total number of favorites: {}".format(total_favorites))
print("Total number of comments: {}".format(total_comments))
print("Medium number of views per photo: {}".format(views_per_photo))
print("Medium number of favorites per photo: {}".format(favorites_per_photo))
print("Medium number of comments per photo: {}\n".format(comments_per_photo))
