# Flickr Tasks

A collection of _python_ scripts to automate some tasks on _Flickr_. At the moment, the following are available:

- **_auto_add2groups/_**
    - **_add_photo_to_group.py_**: Automatically add photos to a group according to the group rules. These rules can be regarding the limit for the number of added photos (eg: 3 each day) or the actual content of the photos (eg: a given camera or lens).

- **_auto_tasks/_**
    - **_process-photos.py_**: Process photos in a photostream to do an action according to specified rules. e.g: Add tags to photos for views, favorites and comments counts.

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

- **auto_add2groups**: Inside directory 'auto_add2groups' create a new one to your specific need (name it what you want, eg: auto_add2group_gp1) and copy the content of the directory 'files' into it. Create a link (or copy) to the file __api_credentials.py__. There are also tree additional files necessary to run the script:
    - **current_id**: Includes just the id of the current photo that is being processed on a given run. This is updated by the script with the id of the next photo in the photostream that will be added to the group.
    - **data.py**: Include here the group data (url, limit of photos) and any other data necessary to run the script (eg: camera model, for groups of a specific camera).
    - **procs.py**: Implement here the procedures that will actually process the photos to be added to the group.

    _**TIP**: For groups that allow to add only a limited number of photos during a period (eg: 3 photos per day), create a [cron](https://opensource.com/article/17/11/how-use-cron-linux) to do this._

- **auto_tasks**: Inside directory 'auto_tasks' create a new one to your specific need (name it what you want, eg: auto_tags) and copy the content of the directory 'files' into it. Create a link (or copy) to the file __api_credentials.py__. There is also an additional file necessary to run the script:
    - **procs.py**: Implement here the procedures that will actually process the photos.

- **group_admin**: Inside directory 'group_admin' create a new one to your specific need (name it what you want, eg: group_name) and copy the content of the directory 'files' into it. Create a link (or copy) to the file __api_credentials.py__. There are also two additional files necessary to run the script:
    - **group_data.py**: Include here the id, alias and url of the group.
    - **procs.py**: Implement here the procedures that will actually process the photos to generate the reports.

### IMPORTANT WARNING! Please, read before use these scripts:
These scripts were written for my specific needs and I don't know if they will be useful for anyone else. But, if you want to use them,
when using the **group_admin** scripts, always review carefully the results of the generated **_remove-photos.py_**' and only after that run it. If you don't do this, there is a chance of removing "good" files (or even end up with an empty group pool!), in case there is any changes in the way Flickr returns the EXIF data or an error in your procedures implementation.  **Please, use these scripts with care and at your own risk.**

