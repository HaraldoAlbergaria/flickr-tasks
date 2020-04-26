#!/usr/bin/python3

# This script finds, from a list of lenses, the photos that were
# taken with an aperture below a given value.
#
# Author: Haraldo Albergaria
# Date  : Apr 23, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import flickrapi
import api_credentials
import sys
import time
import data

from common import getExif
from common import getCameraMaker
from common import getCameraModel
from common import getLensModel
from common import getAperture

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
report_file_name = "lenses_wide_open_report.txt"


#===== Procedures ===========================================================#

def genReport(data, file_name):
    report_file = open(file_name, "w")
    report_file.write("+=========================================================================+\n")
    report_file.write("| Lens                                               |  Photos  |  Total  |\n")
    report_file.write("+=========================================================================+\n")
    for i in range(len(data)):
        lens = data[i][0]
        photos = data[i][2]
        total = data[i][3]
        report_file.write("| {0:<50.50} | {1:>8} | {2:>7} |\n".format(lens, photos, total))
    report_file.write("+=========================================================================+\n")
    report_file.close()


#===== MAIN CODE ==============================================================#

if data.mode == 'wide_open':
    print("Searching for photos taken with wide open aperture... Please, wait.")
else:
    if data.mode == 'max_open':
        print("Searching for photos taken below a max open aperture... Please, wait.")
    else:
        print("ERROR: Unrecognized mode. Check variable \'mode\' in file \'data.py\'")
        sys.exit()

photos = flickr.people.getPhotos(user_id=user_id)

npages = int(photos['photos']['pages'])
ppage = int(photos['photos']['perpage'])
total_photos = int(photos['photos']['total'])

photo = 0
lenses = data.lenses

for pg in range(1, npages+1):
    page = flickr.people.getPhotos(user_id=user_id, page=pg)
    ppage = len(page['photos']['photo'])

    for ph in range(0, ppage):
        photo = photo + 1
        photo_id = page['photos']['photo'][ph]['id']
        try:
            exif = getExif(photo_id, 0, False)
            camera_maker = getCameraMaker(exif)
            camera_model = getCameraModel(exif)
            lens_model = getLensModel(exif).replace(' ', '')
            aperture = getAperture(exif)
        except:
            break
        if camera_maker == data.camera['maker'] and data.camera['system'] in camera_model:
            for i in range(len(lenses)):
                if lens_model == lenses[i][0].replace(camera_maker + ' ', '').replace(' ', ''):
                    if (data.mode == 'wide_open' and float(aperture) == lenses[i][1]) \
                    or (data.mode == 'max_open' and float(aperture) < lenses[i][1]):
                        n = lenses[i][2]
                        lenses[i][2] = n + 1
                    t = lenses[i][3]
                    lenses[i][3] = t + 1
        print("Processed photo {0}/{1}".format(photo, total_photos), end='\r')

genReport(lenses, report_file_name)

print("\nFinished! Open file {} to see the results.".format(report_file_name))
