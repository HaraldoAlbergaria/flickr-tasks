#!/usr/bin/python3

# This generates a report with photos that need to be removed
# or kept in a groups. It is useful for groups based in cameras,
# lenses or anything exif related.
#
# Author: Haraldo Albergaria
# Date  : Jan 01, 2018
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


####################################################
# !!!DO NOT MODIFY THIS FILE!!!                    #
# Implement the procedures in file procs_report.py #
# Include the rules in file group_data.py          #
####################################################


import flickrapi
import json
import time
import api_credentials
import group_data
import last_remove_run
import procs


#===== CONSTANTS =================================#

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

group_url = group_data.group_url
group_alias = group_data.group_alias

lens_models = group_data.lens_models
focal_lengths = group_data.focal_lengths

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== MAIN CODE ==============================================================#

# get group id and name from group url
group_id = flickr.urls.lookupGroup(api_key=api_key, url=group_data.group_url)['group']['id']
group_name = flickr.groups.getInfo(group_id=group_id)['group']['name']['_content']

# get photos from group pool
pool = flickr.groups.pools.getPhotos(api_key=api_key, group_id=group_id)
total_of_photos = int(pool['photos']['total'])
number_of_pages = int(pool['photos']['pages'])
photos_per_page = int(pool['photos']['perpage'])

# set output files names
report_file_name = '/home/pi/flickr_tasks/group_admin/{0}/{1}.group_admin.rep'.format(group_alias, group_name).replace(' ','_')
remove_file_name = '/home/pi/flickr_tasks/group_admin/{0}/remove-photos.py'.format(group_alias)

number_of_photos_in_last_remove = last_remove_run.number_of_photos
added_photos = total_of_photos - number_of_photos_in_last_remove
additional_photos_in_report = 100

# Add 100 more photos to the report to guarantee that photos added or removed during
# the last time the script was running will be included in the current report
photos_in_report = added_photos + additional_photos_in_report

if photos_in_report > photos_per_page + additional_photos_in_report:
    number_of_pages = int(photos_in_report / photos_per_page) + 1
else:
    photos_per_page = photos_in_report
    number_of_pages = 1

# create and add header to report file
procs.addReportHeader(report_file_name, group_name, added_photos)
# create remove script
procs.createRemoveScript(remove_file_name)

# iterate over each pool page
for page_number in range(1, number_of_pages+1):
    pool = flickr.groups.pools.getPhotos(api_key=api_key, group_id=group_id, page=page_number, per_page=photos_per_page)
    # add header to photos page
    procs.addPageHeader(report_file_name, page_number, number_of_pages, photos_per_page)
    # iterate over each photo in page
    for photo_number in range(photos_per_page):
        # add photo to report with action to be performed
        # add also to remove script in case should be removed
        procs.addPhoto(report_file_name, remove_file_name, pool, page_number, photo_number)
        # add page footer if it is the last photo of the page
        if photo_number == photos_per_page-1:
            procs.addPageFooter(report_file_name)

# write to a file the number of remaining photos in the pool after the last remove
procs.addLastRemoveRunProcedure(remove_file_name, group_id)

