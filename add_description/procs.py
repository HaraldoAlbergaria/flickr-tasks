# Procedures of script add-description.py
#
# Author: Haraldo Albergaria
# Date  : Jun 23, 2024
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import api_credentials
import json
import data

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

photoset_id = data.photoset_id
overwrite_current = data.overwrite_current


#===== PROCEDURES =======================================================#

### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, user_id):

    try:
        fr = open("description.txt", "r")
        description = fr.read()
        fr.close()
    except:
        print("ERROR: Unable to open description file")
        return

    try:
        current_description = flickr.photos.getInfo(api_key=api_key, photo_id=photo_id)['photo']['description']['_content']
    except FlickrException as e:
        print("ERROR: Unable to retrieve photo info")
        print(e)
        return

    # Put any description customization here
    description_to_add = description.replace('00000000000', photo_id)

    if overwrite_current == 'yes':
        try:
            flickr.photos.setMeta(api_key=api_key, photo_id=photo_id, description=description_to_add)
            print("Description updated!")
        except FlickrException as e:
            print("ERROR: Unable to update description")
            print(e)
            return
    else:
        if description_to_add not in current_description:

            try:
                fa = open("original_descriptions.txt", "a")
                fa.write("Photo id: {}\n".format(photo_id))
                fa.write("---------------------------------------------------------\n")
                fa.write("{}\n\n\n".format(current_description))
                fa.close()
            except:
                print("ERROR: Unable to open original descriptions file")
                return

            new_description = current_description + description_to_add

            try:
                flickr.photos.setMeta(api_key=api_key, photo_id=photo_id, description=new_description)
                print("Description appended!")
            except FlickrException as e:
                print("ERROR: Unable to append description")
                print(e)
                return

        else:
            print("WARN: Description already updated")


