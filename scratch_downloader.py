"""
A quick file downloader...
Author: Simon Vogt
Language: Python 3.6
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import hashlib
try:  # python 3
    from urllib.request import urlretrieve
    from urllib.error import HTTPError
except ImportError:  # python 2
    from urllib import urlretrieve
    from urllib2 import HTTPError


# using actual local urls on my computer for quick checking:
urls = ["http://127.0.0.1:8081/textures/wood.jpg",
        "http://127.0.0.1:8081/textures/ebbe.jpg",
        "http://127.0.0.1:8081/textures/gridjpg"]

urls = set(urls)  # no need to download anything twice
hashed_urls = {}
for url in urls:
    # make unique identifier for filename:
    hashed = hashlib.sha256(url.encode()).hexdigest()
    hashed_urls[hashed] = url
    filename_on_disk = hashed

    # extract file ending:
    append_known_endings = True
    if append_known_endings:
        filetype = url.split('.')[-1]
        if filetype in ['jpg', 'jpeg', 'png', 'gif']:
            filename_on_disk = hashed + '.' + filetype
    
    # download file:
    try:
        urlretrieve(url, filename_on_disk)
    except HTTPError as e:
        print("Could not download URL '"+url+"': " + str(e))
        #raise 

    
hashed_urls

