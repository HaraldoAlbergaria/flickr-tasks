# Procedures of script process-photos.py
#
# Author: Haraldo Albergaria
# Date  : Jan 01, 2018
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


###########################################
#  !!! IMPLEMENT THE PROCEDURES HERE !!!  #
###########################################


import flickrapi
import json
import api_credentials

api_key = api_credentials.api_key
api_secret = api_credentials.api_secret
user_id = api_credentials.user_id

# Flickr api access
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

fav_others_id = '72157623439971318'
fav_others_set = flickr.photosets.getPhotos(photoset_id=fav_others_id, user_id=user_id)
fav_others_title = fav_others_set['photoset']['title']

at10mm_id = '72157694314388675'
at10mm_set = flickr.photosets.getPhotos(photoset_id=at10mm_id, user_id=user_id)
at10mm_title = at10mm_set['photoset']['title']

at250mm_id = '72157666561896128'
at250mm_set = flickr.photosets.getPhotos(photoset_id=at250mm_id, user_id=user_id)
at250mm_title = at250mm_set['photoset']['title']

at1p8_id = '72157703794055595'
at1p8_set = flickr.photosets.getPhotos(photoset_id=at1p8_id, user_id=user_id)
at1p8_title = at1p8_set['photoset']['title']

tag = 'DNA'
summary_file = '/home/pi/flickr_tasks/auto_tasks/auto_sets/summary_sets.log'


#===== PROCEDURES =======================================================#

def isInSet(photo_id, set_id):
    try:
        photo_sets = flickr.photos.getAllContexts(photo_id=photo_id)['set']
        for i in range(len(photo_sets)):
            if photo_sets[i]['id'] == set_id:
                return True
    except:
        pass
    return False

def hasTag(photo_id, tag):
    try:
        photo_tags = flickr.tags.getListPhoto(photo_id=photo_id)
    except:
        return False
    tags = photo_tags['photo']['tags']['tag']
    for i in range(len(tags)):
        tag_id = tags[i]['id']
        tag_raw = tags[i]['raw']
        if tag_raw == tag :
            return True
    return False

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

def getFocalLength(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "FocalLength":
            return exif[i]['raw']['_content']
    return ''

def getAperture(exif):
    for i in range(len(exif)):
        if exif[i]['tag'] == "FNumber":
            return exif[i]['raw']['_content']
    return ''

def addPhotoToSetFavOthers(photo_id, photo_title, favorites, in_set):
    if not in_set and favorites >= 1 and not hasTag(photo_id, tag):
        try:
            flickr.photosets.addPhoto(api_key=api_key, photoset_id=fav_others_id, photo_id=photo_id)
            print('Added photo to \'{0}\' photoset\n'.format(set_title), end='')
            summary = open(summary_file, 'a')
            summary.write('Added photo \'{0}\' to \'{1}\'\n'.format(photo_title, fav_others_title))
            summary.close()
        except:
            print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, fav_others_title))

def addPhotoToSetAt10mm(photo_id, photo_title, in_set):
    if not in_set and not hasTag(photo_id, tag):
        try:
            flickr.photosets.addPhoto(api_key=api_key, photoset_id=at10mm_id, photo_id=photo_id)
            print('Added photo to \'{0}\' photoset\n'.format(at10mm_title), end='')
            summary = open(summary_file, 'a')
            summary.write('Added photo \'{0}\' to \'{1}\'\n'.format(photo_title, at10mm_title))
            summary.close()
        except:
            print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, at10mm_title))

def addPhotoToSetAt250mm(photo_id, photo_title, in_set):
    if not in_set and not hasTag(photo_id, tag):
        try:
            flickr.photosets.addPhoto(api_key=api_key, photoset_id=at250mm_id, photo_id=photo_id)
            print('Added photo to \'{0}\' photoset\n'.format(at250mm_title), end='')
            summary = open(summary_file, 'a')
            summary.write('Added photo \'{0}\' to \'{1}\'\n'.format(photo_title, at250mm_title))
            summary.close()
        except:
            print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, at250mm_title))

def addPhotoToSetAt1p8(photo_id, photo_title, in_set):
    if not in_set and not hasTag(photo_id, tag):
        try:
            flickr.photosets.addPhoto(api_key=api_key, photoset_id=at1p8_id, photo_id=photo_id)
            print('Added photo to \'{0}\' photoset\n'.format(at1p8_title), end='')
            summary = open(summary_file, 'a')
            summary.write('Added photo \'{0}\' to \'{1}\'\n'.format(photo_title, at1p8_title))
            summary.close()
        except:
            print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, at1p8_title))

def remPhotoFromSetFavOthers(photo_id, photo_title, favorites, in_set):
    if in_set and (favorites == 0 or hasTag(photo_id, tag)):
        try:
            flickr.photosets.removePhoto(api_key=api_key, photoset_id=fav_others_id, photo_id=photo_id)
            print('Removed photo from \'{0}\' photoset\n'.format(fav_others_title), end='')
            summary = open(summary_file, 'a')
            summary.write('Removed photo \'{0}\' from \'{1}\'\n'.format(photo_title, fav_others_title))
            summary.close()
        except:
            print('ERROR: Unable to remove photo \'{0}\' from set \'{1}\''.format(photo_title, set_title))


### !!! DO NOT DELETE OR CHANGE THE SIGNATURE OF THIS PROCEDURE !!!

def processPhoto(photo_id, photo_title, user_id):

    # Favorites of Others Set
    try:
        favorites = flickr.photos.getFavorites(photo_id=photo_id)
        photo_favs = int(favorites['photo']['total'])
        in_set = isInSet(photo_id, fav_others_id)
        print('favorites: {0}\n'.format(photo_favs), end='')
        addPhotoToSetFavOthers(photo_id, photo_title, photo_favs, in_set)
        remPhotoFromSetFavOthers(photo_id, photo_title, photo_favs, in_set)
    except:
        print('ERROR: Unable to get favorites for photo \'{0}\''.format(photo_title))

    # Lenses Exif Sets
    try:
        exif = getExif(photo_id)
        focal_length = getFocalLength(exif)
        aperture = getAperture(exif)
        print('focal length: {0}\n'.format(focal_length), end='')
        print('aperture: {0}\n'.format(aperture), end='')
    except:
        print('ERROR: Unable to get information for photo \'{0}\''.format(photo_title))
        pass

    ## @10mm
    if focal_length == '10.0 mm':
        try:
            in_set = isInSet(photo_id, at10mm_id)
            addPhotoToSetAt10mm(photo_id, photo_title, in_set)
        except:
            print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, at10mm_title))

    ## @250mm
    if (focal_length == '250.0 mm' and not hasTag(photo_id, "Kenko TELEPLUS HD DGX 1.4x") and not hasTag(photo_id, "Kenko TELEPLUS HD DGX 2x")) \
        or (focal_length == '350.0 mm' and hasTag(photo_id, "Kenko TELEPLUS HD DGX 1.4x")) \
        or (focal_length == '500.0 mm' and hasTag(photo_id, "Kenko TELEPLUS HD DGX 2x")):
        try:
            in_set = isInSet(photo_id, at250mm_id)
            addPhotoToSetAt250mm(photo_id, photo_title, in_set)
        except:
            print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, at250mm_title))

    ## @f1.8
    if aperture == '1.8':
        try:
            in_set = isInSet(photo_id, at250mm_id)
            addPhotoToSetAt1p8(photo_id, photo_title, in_set)
        except:
            print('ERROR: Unable to add photo \'{0}\' to set \'{1}\''.format(photo_title, at1p8_title))


