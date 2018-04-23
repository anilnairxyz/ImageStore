# -*- coding: utf-8 -*-
"""
A flask microservice API that:
    - Can receive an uploaded image and return a unique identifier
    - Retrieve an uploaded image using the identifier
    - Retrieve other file types (transformations from the original)
      using the same identified (different file type parameter)
For this microservice we do not deal with images directly but only 
use image metadata to mock operations on images
"""
import logging
import uuid
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request, jsonify, make_response
from fs_interface import Storage

ALLOWED_TYPES = ('jpg', 'png', 'bmp', 'gif')

app = Flask(__name__)
storage = Storage()


def _image_check(image_type):
    """
    Check whether the file is really a valid image.
    Here we are only checking the extension of the file
    """
    if image_type in ALLOWED_TYPES:
        return True
    return False

@app.route('/upload', methods=['POST'])
def upload():
    """
    Upload an image into the image store
    The web service returns a JSON response:
        500:
            Server failure to store image
        415:
            Unsupported image file type
        200:
            Image succesfully uploaded and ID generated
    """
    try:
        image = request.get_json()
        image_name = image.get('filename')
        image_type = image.get('type')
        transform = image.get('transform')
        image_id = image.get('id')
        if not (image and _image_check(image_type)):
            raise TypeError
        if not image_id:
            image_id = str(uuid.uuid4())
        if not storage.save_image(image_name, image_type, image_id, transform):
            raise Exception
        response = {'image ID': image_id, 'status': 'OK'}
        response['message'] = 'Image succesfully uploaded'
        return make_response(jsonify(response), 200)
    except TypeError:
        response = {'status': 'Error'}
        response['message'] = 'Unsupported file type'
        app.logger.info(response['message'])
        return make_response(jsonify(response), 415)
    except Exception as e:
        response = {'status': 'Error'}
        response['message'] = 'Failed to upload image'
        app.logger.error(e)
        return make_response(jsonify(response), 500)

@app.route('/download/<image_id>', methods=['GET'])
def download(image_id):
    """
    Download an uploaded image from the image store
    The web service returns a JSON response:
        500:
            Server failure to download image
        415:
            Unsupported image file type
        404:
            File not found
        200:
            Image succesfully uploaded and ID generated
    """
    try:
        image_type = request.args.get('type')
        transform = request.args.get('transform')
        if image_type not in ALLOWED_TYPES:
            raise TypeError
        image = storage.get_image(image_id, image_type, transform)
        if not image:
            raise ValueError
        response = {'image': image, 'status': 'OK'}
        response['message'] = 'Image succesfully downloaded'
        return make_response(jsonify(response), 200)
    except TypeError:
        response = {'status': 'Error'}
        response['message'] = 'Image type not specified'
        app.logger.info(response['message'])
        return make_response(jsonify(response), 415)
    except ValueError:
        response = {'status': 'Error'}
        response['message'] = 'Image not found'
        app.logger.info(response['message'])
        return make_response(jsonify(response), 404)
    except Exception as e:
        response = {'status': 'Error'}
        response['message'] = 'Failed to download image'
        app.logger.error(e)
        return make_response(jsonify(response), 500)

@app.errorhandler(404)
def url_not_found(error):
    """
    Custom JSON error handler for 404 response
    """
    response = {'status': 'Error', 'message': 'URL not found'}
    app.logger.error(response['message'])
    return make_response(jsonify(response), 404)


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Custom JSON error handler for 405 response
    """
    response = {'status': 'Error', 'message': 'Method not allowed'}
    app.logger.error(response['message'])
    return make_response(jsonify(response), 405)


@app.route("/healthcheck", methods=['GET'])
def healthcheck():
    """
    Basic healthcheck
    """
    response = {'status': 200, 'message': 'Connection fine'}
    return make_response(jsonify(response), 200)


if __name__ == '__main__':
    logfile = 'log/app.log'
    handler = TimedRotatingFileHandler(logfile, when='midnight', interval=1)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=8000)
