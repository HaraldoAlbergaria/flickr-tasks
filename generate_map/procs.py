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


#===== PROCEDURES =======================================================#


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def createMarker(marker_info, base_url, user_id, retry):
    try:
        longitude = marker_info[0][0]
        latitude = marker_info[0][1]

        html_file = open("/home/pi/flickr_tasks/generate_map/map.html", "a")
        html_file.write("        locations.push([[{0}, {1}], \"".format(longitude, latitude))

        for photo_id in marker_info[1]:
            # get photo information
            photo_url = base_url + photo_id
            # get thumbnails urls
            photo_sizes = flickr.photos.getSizes(api_key=api_key, user_id=user_id, photo_id=photo_id)['sizes']['size']
            thumb_url = photo_sizes[0]['source']
            # write to html file if photo and location are public
            html_file.write("<a href=\\\"{0}\\\" target=\\\"_blank\\\"><img src=\\\"{1}\\\"/></a> ".format(photo_url, thumb_url))

        html_file.write("\"]);\n")
        html_file.close()

    except:
        if retry < max_retries:
            time.sleep(retry_wait)
            retry += 1
            print("ERROR when adding marker to map")
            print("Retrying: {0}".format(retry))
            createMarker(marker_info, base_url, user_id, retry)
        else:
            pass
