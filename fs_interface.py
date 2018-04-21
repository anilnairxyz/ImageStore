# -*- coding: utf-8 -*-
"""
File System Interface
This is an interface / model for the file system used for image storage.
This should be replaced if the images are stored elsewhere like AWS S3
"""
import os
import json

class Storage(object):

    UPLOAD_FOLDER = '/Users/anilnair/Repos/ImageStore/tmp/'

    def save_image(self, image, image_type, image_id, transform=None):
        directory = os.path.join(self.UPLOAD_FOLDER, image_id[:2])
        if transform:
            image_name = '{i}_{t}'.format(i=image_id, t=transform)
        else:
            image_name = image_id
        filename = '{f}.{e}'.format(f=image_name, e=image_type)
        image_metadata = {'filename': image.filename, 'type': image_type}
        image_metadata['transform'] = transform
        if not os.path.exists(directory):
            os.makedirs(directory)
            pathname = os.path.join(directory, filename)
            with open(pathname, 'w') as outfile:
                json.dump(image_metadata, outfile)
        return True

    def get_image(self, image_id, image_type, transform=None):
        directory = os.path.join(self.UPLOAD_FOLDER, image_id[:2])
        if transform:
            image_name = '{i}_{t}'.format(i=image_id, t=transform)
        else:
            image_name = image_id
        filename = '{f}.{e}'.format(f=image_name, e=image_type)
        pathname = os.path.join(directory, filename)
        if not os.path.exists(pathname):
            return False
        with open(pathname, 'r') as infile:
            return json.load(infile)
