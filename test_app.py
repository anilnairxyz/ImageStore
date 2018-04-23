from app import app
from flask import json


class TestImageStore(object):
    def setUp(self):
        self.test_app = app.test_client()
        self.upload_url = '/upload'
        self.download_url = '/download'
        self.mandatory_args = ({'type': 'png'})
        self.jpg_image = {
                            'filename': 'sunset.jpg',
                            'type': 'jpg'
                         }
        self.png_image = {
                            'filename': 'trees.png',
                            'type': 'png'
                         }

    def test_image_upload(self):
        """
        Upload an image and test whether the response is a success
        """
        response = self.test_app.post(self.upload_url,
                                      data=json.dumps(self.jpg_image),
                                      content_type='application/json')
        assert json.loads(response.data)['status'] == 'OK'
        assert response.status_code == 200

    def test_image_download(self):
        """
        Upload an image; Obtain the unique identifier;
        Download the same image; Check attributes

        """
        response = self.test_app.post(self.upload_url,
                                      data=json.dumps(self.png_image),
                                      content_type='application/json')
        response_data = json.loads(response.data)
        image_id = response_data['image ID']
        assert response_data['status'] == 'OK'
        assert response.status_code == 200

        # Use the image ID in the download URL
        dn_url = '{u}/{i}'.format(u=self.download_url,
                                  i=image_id
                                 )
        response = self.test_app.get(dn_url, query_string=self.mandatory_args)
        response_data = json.loads(response.data)
        image_data = response_data['image']
        assert image_data['filename'] == self.png_image['filename']
        assert image_data['type'] == self.png_image['type']
        assert image_data['id'] == image_id
