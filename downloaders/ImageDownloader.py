"""
A more modular file downloader...
Author: Simon Vogt
Language: Python 3.6
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
#from __future__ import braces

import os
import hashlib

# using urllib instead of assuming existence of the shiny requests package:
try:  # python 3
    from urllib.request import urlretrieve
except ImportError:  # python 2
    from urllib import urlretrieve


class ImageDownloader(object):
    """
    A class for downloading any file from a given list of URLs in a text file.
    If the downloaded file has a known image type file extension, it is preserved in the downloaded file
    as to support quick image viewing for UIs that only identify file types by file name.
    """

    def __init__(self, urls_filename, append_known_endings=True):
        """
        Constructs an ImageDownloader

        :param urls_filename: Filename of the text file containing urls (one per line).
        :param append_known_endings: boolean for appending known image filetype endings. (default: True)
        """

        # sanity checks:
        if not os.path.isfile(urls_filename):  # just check existence here instead of more expensive read-op.
            raise FileNotFoundError("No such file: '"+os.getcwd()+"/"+urls_filename+"'")

        # field assignments:
        self.urls_filename = urls_filename
        self.append_known_endings = append_known_endings

        # constants, for now (possibly user-selectable in future)
        self.known_endings = ['jpg', 'jpeg', 'png', 'gif']

    def compute_unique_filename_on_disk(self, url):
        """
        Returns a unique hash of the given URL as well as a plausible file name for local storage.

        :param url: The URL string to be hashed.
        :return: Unique hash of URL for filename to be stored on disk.
        """

        # make unique identifier for filename:
        hashed = hashlib.sha256(url.encode()).hexdigest()
        filename_on_disk = hashed

        # extract file ending if requested:
        if self.append_known_endings:
            filetype = url.split('.')[-1]
            if filetype in self.known_endings:
                filename_on_disk = hashed + '.' + filetype

        return filename_on_disk

    def download_single_url(self, url):
        """
        Downloads a single URL to a file on disk.

        :param url: The URL string to be downloaded.
        :return: status of the download via a single dict with keys: ['url','filename','status']
        """

        infodict = {'url': url}
        if len(url) > 0:
            filename_on_disk = self.compute_unique_filename_on_disk(url)

            # download file:
            try:
                urlretrieve(url, filename_on_disk)
                infodict['filename'] = filename_on_disk
                infodict['status'] = 'Ok'
            except Exception as e:
                errmsg = "Could not download URL '" + url + "' due to " + str(e.__class__.__name__) + ": " + str(e)
                # print(errmsg)
                infodict['filename'] = ''
                infodict['status'] = errmsg
        else:
            infodict['filename'] = ''
            infodict['status'] = 'Skipped'
        return infodict

    def download_all_with_feedback(self):
        """
        Downloads a set of URLs into unique files and returns a list of status dicts.
        Uses the URL-file name that was given at object creation time.

        :return: list of status dicts of download attempts for all URLs given in URL-file.
        """

        # TODO: Download-status is just stored in memory. Need to instead store in some db for very long lists!
        status_info = []
        with open(self.urls_filename, 'r') as file:
            for i, line in enumerate(file):
                url = line.strip()

                infodict = self.download_single_url(url)
                infodict['linenum'] = i

                status_info.append(infodict)

        return status_info

    def download_all_standalone(self):
        """
        "Standalone" method that downloads the files and just displays the status_info on stdout.

        :return: None
        """

        import json  # built-in module and only used here, so slightly less bad to import locally
        status_info = self.download_all_with_feedback()
        print(json.dumps(status_info, indent=2))

