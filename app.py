# -*- coding: utf-8 -*-
"""
A flask microservice API that:
    - Can receive an uploaded image and return a unique identifier
"""
import logging
import os # may not be needed here
import uuid
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request, jsonify, make_response

UPLOAD_FOLDER = '/Users/anilnair/Repos/ImageStore/tmp' # may not be needed here
ALLOWED_EXTENSIONS = ('.jpg', '.png', '.bmp', '.gif')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # may not be needed here


def _image_check(filename):
    """
    Check whether the file is really a valid image.
    Here we are only checking the extension of the file
    """
    if filename.lower().endswith(ALLOWED_EXTENSIONS):
        return True
    return False

@app.route('/', methods=['POST'])
def load():
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
    if request.method == 'POST':
        image = request.files['image']
        if image and _image_check(image.filename):
            try:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
                image_id = str(uuid.uuid4())
                response = {'image ID': image_id, 'status': 'OK'}
                response['message'] = 'Image succesfully uploaded'
                return make_response(jsonify(response), 200)
            except Exception:
                response = {'status': 'Error'}
                response['message'] = 'Failed to upload image'
                app.logger.error(response['message'])
        else:    
            response = {'status': 'Error'}
            response['message'] = 'Unsupported file type'
            app.logger.warning(response['message'])
            return make_response(jsonify(response), 400)


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


if __name__ == '__main__':
    logfile = 'log/api.log'
    handler = TimedRotatingFileHandler(logfile, when='midnight', interval=1)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=8000)
