# Flickr Tasks

A collection of _python_ scripts to automate some tasks on [_Flickr™_](https://www.flickr.com/). At the moment, the following are available:

- **_add_gear_tags/_**
   - **_add-gear-tags.py_**: Automatically add tags for the gear used (eg: camera model, lens model) according to exif data.
   
- **_auto_add2groups/_**
    - **_add-photo-to-group.py_**: Automatically add photos to a group according to the group rules. These rules can be regarding the limit for the number of added photos (eg: 3 each day) or the actual content of the photos (eg: a given camera or lens).

- **_auto_post2blogs/_**
    - **_post-photo-to-blogs.py_**: Automatically post photos to all the blogs configured in the user's account.

- **_auto_tasks/_**
    - **_process-photos.py_**: Process photos in a photostream to do an action according to specified rules. e.g: Add tags to photos for views, favorites and comments counts.

- **_check_exif/_**
    - **_check_exif.py_**: Checks for missing exif information on photos of a photostream.  When the script is run, if there are photos with missing exif information, the photoset 'Missing Exif' will be automatically created, and they will be added to it.

- **_find_explored/_**
    - **_find-photos-in-explore.py_**: Find user's photos in _Explore_ for the current day and send an e-mail with the list of photos if any is found.

- **_group_admin/_**
    - **_group-admin-daily-report.py_**: Reports which photos should be removed or kept in a group according to specified exif parameters. e.g.: Lens Model. Also, generates the script **_remove-photos.py_** to remove the photos that need to be removed. The report shows only the photos that were added after the last removal plus the last 100 photos before that, to guarantee that any photos added or removed during the last run will be included in the current report. Additionaly, it reports the usernames of the group's new members. Made to be run at least once a day.
    - **_group-admin-monthly-report.py_**: Same as above, but the report shows all photos since the group creation and is good to catch photos the should have been removed but for any reason were not. This can happen, for example, if photos are removed of the group by the owner after others been added, which will make some added photos do not show up in the daily report. Made to be run at least once a month.

To use these scripts it is necessary a basic knowledge of computer programming in _Python_

## Installation

The scripts were developed to run on _Linux_ systems and need _Python 3.x_ to run.

First, install the [_flickrapi_](https://stuvel.eu/flickrapi) package by typing in a terminal:

```
% pip3 install flickrapi
```
Now, get a _Flickr_'s API key by visiting the [_Flickr_ API key request page](https://www.flickr.com/services/apps/create/apply/).

After that, create a file __api_credentials.py__ with the following code and with the obtained values:

```python
api_key = u'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
api_secret = u'xxxxxxxxxxxxxxx'
user_id = 'XXXXXXXXXXXX'

```

Then, [authenticate](https://stuvel.eu/flickrapi-doc/3-auth.html#authenticating-without-local-web-server) on _Flickr_ by running:

```
% ./authenticate.py
```
This will open a web browser to get the user approval. After approve, type in the terminal the generated code.

**_Important Note:_** If a headless computer is being used the procedure above must be done in a graphical environment and the generated directory _~/.flickr_ copied to the same location at the headless system.

## Usage

- **add_gear_tags**: Inside directory 'add_gear_tags' create a link (or copy) to the file __api_credentials.py__. There are three additional files necessary to run the script:
    - **procs.py**: Open the file and read the comments to know how to customize it for your specific needs.
    - **data.py**: Include here the id of the photoset where you want to apply the tags and create dictionaries associating the exif data to the tags.

- **auto_add2groups**: Inside directory 'auto_add2groups' create a new one to your specific need (name it what you want, eg: auto_add2group_gp1) and copy the content of the directory 'files' into it. Create a link (or copy) to the file __api_credentials.py__. There are tree additional files necessary to run the script:
    - **current_id**: Include here just the id of the last photo processed by the script in the previous run. If this file is not provided or the id is invalid, the script will create a new one with the id of the last (newest) photo in the photostream. In this case, the script will run over just the photos added after it. To start the script on any photo in the photostream, set here a valid photo id. The photos will then be processed in increasing order of upload time, starting from the next photo to the id that was set here.
    - **data.py**: Include here the group data (url, limit of photos) and any other data necessary to run the script (eg: camera model, for groups of a specific camera).
    - **procs.py**: Implement here the procedures that will actually process the photos to be added to the group.

    _**TIP**: For groups that allow to add only a limited number of photos during a period (eg: 3 photos per day), create a [cron](https://opensource.com/article/17/11/how-use-cron-linux) to automatically do this._

- **auto_post2blogs**: Inside directory 'auto_post2blogs' create a link (or copy) to the file __api_credentials.py__. There is an additional file necessary to run the script:
    - **current_id**: Include here just the id of the last photo processed by the script in the previous run. If this file is not provided or the id is invalid, the script will create a new one with the id of the last (newest) photo in the photostream. In this case, the script will run over just the photos added after it. To start the script on any photo in the photostream, set here a valid photo id. The photos will then be processed in increasing order of upload time, starting from the next photo to the id that was set here.

- **auto_tasks**: Inside directory 'auto_tasks' create a new one to your specific need (name it what you want, eg: auto_tags) and copy the content of the directory 'files' into it. Create a link (or copy) to the file __api_credentials.py__. There is an additional file necessary to run the script:
    - **procs.py**: Implement here the procedures that will actually process the photos.

- **check_exif**: Inside directory 'check_exif' create a link (or copy) to the file __api_credentials.py__. There is an additional file necessary to run the script:
    - **procs.py**: Open the file and read the comments to know how to customize it for your specific needs.

- **find_explored**: Inside directory 'find_explored' create a link (or copy) to the file __api_credentials.py__. There is an additional file necessary to run the script:
    - **mail.py**: Copy the file from 'mail_cfg' to 'find_explored' directory and edit it to add the e-mail addresses and change the e-mail subject if wanted.
    
    _**TIP**: Create a [cron](https://opensource.com/article/17/11/how-use-cron-linux) to automatically check for photos in Explore and configure it to run at least once a day._

- **group_admin**: Inside directory 'group_admin' create a new one to your specific need (name it what you want, eg: group_name) and copy the content of the directory 'files' into it. Create a link (or copy) to the file __api_credentials.py__. There are two additional files necessary to run the script:
    - **group_data.py**: Include here the id, alias and url of the group.
    - **procs.py**: Implement here the procedures that will actually process the photos to generate the reports.

### IMPORTANT WARNING! Please, read before use these scripts:
These scripts were written for my specific needs of automating tasks on [my Flickr account](https://www.flickr.com/photos/hpfilho/) and I don't know if they will be useful for anyone else. But, if you want to use them, when using the **group_admin** scripts, always review carefully the results of the generated **_remove-photos.py_** and only after that run it. If you don't do this, there is a chance of removing "good" files (or even end up with an empty group pool!), in case there is any changes in the way _Flickr_ returns the EXIF data or an error in your procedures implementation.  **Please, use these scripts with care and at your own risk.**

