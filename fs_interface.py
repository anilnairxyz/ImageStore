# -*- coding: utf-8 -*-
"""
File System Interface
This is an interface / model for the file system used for image storage.
In this minimal example we use a simple directory structure to store
the images.
This will be replaced by a scalable image storage mechanism like AWS S3
"""
import os
import json

class Storage(object):

    UPLOAD_FOLDER = os.environ['STORAGE_FOLDER']

    def save_image(self, image_name, image_type, image_id, transform=None):
        """
        Save the image into the file system
        """
        directory = os.path.join(self.UPLOAD_FOLDER, image_id[:2])
        if transform:
            filename = '{i}_{t}'.format(i=image_id, t=transform)
        else:
            filename = image_id
        filename = '{i}_{t}'.format(i=filename, t=image_type)
        filename = '{f}.{e}'.format(f=filename, e='txt')
        image_metadata = {'filename': image_name, 'type': image_type}
        image_metadata['id'] = image_id
        image_metadata['transform'] = transform
        if not os.path.exists(directory):
            os.makedirs(directory)
        pathname = os.path.join(directory, filename)
        with open(pathname, 'w') as outfile:
            json.dump(image_metadata, outfile)
        return True

    def get_image(self, image_id, image_type, transform=None):
        """
        Retrieves the image from the file system
        """
        directory = os.path.join(self.UPLOAD_FOLDER, image_id[:2])
        if transform:
            filename = '{i}_{t}'.format(i=image_id, t=transform)
        else:
            filename = image_id
        filename = '{i}_{t}'.format(i=filename, t=image_type)
        filename = '{f}.{e}'.format(f=filename, e='txt')
        pathname = os.path.join(directory, filename)
        if not os.path.exists(pathname):
            return False
        with open(pathname, 'r') as infile:
            return json.load(infile)
