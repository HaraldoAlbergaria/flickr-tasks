# Procedures of script process-photos.py
#
# Author: Haraldo Albergaria
# Date  : Nov 18, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import json
import api_credentials
import time

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== PROCEDURES =======================================================#

# Do not edit any procedure, excepting 'isExifMissing()'
# Read the comments to know how to do it

### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!


def processPhoto(photo_id, photo_title, user_id):
    try:

        photo_title = photo_title.replace('&', 'and')
        thumb_url = flickr.photos.getSizes(api_key=api_key, user_id=user_id, photo_id=photo_id)['sizes']['size'][3]['source']
        photos_url = flickr.people.getInfo(api_key=api_key, user_id=user_id)['person']['photosurl']['_content']
        photo_url = photos_url + photo_id

        location = flickr.photos.geo.getLocation(api_ky=api_key, photo_id=photo_id)
        latitude = location['photo']['location']['latitude']
        longitude = location['photo']['location']['longitude']

        output = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.kml", "a")
        output.write("        <Placemark>\n            <name>{0}</name>\n            <description><![CDATA[<a href=\"{1}\"><img src=\"{2}\"></a>]]></description>\n            <LookAt>\n                <longitude>{3}</longitude>\n                <latitude>{4}</latitude>\n                <altitude>0</altitude>\n            </LookAt>\n            <styleUrl>#msn_placemark_circle</styleUrl>\n            <Point>\n                <gx:drawOrder>1</gx:drawOrder>\n                <coordinates>{4},{3}</coordinates>\n            </Point>\n        </Placemark>\n".format(photo_title, photo_url, thumb_url, latitude, longitude))
        output.close()

    except:
        pass
