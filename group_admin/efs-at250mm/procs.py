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
import api_credentials
import json
import time
import group_data
import data

from datetime import datetime

from common import getExif
from common import getLensModel
from common import getFocalLength


#===== CONSTANTS =================================#

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret

group_id = group_data.group_id

lens_models = group_data.lens_models
focal_lengths = group_data.focal_lengths

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== PROCEDURES =======================================================#

def createRemoveScript(remove_file_name):
    remove_file = open(remove_file_name, 'w')
    remove_file.write('#!/usr/bin/python3\n\n')
    remove_file.write('import flickrapi\n')
    remove_file.write('import json\n')
    remove_file.write('import procs\n')
    remove_file.write('import api_credentials\n\n')
    remove_file.write('api_key = api_credentials.api_key\n')
    remove_file.write('api_secret = api_credentials.api_secret\n\n\n')
    remove_file.write('### PHOTOS TO REMOVE:\n\n')
    remove_file.close()

def addReportHeader(report_file_name, html_file_name, group_name, photos_in_report):
    report_file = open(report_file_name,'w')
    report_file.write('+==============================================================================================================================================================================+\n')
    if photos_in_report > 1:
        report_file.write('|                 GROUP ADMIN REPORT                     {0:30.30}                                {1:>7} PHOTOS ADDED                                    | \n'.format(group_name, photos_in_report))
    else:
        report_file.write('|                 GROUP ADMIN REPORT                     {0:30.30}                                {1:>7} PHOTO ADDED                                     | \n'.format(group_name, photos_in_report))
    report_file.write('+==============================================================================================================================================================================+\n')
    report_file.close()

    now = datetime.now()
    report_file = open(html_file_name,'w')
    report_file.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\" />\n<title>Group Admin Report</title>\n')
    report_file.write('<style>\nbody {\n  font-family: courier;\n  font-size: 12px;\n  margin: 10;\n  padding: 0;\n}\n</style>\n</head>\n\n<body>\n')
    report_file.write('Updated: {}<br><br>\n'.format(datetime.strftime(now, "%d/%m/%y %H:%M:%S")))
    report_file.write('+==============================================================================================================================================================================+<br>\n')
    if photos_in_report > 1:
        report_file.write('|                 GROUP ADMIN REPORT                     {0:30.30}                                {1:>7} PHOTOS ADDED                                    |<br>\n'.format(group_name, photos_in_report).replace(' ','&nbsp;'))
    else:
        report_file.write('|                 GROUP ADMIN REPORT                     {0:30.30}                                {1:>7} PHOTO ADDED                                     |<br>\n'.format(group_name, photos_in_report).replace(' ','&nbsp;'))
    report_file.write('+==============================================================================================================================================================================+<br>\n')
    report_file.close()

def addPageHeader(report_file_name, html_file_name, page, number_of_pages, photos_per_page):
    report_file = open(report_file_name,'a')
    report_file.write('\n')
    report_file.write('+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n')
    report_file.write('| Page: {0:>5}/{1:<5} | Photos: {2:5}                                                                                                                                            |\n'.format(page, number_of_pages, photos_per_page))
    report_file.write('|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n')
    report_file.write('|     | PHOTO                                              | OWNER                               | LENS MODEL                               | F. LENGTH  | DATE ADDED | ACTION |\n')
    report_file.write('|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n')
    report_file.close()

    report_file = open(html_file_name,'a')
    report_file.write('<br>\n')
    report_file.write('+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+<br>\n')
    report_file.write('| Page: {0:>5}/{1:<5} | Photos: {2:5}                                                                                                                                            |<br>\n'.format(page, number_of_pages, photos_per_page).replace(' ','&nbsp;'))
    report_file.write('|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|<br>\n')
    report_file.write('|     | PHOTO                                              | OWNER                               | LENS MODEL                               | F. LENGTH  | DATE ADDED | ACTION |<br>\n'.replace(' ','&nbsp;'))
    report_file.write('|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|<br>\n')
    report_file.close()

def addPhotoToRemove(remove_file_name, page_number, photo_number, photo_id, owner_id, photo_title, photo_owner, lens_model, focal_length):
    remove_file = open(remove_file_name, 'a')
    remove_file.write('# {0},{1} {2}:{3} @{4}'.format(page_number, photo_number, photo_title, lens_model, focal_length))
    remove_file.write('\n# https://www.flickr.com/photos/{0}/{1}/in/pool-{2}\n'.format(owner_id, photo_id, group_data.group_alias))
    remove_file.write('procs.removePhoto(api_key, \'{0}\', \'{1}\', \'{2}\', \'{3}\')\n\n'.format(group_id, photo_id, photo_title.replace("\'", "\\\'"), photo_owner))
    remove_file.close()

