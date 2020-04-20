# Procedures of script generate-kml.py and generate-set-kml.py
#
# Author: Haraldo Albergaria
# Date  : Mar 26, 2020
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

def getEarthThumbUrl(photo_id, photo_sizes):
    e = 1
    if(photo_sizes[e]['width']/photo_sizes[e]['height'] > 1):
        while(photo_sizes[e]['width'] < 240 or photo_sizes[e]['height'] < 120):
            e += 1
    else:
        while(photo_sizes[e]['width'] < 120 or photo_sizes[e]['height'] < 240):
            e += 1
    return photo_sizes[e]['source']

def getMyMapsThumbUrl(photo_id, photo_sizes):
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
        earth_thumb_url = getEarthThumbUrl(photo_id, photo_sizes)
        mymaps_thumb_url = getMyMapsThumbUrl(photo_id, photo_sizes)
        # get photo location data
        location = flickr.photos.geo.getLocation(api_ky=api_key, photo_id=photo_id)
        latitude = location['photo']['location']['latitude']
        longitude = location['photo']['location']['longitude']
        geo_perm = flickr.photos.geo.getPerms(api_ky=api_key, photo_id=photo_id)['perms']['ispublic']
        # write to Google Earth's file
        if not isInSet(photo_id, config.not_map_set_id):
            earth_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml", "a")
            earth_file.write("        <Placemark>\n            <name>{0}</name>\n            <description><![CDATA[<a href=\"{1}\"><img src=\"{2}\" /></a>]]></description>\n            <LookAt>\n                <longitude>{3}</longitude>\n                <latitude>{4}</latitude>\n                <altitude>0</altitude>\n            </LookAt>\n            <styleUrl>#msn_placemark_circle</styleUrl>\n            <Point>\n                <gx:drawOrder>1</gx:drawOrder>\n                <coordinates>{4},{3}</coordinates>\n            </Point>\n        </Placemark>\n".format(photo_title, photo_url, earth_thumb_url, latitude, longitude))
            earth_file.close()
            print("Added marker to 'Google Earth'!")
        # write to Google My Maps' file if photo and location are public
        if photo_perm == 1 and geo_perm == 1 and not isInSet(photo_id, config.not_map_set_id) and not hasTag(photo_id, dont_map_tag):
            mymaps_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.mymaps.kml", "a")
            mymaps_file.write("        <Placemark>\n            <name>{0}</name>\n            <description><![CDATA[<img src=\"{1}\" />{2}]]></description>\n            <LookAt>\n                <longitude>{3}</longitude>\n                <latitude>{4}</latitude>\n                <altitude>0</altitude>\n            </LookAt>\n            <styleUrl>#icon-1535-C2185B</styleUrl>\n            <Point>\n                <gx:drawOrder>1</gx:drawOrder>\n                <coordinates>{4},{3}</coordinates>\n            </Point>\n        </Placemark>\n".format(photo_title, mymaps_thumb_url, photo_url, latitude, longitude))
            mymaps_file.close()
            print("Added marker to 'Google My Maps!'")
    except:
        if retry < max_retries:
            time.sleep(retry_wait)
            retry += 1
            print("ERROR when adding marker to map")
            print("Retrying: {0}".format(retry))
            processPhoto(photo_id, photo_title, user_id, retry)
        else:
            pass
