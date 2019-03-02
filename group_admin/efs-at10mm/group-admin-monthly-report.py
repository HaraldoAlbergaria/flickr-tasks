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
# Implement the procedures in file procs.py        #
# Include the rules in file group_data.py          #
####################################################


import flickrapi
import json
import time
import api_credentials
import group_data
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
report_file_name = '/home/pi/flickr_tasks/group_admin/{0}/{1}.photos.admin.monthly.txt'.format(group_alias, group_name).replace(' ','_')
remove_file_name = '/home/pi/flickr_tasks/group_admin/{0}/remove-photos.py'.format(group_alias)

# create and add header to report file
procs.addReportHeader(report_file_name, group_name, total_of_photos)
# create remove script
procs.createRemoveScript(remove_file_name)

# iterate over each pool page
for page_number in range(1, number_of_pages+1):
    pool = flickr.groups.pools.getPhotos(api_key=api_key, group_id=group_id, page=page_number)
    photos_per_page = len(pool['photos']['photo'])
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

procs.addLastRemoveRunProcedure(remove_file_name, group_id)


##### MEMBERS #####

# get members from group
members = flickr.groups.members.getList(api_key=api_key, group_id=group_id)
total_of_members = int(members['members']['total'])
number_of_pages_ = int(members['members']['pages'])
members_per_page = int(members['members']['perpage'])

# set output files names
current_members_file_name = '/home/pi/flickr_tasks/group_admin/{0}/{1}.members.current.txt'.format(group_alias, group_name).replace(' ','_')
new_members_file_name = '/home/pi/flickr_tasks/group_admin/{0}/{1}.members.new.txt'.format(group_alias, group_name).replace(' ','_')

# read the current members file
last_members = open(current_members_file_name, "r")
last_members_list = last_members.readlines()
last_members.close()

# create the list for current members and open the file for writing
current_members_list = []
current_members_file = open(current_members_file_name, "w")

# iterate over each members page
for page_number in range(1, number_of_pages_+1):
    members = flickr.groups.members.getList(api_key=api_key, group_id=group_id, page=page_number, per_page=members_per_page)
    # iterate over each member in page
    for member_number in range(members_per_page):
        try:
            member_name = members['members']['member'][member_number]['username']
            # add member to list and write to file
            current_members_list.append(member_name)
            current_members_file.write("{0}\n".format(member_name))
        except:
            pass

# close the current members file
current_members_file.close()

# open the new members file for writing
new_members = open(new_members_file_name, "w")

# strip the newline character from last members list
last_members_list = [m.strip("\n") for m in last_members_list]

# for each current member,
# if member is not in the last members list
# add it to the new members file
for member in current_members_list:
    if member not in last_members_list:
        new_members.write("{0}\n".format(member))

# closer the new members file
new_members.close()


