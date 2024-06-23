#!/usr/bin/python3

# This script finds, from a list of lenses, the one with the focal length
# range that covers the highest number of photos in the user's
# photostream, taken with a focal length inside the range.
#
# Author: Haraldo Albergaria
# Date  : Apr 13, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import flickrapi
import api_credentials
import json
import sys
import os
import math
import time
import config

from common import getExif
from common import getCameraMaker
from common import getLensModel

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# getExif retries
max_retries = 10
retry_wait  = 1

# report file name
report_file_name = "lens_usage_report.txt"


#===== Procedures ===========================================================#

def genReport(data, total_photos, file_name):
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
    report_file = open(file_name, "w")
    report_file.write("+---------------------------------------------------------------------+\n")
    report_file.write("| Lens                                               | Photos | Ratio |\n")
    report_file.write("+---------------------------------------------------------------------|\n")
    for item in sorted_data:
        lens = item[0]
        photos = item[1]
        ratio = photos/total_photos*100
        report_file.write("| {0:<50.50} | {1:>6} | {2:>4.1f}% |\n".format(lens, photos, ratio))
    report_file.write("+---------------------------------------------------------------------+\n")
    report_file.close()


#===== MAIN CODE ==============================================================#

# set script mode (photoset or photostream) and get the total number of photos

try:
    photos = flickr.photosets.getPhotos(api_key=api_key, user_id=user_id, photoset_id=config.photoset_id, content_types=0)
    npages = int(photos['photoset']['pages'])
    ppage = int(photos['photoset']['perpage'])
    total_photos = int(photos['photoset']['total'])
    print('Photoset \'{}\''.format(photos['photoset']['title']))
    mode = 'photoset'
except:
    try:
        photos = flickr.people.getPhotos(api_key=api_key, user_id=user_id, content_types=0)
        npages = int(photos['photos']['pages'])
        ppage = int(photos['photos']['perpage'])
        total_photos = int(photos['photos']['total'])
    except:
        print("ERROR: FATAL: Unable to get photos")
        sys.exit()

    if config.photoset_id != '':
        print('ERROR: Invalid photoset id.\nSwitching to user\'s photostream...')
    mode = 'photostream'

print("Retrieving lens usage data... Please, wait.")

photo = 0

lens_dict = dict()

for pg in range(1, npages+1):

    # get photos according to run mode
    try:
        if mode == 'photoset':
            page = flickr.photosets.getPhotos(api_key=api_key, user_id=user_id, photoset_id=config.photoset_id, privacy_filter=0, content_types=0, page=pg)['photoset']['photo']
        else:
            page = flickr.people.getPhotos(api_key=api_key, user_id=user_id, content_types=0, page=pg)['photos']['photo']
    except:
        print("ERROR: FATAL: Unable to get photos")
        sys.exit()

    ppage = len(page)

    for ph in range(0, ppage):
        photo = photo + 1
        photo_id = page[ph]['id']
        try:
            exif = getExif(photo_id, 0, False)
            maker = getCameraMaker(exif)
            lens = getLensModel(exif)
            if maker not in lens:
                lens = maker + " " + lens
        except:
            break
        if lens != '':
            if config.camera_maker == '' or maker == config.camera_maker:
                try:
                    lens_dict[lens] = lens_dict[lens] + 1
                except:
                    lens_dict[lens] = 1

        print("Processed photo {0}/{1}".format(photo, total_photos), end='\r')

genReport(lens_dict, total_photos, report_file_name)

os.system("more {}".format(report_file_name))
