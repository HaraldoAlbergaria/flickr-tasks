# Procedures of scripts group-admin-*-report.py
#
# Author: Haraldo Albergaria
# Date  : Jan 01, 2018
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
# !!! MODIFY ONLY THE ANNOTATED LINES !!! #
###########################################


import flickrapi
import json
import time
import api_credentials
import group_data
import data

#===== CONSTANTS =================================#

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret

group_id = group_data.group_id

exif_tag = group_data.exif_tags

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# getExif retries
max_retries = 10
retry_wait  = 1


#===== PROCEDURES =======================================================#

def getExif(photo_id, retry):
    try:
        exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
        if len(exif) == 0:
            while len(exif) == 0 and retry < max_retries:
                time.sleep(retry_wait)
                retry += 1
                print("ERROR when getting Exif")
                print("Retrying: {0}".format(retry))
                exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
    except:
        if retry < max_retries:
            time.sleep(retry_wait)
            retry += 1
            print("ERROR when getting Exif")
            print("Retrying: {0}".format(retry))
            getExif(photo_id, retry)
        else:
            pass
    return exif

def get(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "": # complete with your own exif tag, e.g.: LensModel, Camera
            return exif[i]['raw']['_content']
    return ''


def createRemoveScript(remove_file_name):
    remove_file = open(remove_file_name, 'w')
    remove_file.write('#!/usr/bin/python3\n\n')
    remove_file.write('import flickrapi\n')
    remove_file.write('import json\n')
    remove_file.write('import api_credentials\n\n')
    remove_file.write('api_key = api_credentials.api_key\n')
    remove_file.write('api_secret = api_credentials.api_secret\n\n')
    remove_file.write('flickr = flickrapi.FlickrAPI(api_key, api_secret, format=\'parsed-json\')\n\n')
    remove_file.write('def removePhoto(api_key, group_id, photo_id, photo_title):\n')
    remove_file.write('    try:\n')
    remove_file.write('        flickr.groups.pools.remove(api_key=api_key, photo_id=photo_id, group_id=group_id)\n')
    remove_file.write('        print(\'Removed photo: {0}\'.format(photo_title))\n')
    remove_file.write('    except:\n')
    remove_file.write('        print(\'FAILED removing photo: {0}\'.format(photo_title))\n\n')
    remove_file.write('def writeLastRemoveRun(group_id):\n')
    remove_file.write('    pool = flickr.groups.pools.getPhotos(api_key=api_key, group_id=group_id)\n')
    remove_file.write('    number_of_photos_after_current_remove = int(pool[\'photos\'][\'total\'])\n')
    remove_file.write('    last_run = open(\'last_remove_run.py\', \'w\')\n')
    remove_file.write('    last_run.write(\'number_of_photos = {0}\'.format(number_of_photos_after_current_remove))\n')
    remove_file.write('    last_run.close()\n')
    remove_file.write('\n\n### PHOTOS TO REMOVE:\n\n')
    remove_file.close()

def addReportHeader(report_file_name, group_name, photos_in_report):
    report_file = open(report_file_name,'w')
    report_file.write('+=================================================================================================================================================================+\n') # adjust szie
    if photos_in_report > 1:
        report_file.write('|                 GROUP ADMIN REPORT                     {0:30.30}                                 {1:>7} PHOTOS ADDED                      | \n'.format(group_name, photos_in_report)) # adjust size
    else:
        report_file.write('|                 GROUP ADMIN REPORT                     {0:30.30}                                 {1:>7} PHOTO ADDED                       | \n'.format(group_name, photos_in_report)) # adjust size
    report_file.write('+=================================================================================================================================================================+\n') # adjust size
    report_file.close()

def addPageHeader(report_file_name, page, number_of_pages, photos_per_page):
    report_file = open(report_file_name,'a')
    report_file.write('\n')
    report_file.write('+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+\n') # adjust size
    report_file.write('| Page: {0:>5}/{1:<5} | Photos: {2:5}                                                                                                                               |\n'.format(page, number_of_pages, photos_per_page)) # adjust size
    report_file.write('|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|\n') # adjust size
    report_file.write('|     | PHOTO                                              | OWNER                               |                                |            | ACTION |\n') # complete with your own fields and adjust size
    report_file.write('|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|\n') # adjust size
    report_file.close()

def addPhotoToRemove(remove_file_name, page_number, photo_number, photo_id, owner_id, photo_title, ): # complete with your own arguments
    remove_file = open(remove_file_name, 'a')
    remove_file.write('# {0}/{1} {2}:{3}'.format(page_number, photo_number, photo_title, )) # complete with your own argumnents
    if exif_tag:
        remove_file.write(' @{0}'.format()) # complete with your own argumnents
    remove_file.write('\n# https://www.flickr.com/photos/{0}/{1}/in/pool-{2}\n'.format(owner_id, photo_id, group_data.group_alias))
    if (not exif_tag): # complete with your own condition
        remove_file.write('# ')
    remove_file.write('removePhoto(api_key, \'{0}\', \'{1}\', \"{2}\")\n\n'.format(group_id, photo_id, photo_title))
    remove_file.close()

def addPhoto(report_file_name, remove_file_name, pool, page_number, photo_number):
    photo_id = pool['photos']['photo'][photo_number]['id']
    photo_title = pool['photos']['photo'][photo_number]['title']
    photo_owner = pool['photos']['photo'][photo_number]['ownername']
    owner_id = pool['photos']['photo'][photo_number]['owner']
    try:
        exif = getExif(photo_id)
        exif_tag = get(exif) # modify to get your own info
    except:
        exif_tag = 'NO EXIF'
    report_file = open(report_file_name,'a')
    asian = photo_title.strip(data.eastern_chars)
    no_asian = photo_title.replace(asian,'')
    report_file.write('| {0:3} | {1:50.50} | {2:35.35} | {3:40.40} | {4:>10.10} '.format(photo_number+1, no_asian, )) # complete with your own variables
    if not(exif_tag in exif_tags): # complete with your own data
        if ((not exif_tag):
            report_file.write('| REVIEW |\n')
        else:
            report_file.write('| REMOVE |\n')
        addPhotoToRemove(remove_file_name, page_number, photo_number+1, photo_id, owner_id, photo_title, ) # complete with your own arguments
    else:
        report_file.write('|  KEEP  |\n')
    report_file.close()

def addPageFooter(report_file_name):
    report_file = open(report_file_name,'a')
    report_file.write('+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+\n')

def addLastRemoveRunProcedure(remove_file_name, group_id):
    remove_file = open(remove_file_name, 'a')
    remove_file.write('\nwriteLastRemoveRun(\'{0}\')\n'.format(group_id))
    remove_file.close()


