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
import config
import os

from common import hasTag
from common import isInSet
from procs import createMarker


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

coordinates = []
photos_base_url = flickr.people.getInfo(api_key=api_key, user_id=user_id)['person']['photosurl']['_content']

n = 0
print('Extracting photos coordinates and ids...')
for pg in range(1, npages+1):
    page = flickr.people.getPhotos(user_id=user_id, page=pg)
    ppage = len(page['photos']['photo'])

    for ph in range(0, ppage):
        n = n + 1
        photo_id = page['photos']['photo'][ph]['id']

        try:
            photo_perm = flickr.photos.getPerms(api_ky=api_key, photo_id=photo_id)['perms']['ispublic']
            geo_perm = flickr.photos.geo.getPerms(api_ky=api_key, photo_id=photo_id)['perms']['ispublic']
        except:
            photo_perm = 0
            geo_perm = 0

        exists = False
        if photo_perm == 1 and geo_perm == 1 and not isInSet(photo_id, config.not_map_set_id) and not hasTag(photo_id, config.dont_map_tag):
            try:
                location = flickr.photos.geo.getLocation(api_ky=api_key, photo_id=photo_id)
                longitude = location['photo']['location']['longitude']
                latitude = location['photo']['location']['latitude']
                for coord in coordinates:
                    if longitude == coord[0][0] and latitude == coord[0][1]:
                        coord[1].append(photo_id)
                        exists = True
                if not exists:
                    coordinates.append([[longitude, latitude], [photo_id]])
            except:
                pass

        print('Processed photo {0}/{1}'.format(n, total), end='\r')

print('')

m = 0
n_markers = len(coordinates)

print('Adding markers...')
for marker_info in coordinates:
    m = m + 1
    createMarker(marker_info, photos_base_url, user_id, 0)
    print('Added marker {0}/{1}'.format(m, n_markers), end='\r')

html_file = open("/home/pi/flickr_tasks/generate_map/map.html", "a")
html_file.write("\n        return locations;\n\n    }\n\n</script>\n\n")

# Add Statcounter code
html_file.write('<!-- Default Statcounter code for photo website\n')
html_file.write('https://haraldo-albergaria.photos/ -->\n')
html_file.write('<script type=\"text/javascript\">\n')
html_file.write('var sc_project=12357551;\n')
html_file.write('var sc_invisible=1;\n')
html_file.write('var sc_security="b15a6b74";\n')
html_file.write('var sc_https=1;\n')
html_file.write('var sc_remove_link=1;\n')
html_file.write('</script>\n')
html_file.write('<script type=\"text/javascript\"\n')
html_file.write('src=\"https://www.statcounter.com/counter/counter.js\" async></script>\n')
html_file.write('<noscript><div class=\"statcounter\"><img class=\"statcounter\"\n')
html_file.write('src=\"https://c.statcounter.com/12357551/0/b15a6b74/1/\"\n')
html_file.write('alt=\"Web Analytics"></div></noscript>\n')
html_file.write('<!-- End of Statcounter Code -->\n')

html_file.write("\n</body>\n</html>\n\n")
html_file.close()

print('')
print('Finished!')
