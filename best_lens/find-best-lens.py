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
import time
import data

from common import getCameraMaker
from common import getCameraModel

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# getExif retries
max_retries = 10
retry_wait  = 1


#===== Procedures ===========================================================#

def getExif(photo_id, retry):
    try:
        exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
        if len(exif) == 0:
            while len(exif) == 0 and retry < max_retries:
                time.sleep(retry_wait)
                retry += 1
                exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
        return exif
    except:
        if retry < max_retries:
            time.sleep(retry_wait)
            retry += 1
            getExif(photo_id, retry)
        else:
            return ''

def getFocalLength(exif):
    if exif != '':
        for i in range(len(exif)):
            if exif[i]['tag'] == "FocalLength":
                return float(exif[i]['raw']['_content'].replace(' mm', ''))
    return 0

def getBestLens(data):
    best_lens = [ "", 0 ]
    for i in range(len(data)):
        if data[i][3] > best_lens[1]:
            best_lens[0] = data[i][0]
            best_lens[1] = data[i][3]
    return best_lens[0]

def genReport(data):
    best_lens = getBestLens(data)
    report_file = open("best_lens_report.txt", "w")
    report_file.write("+==========================================================================+\n")
    report_file.write("| Lens                                               |   Score   | Is Best |\n")
    report_file.write("+==========================================================================+\n")
    for i in range(len(data)):
        lens = data[i][0]
        score = data[i][3]
        report_file.write("| {0:<50.50} | {1:>9} ".format(lens, score))
        if lens == best_lens:
            report_file.write("|    *    |\n")
        else:
            report_file.write("|         |\n")
    report_file.write("+==========================================================================+\n")


#===== MAIN CODE ==============================================================#

photos = flickr.people.getPhotos(user_id=user_id)

npages = int(photos['photos']['pages'])
ppage = int(photos['photos']['perpage'])
total_photos = int(photos['photos']['total'])

print("Searching for best lens... Please, wait.")

photo = 0
lenses = data.lenses

for pg in range(1, npages+1):
    page = flickr.people.getPhotos(user_id=user_id, page=pg)
    ppage = len(page['photos']['photo'])

    for ph in range(0, ppage):
        photo = photo + 1
        photo_id = page['photos']['photo'][ph]['id']
        try:
            exif = getExif(photo_id, 0)
            camera_maker = getCameraMaker(exif)
            camera_model = getCameraModel(exif)
            focal_length = getFocalLength(exif)
        except:
            break
        if camera_maker == data.camera['maker'] and data.camera['system'] in camera_model:
            for i in range(len(lenses)):
                if focal_length >= lenses[i][1] and focal_length <= lenses[i][2]:
                    n = lenses[i][3]
                    lenses[i][3] = n + 1
        print("Processed photo {0}/{1}".format(photo, total_photos), end='\r')

genReport(lenses)
best_lens = getBestLens(lenses)
print("Best Lens: {}".format(best_lens))

