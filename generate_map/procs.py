# Procedures of script generate-map.py
#
# Author: Haraldo Albergaria
# Date  : Jul 07, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import flickrapi
import api_credentials
import json
import time
import config

from common import isInSet
from common import hasTag

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Retries in case of errors
max_retries = 10
retry_wait  = 3

dont_map_tag = 'DontMap'


#===== PROCEDURES =======================================================#

def getThumbUrl(photo_id, photo_sizes):
    m = 1
    if(photo_sizes[m]['width']/photo_sizes[m]['height'] > 1):
        while(photo_sizes[m]['width'] < 500 or photo_sizes[m]['height'] < 250):
            m += 1
    else:
        while(photo_sizes[m]['width'] < 250 or photo_sizes[m]['height'] < 500):
            m += 1
    return photo_sizes[m]['source']



### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, photo_title, user_id, retry):
    try:
        # get photo information
        photo_title = photo_title.replace('&', 'and')
        photos_base_url = flickr.people.getInfo(api_key=api_key, user_id=user_id)['person']['photosurl']['_content']
        photo_url = photos_base_url + photo_id
        photo_perm = flickr.photos.getPerms(api_ky=api_key, photo_id=photo_id)['perms']['ispublic']
        # get thumbnails urls
        photo_sizes = flickr.photos.getSizes(api_key=api_key, user_id=user_id, photo_id=photo_id)['sizes']['size']
        thumb_url = photo_sizes[0]['source']
        # get photo location data
        location = flickr.photos.geo.getLocation(api_ky=api_key, photo_id=photo_id)
        latitude = location['photo']['location']['latitude']
        longitude = location['photo']['location']['longitude']
        geo_perm = flickr.photos.geo.getPerms(api_ky=api_key, photo_id=photo_id)['perms']['ispublic']
        # write to html file if photo and location are public
        if photo_perm == 1 and geo_perm == 1 and not isInSet(photo_id, config.not_map_set_id) and not hasTag(photo_id, dont_map_tag):
            html_file = open("/home/pi/flickr_tasks/generate_map/map.html", "a")
            html_file.write("    locations.push([[{0}, {1}], \"<a href=\\\"{2}\\\" target=\\\"_blank\\\"><img src=\\\"{3}\\\"/></a>\"]);\n".format(longitude, latitude, photo_url, thumb_url))
            html_file.close()
            print("Added marker to map!")
    except:
        if retry < max_retries:
            time.sleep(retry_wait)
            retry += 1
            print("ERROR when adding marker to map")
            print("Retrying: {0}".format(retry))
            processPhoto(photo_id, photo_title, user_id, retry)
        else:
            pass
