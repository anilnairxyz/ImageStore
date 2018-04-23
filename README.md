# Basic Image Hosting Service

## Microservices
This includes two microservices in 2 separate Git repositories
- ImageStore
- [ImageCompress](https://github.com/anilnairxyz/ImageCompress)

![ImageStore Implementation](https://github.com/anilnairxyz/Geoview/blob/master/ImageStore1.png)

###The ImageStore microservice:
- Receives an uploaded image and returns a unique identifier which can then be used to retrieve the image
- Different image formats can be returned by using different extensions against the image ID
- Different image tarnsformations can be download using the image ID

###The ImageCompress microservice:
- Calls the `ImageStore` service to retrieve the image using Image ID
- Compresses the image
- Calls the `ImageStore` service to 

## To run
```pip install -r requirements.txt```<br>
```mkdir log```<br>
```python app.py```<br>

## To Test
```curl -X GET http://localhost:8000/```
