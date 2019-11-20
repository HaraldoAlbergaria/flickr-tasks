# Procedures of script process-photos.py
#
# Author: Haraldo Albergaria
# Date  : Nov 18, 2019
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import flickrapi
import json
import api_credentials
import time

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Photos with this tag
# won't be included on map
not_map_tag = 'Exhibition'

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


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, photo_title, user_id):
    try:
        # get photo information
        photo_title = photo_title.replace('&', 'and')
        small_size_url = flickr.photos.getSizes(api_key=api_key, user_id=user_id, photo_id=photo_id)['sizes']['size'][3]['source']
        medium_size_url = flickr.photos.getSizes(api_key=api_key, user_id=user_id, photo_id=photo_id)['sizes']['size'][6]['source']
        photos_base_url = flickr.people.getInfo(api_key=api_key, user_id=user_id)['person']['photosurl']['_content']
        photo_url = photos_base_url + photo_id
        photo_perm = flickr.photos.getPerms(api_ky=api_key, photo_id=photo_id)['perms']['ispublic']
        # get photo location data
        location = flickr.photos.geo.getLocation(api_ky=api_key, photo_id=photo_id)
        latitude = location['photo']['location']['latitude']
        longitude = location['photo']['location']['longitude']
        geo_perm = flickr.photos.geo.getPerms(api_ky=api_key, photo_id=photo_id)['perms']['ispublic']
        # write to Google Earth's file
        earth_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.earth.kml", "a")
        earth_file.write("        <Placemark>\n            <name>{0}</name>\n            <description><![CDATA[<a href=\"{1}\"><img src=\"{2}\" /></a>]]></description>\n            <LookAt>\n                <longitude>{3}</longitude>\n                <latitude>{4}</latitude>\n                <altitude>0</altitude>\n            </LookAt>\n            <styleUrl>#msn_placemark_circle</styleUrl>\n            <Point>\n                <gx:drawOrder>1</gx:drawOrder>\n                <coordinates>{4},{3}</coordinates>\n            </Point>\n        </Placemark>\n".format(photo_title, photo_url, small_size_url, latitude, longitude))
        earth_file.close()
        # write to Google My Maps' file if photo and location are public
        if photo_perm == 1 and geo_perm == 1 and not hasTag(photo_id, not_map_tag):
            mymaps_file = open("/home/pi/flickr_tasks/generate_kml/my_flickr_photos.mymaps.kml", "a")
            mymaps_file.write("        <Placemark>\n            <name>{0}</name>\n            <description><![CDATA[<img src=\"{1}\" />{2}]]></description>\n            <LookAt>\n                <longitude>{3}</longitude>\n                <latitude>{4}</latitude>\n                <altitude>0</altitude>\n            </LookAt>\n            <styleUrl>#msn_placemark_circle</styleUrl>\n            <Point>\n                <gx:drawOrder>1</gx:drawOrder>\n                <coordinates>{4},{3}</coordinates>\n            </Point>\n        </Placemark>\n".format(photo_title, medium_size_url, photo_url, latitude, longitude))
            mymaps_file.close()
    except:
        pass