def addPhoto(report_file_name, html_file_name, remove_file_name, pool, page_number, photo_number):
    photo_id = pool['photos']['photo'][photo_number]['id']
    photo_title = pool['photos']['photo'][photo_number]['title']
    photo_owner = pool['photos']['photo'][photo_number]['ownername']
    owner_id = pool['photos']['photo'][photo_number]['owner']

    try:
        photo_url = flickr.people.getInfo(api_key=api_key, user_id=owner_id)['person']['photosurl']['_content'] + photo_id
        date_added = pool['photos']['photo'][photo_number]['dateadded']
    except:
        photo_url = ''
        date_added = '0000000000'

    try:
        exif = getExif(photo_id, 0)
        lens_model = getLensModel(exif)
        focal_length = getFocalLength(exif)
    except:
        lens_model = 'NO EXIF'
        focal_length = 'NO EXIF'

    asian = photo_title.strip(data.eastern_chars)
    no_asian = photo_title.replace(asian,'')
    date = datetime.fromtimestamp(int(date_added)).strftime('%d/%m/%Y')

    report_file = open(report_file_name,'a')
    report_file.write('| {0:3} | {1:50.50} | {2:35.35} | {3:40.40} | {4:>10.10} | {5:>10.10} '.format(photo_number+1, no_asian, photo_owner, lens_model, focal_length, date))
    if (not(lens_model in lens_models)) or (not(focal_length in focal_lengths)):
        if lens_model != 'NO EXIF' and focal_length != 'NO EXIF' and lens_model != '' and focal_length != '':
            report_file.write('| REMOVE |\n')
            addPhotoToRemove(remove_file_name, page_number, photo_number+1, photo_id, owner_id, photo_title, photo_owner, lens_model, focal_length)
        else:
            report_file.write('| REVIEW |\n')
    else:
        report_file.write('|  KEEP  |\n')
    report_file.close()

    report_file = open(html_file_name,'a')
    report_file.write('| {0:3} | {1:50.50} | {2:35.35} | {3:40.40} | {4:>10.10} | {5:>10.10} '.format(photo_number+1, no_asian, photo_owner, lens_model, focal_length, date).replace(' ','&nbsp;'))
    if (not(lens_model in lens_models)) or (not(focal_length in focal_lengths)):
        if lens_model != 'NO EXIF' and focal_length != 'NO EXIF' and lens_model != '' and focal_length != '':
            report_file.write('| <ahref=\"{}\"target=\"_blank\">REMOVE</a> |<br>\n'.format(photo_url).replace(' ','&nbsp;').replace('ahref','a href').replace('target', ' target'))
        else:
            report_file.write('| <ahref=\"{}\"target=\"_blank\">REVIEW</a> |<br>\n'.format(photo_url).replace(' ','&nbsp;').replace('ahref','a href').replace('target', ' target'))
    else:
        report_file.write('|  KEEP  |<br>\n'.replace(' ','&nbsp;'))
    report_file.close()

def addPageFooter(report_file_name, html_file_name):
    report_file = open(report_file_name,'a')
    report_file.write('+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+\n')
    report_file.close()

    report_file = open(html_file_name,'a')
    report_file.write('+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+<br>\n')
    report_file.write('</body>\n</html>\n')
    report_file.close()

def addLastRemoveRunProcedure(remove_file_name, group_id):
    remove_file = open(remove_file_name, 'a')
    remove_file.write('\nprocs.writeLastRemoveRun(\'{0}\')\n'.format(group_id))
    remove_file.close()

def removePhoto(api_key, group_id, photo_id, photo_title, photo_owner):
    try:
        flickr.groups.pools.remove(api_key=api_key, photo_id=photo_id, group_id=group_id)
        print('Removed photo: \"{0}\" by {1}'.format(photo_title, photo_owner))
    except:
        print('FAILED removing photo: \"{0}\" by {1}'.format(photo_title, photo_owner))

def writeLastRemoveRun(group_id):
    try:
        pool = flickr.groups.pools.getPhotos(api_key=api_key, group_id=group_id)
        number_of_photos_after_current_remove = int(pool['photos']['total'])
        last_run = open('last_remove_run.py', 'w')
        last_run.write('number_of_photos = {0}'.format(number_of_photos_after_current_remove))
        last_run.close()
    except:
        pass

