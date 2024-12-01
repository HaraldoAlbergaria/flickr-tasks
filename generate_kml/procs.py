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


#===== PROCEDURES =======================================================#

def getEarthThumbUrl(photo_id, photo_sizes):
    e = 2
    while(photo_sizes[e]['width'] < 320):
        e += 1
    return photo_sizes[e]['source']

def getMyMapsThumbUrl(photo_id, photo_sizes):
    m = 2
    if(photo_sizes[m]['width']/photo_sizes[m]['height'] > 1):
        while(photo_sizes[m]['width'] < 500 or photo_sizes[m]['height'] < 250):
            m += 1
    else:
        while(photo_sizes[m]['width'] < 250 or photo_sizes[m]['height'] < 500):
            m += 1
    return photo_sizes[m]['source']


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo, photos_base_url, user_id, retry):
    try:
        # get photo information
        photo_id = photo['id']
        photo_title = photo['title'].replace('&', 'and')
        print(u'\nid: {0}\ntitle: {1}'.format(photo_id, photo_title))
        photo_url = photos_base_url + photo_id
        # get thumbnails urls
        photo_sizes = flickr.photos.getSizes(api_key=api_key, user_id=user_id, photo_id=photo_id)['sizes']['size']
        earth_thumb_url = getEarthThumbUrl(photo_id, photo_sizes)
        mymaps_thumb_url = getMyMapsThumbUrl(photo_id, photo_sizes)
        # get photo location data
        latitude = photo['latitude']
        longitude = photo['longitude']
        # don't add marker if photo has don't map tag
        if not hasTag(photo_id, config.dont_map_tag):
            # write to Google Earth's file
            earth_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml", "a")
            earth_file.write("        <Placemark>\n            <name>{0}</name>\n            <description><![CDATA[<a href=\"{1}\"><img src=\"{2}\" /></a>]]></description>\n            <LookAt>\n                <longitude>{3}</longitude>\n                <latitude>{4}</latitude>\n                <altitude>0</altitude>\n            </LookAt>\n            <styleUrl>#msn_placemark_circle</styleUrl>\n            <Point>\n                <gx:drawOrder>1</gx:drawOrder>\n                <coordinates>{4},{3}</coordinates>\n            </Point>\n        </Placemark>\n".format(photo_title, photo_url, earth_thumb_url, latitude, longitude))
            earth_file.close()
            print("Added marker to 'Google Earth'!")
            # write to Google My Maps' file if photo and location are public
            if photo['ispublic'] == 1 and photo['geo_is_public'] == 1:
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
            processPhoto(photo, photos_base_url, user_id, retry)
        else:
            pass
