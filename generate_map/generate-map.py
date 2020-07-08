#!/usr/bin/python3

# This script generates a html file of all the photos on the
# user's photostream, that can be viewed in a web browser
#
# Author: Haraldo Albergaria
# Date  : Jul 07, 2020
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


####################################################
# !!!DO NOT MODIFY THIS FILE!!!                    #
# Implement the procedures in file procs.py        #
####################################################


import flickrapi
import json
import api_credentials
import procs
import config
import os

# Credentials
api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


#===== MAIN CODE ==============================================================#

os.system('cp /home/pi/flickr_tasks/generate_map/header.html /home/pi/flickr_tasks/generate_map/map.html')

photos = flickr.people.getPhotos(user_id=user_id)

npages = int(photos['photos']['pages'])
ppage = int(photos['photos']['perpage'])
total = int(photos['photos']['total'])

print('=============================================')
print('Pages: {0} | Per page: {1} | Total: {2}'.format(npages, ppage, total))
print('=============================================')

for pg in range(1, npages+1):
    page = flickr.people.getPhotos(user_id=user_id, page=pg)
    ppage = len(page['photos']['photo'])
    print('\n\n\nPage: {0}/{1} | Photos: {2}'.format(pg, npages, ppage))
    print('---------------------------------------------')

    for ph in range(0, ppage):
        photo_id = page['photos']['photo'][ph]['id']
        photo_title = page['photos']['photo'][ph]['title']
        print(u'\nid: {0}\ntitle: {1}'.format(photo_id, photo_title))
        set_id = procs.processPhoto(photo_id, photo_title, user_id, 0)

print('\n\n')

html_file = open("/home/pi/flickr_tasks/generate_map/map.html", "a")
html_file.write("\n    locations.forEach(addMarker);\n\n    function addMarker(value) {\n        new mapboxgl.Marker({color:'#C2185B',scale:0.7,draggable:false})\n        	.setLngLat(value[0])\n            .setPopup(new mapboxgl.Popup({closeButton:false}).setHTML(value[1]))\n            .addTo(map);\n    }\n\n</script>\n\n</body>\n</html>\n")
html_file.close()

os.system('cp /home/pi/flickr_tasks/generate_map/map.html /home/pi/github/pages/flickr-photos-map/index.html')
