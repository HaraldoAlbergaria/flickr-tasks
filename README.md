# Flickr Tasks

A collection of _python_ scripts to automate some tasks on _Flickr_. At the moment, the following are available:

- **_auto_tasks/_**
    - **_process-photos.py_**: Process photos in a photostream to do an action according to specified rules. e.g: Add tags to photos for views, favorites and comments counts.

- **_group_admin/_**
    - **_group-admin-daily-report.py_**: Reports which photos should be removed or kept in a group according to specified exif parameters. e.g.: Lens Model. Also, generates the script **_remove-photos.py_** to remove the photos that need to be removed. The report shows only the photos that were added after the last removal plus the last 100 photos before that, to guarantee that any photos added or removed during the last run will be included in the current report. Made to be run at least once a day.
    - **_group-admin-monthly-report.py_**: Same as above, but the report shows all photos since the group creation and is good to catch photos the should have been removed but for any reason were not. This can happen, for example, if photos are removed of the group by the owner after others been added, which will make some added photos do not show up in the daily report. Made to be run at least once a month.

To use these scripts it is necessary a basic knowledge of computer programming in _Python_

## Installation:

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

**_Important Note:_** If a headless computer is being used the following procedure must be done in a graphical environment and the generated directory _~/.flickr_ copied to the same location at the headless system.

## Usage:

- **auto_tasks**: Inside 'auto_tasks' directory create a new one to your specific need (name it what you want) and copy the scripts in the parent directory to it. Create a link (or copy) to the file __api_credentials.py__. Implement the procedures you need in the file **procs.py**.

- **group_admin**: Inside 'group_admin' directory create a new one to your specific need (name it what you want) and copy the scripts in the parent directory to it. Create a link (or copy) to the file __api_credentials.py__. Implement the procedures you need in the respective **procs_*.py** files.

### IMPORTANT WARNING! Please, read before using these scripts:
These scripts were written for my specific needs and I don't know if they will be useful for anyone else. But, if you want to use them,
when using the **group_admin** scripts, always review carefully the results of the generated **_remove-photos.py_**' and only after that run it. If you don't do this, there is a chance of removing "good" files (or even end up with an empty group pool!), in case there is any changes in the way Flickr returns the EXIF data or an error in your procedures implementation.  **Please, use these scripts with care and at your own risk.**

