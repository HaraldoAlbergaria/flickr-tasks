# Procedures of script group-admin-report.py
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

lens_models = group_data.lens_models
focal_lengths = group_data.focal_lengths

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== PROCEDURES =======================================================#

def getExif(photo_id):
    try:
        exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
        if len(exif) == 0:
            retry = 0
            while len(exif) == 0 and retry < 10:
                time.sleep(1)
                exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
                retry = retry + 1
    except:
        try:
            exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
            if len(exif) == 0:
                retry = 0
                while len(exif) == 0 and retry < 10:
                    time.sleep(1)
                    exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
                    retry = retry + 1
        except:
            exif = flickr.photos.getExif(api_key=api_key, photo_id=photo_id)['photo']['exif']
    return exif

def getLensModel(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "LensModel" or exif[i]['tag'] == "Lens":
            return exif[i]['raw']['_content']
    return ''

def getFocalLength(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "FocalLength":
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
    report_file.write('+=================================================================================================================================================================+\n')
    if photos_in_report > 1:
        report_file.write('|                 GROUP ADMIN REPORT                     {0:30.30}                                {1:>7} PHOTOS ADDED                       | \n'.format(group_name, photos_in_report))
    else:
        report_file.write('|                 GROUP ADMIN REPORT                     {0:30.30}                                {1:>7} PHOTO ADDED                        | \n'.format(group_name, photos_in_report))
    report_file.write('+=================================================================================================================================================================+\n')
    report_file.close()

def addPageHeader(report_file_name, page, number_of_pages, photos_per_page):
    report_file = open(report_file_name,'a')
    report_file.write('\n')
    report_file.write('+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+\n')
    report_file.write('| Page: {0:>5}/{1:<5} | Photos: {2:5}                                                                                                                               |\n'.format(page, number_of_pages, photos_per_page))
    report_file.write('|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|\n')
    report_file.write('|     | PHOTO                                              | OWNER                               | LENS MODEL                               |  F. LENGTH | ACTION |\n')
    report_file.write('|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|\n')
    report_file.close()

def addPhotoToRemove(remove_file_name, page_number, photo_number, photo_id, owner_id, photo_title, lens_model, focal_length):
    remove_file = open(remove_file_name, 'a')
    remove_file.write('# {0}/{1} {2}:{3}'.format(page_number, photo_number, photo_title, lens_model))
    if lens_model:
        remove_file.write(' @{0}'.format(focal_length))
    remove_file.write('\n# https://www.flickr.com/photos/{0}/{1}/in/pool-{2}\n'.format(owner_id, photo_id, group_data.group_alias))
    if ((not lens_model) or (not focal_length)):
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
        lens_model = getLensModel(exif)
        focal_length = getFocalLength(exif)
    except:
        lens_model = 'NO EXIF'
        focal_length = 'NO EXIF'
    report_file = open(report_file_name,'a')
    asian = photo_title.strip(data.eastern_chars)
    no_asian = photo_title.replace(asian,'')
    report_file.write('| {0:3} | {1:50.50} | {2:35.35} | {3:40.40} | {4:>10.10} '.format(photo_number+1, no_asian, photo_owner, lens_model, focal_length))
    if (not(lens_model in lens_models)) or (not(focal_length in focal_lengths)):
        if ((not lens_model) or (not focal_length)):
            report_file.write('| REVIEW |\n')
        else:
            report_file.write('| REMOVE |\n')
        addPhotoToRemove(remove_file_name, page_number, photo_number+1, photo_id, owner_id, photo_title, lens_model, focal_length)
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


