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

## To run both services on a local machine
- For ImageStore
```pip install -r requirements.txt```<br>
```export STORAGE_FOLDER=<path to your temp folder>```
``` mkdir <path to your temp folder>```
```mkdir log```<br>
```python app.py```<br>

- For ImageCompress
```pip install -r requirements.txt```<br>
```export STORE_URL=<url path to ImageStore service>```
```mkdir log```<br>
```python app.py```<br>

## To Test
```curl -H "Content-Type: application/json" -X POST -d '{"filename":"table.jpg","type":"jpg"}' http://localhost:8000/upload```
```curl http://0.0.0.0:8000/download/<image ID for table.jpg>\?type\=jpg```
```curl http://0.0.0.0:8000/compress/<image ID for table.jpg>\?type\=jpg```
```curl http://0.0.0.0:8000/download/<image ID for table.jpg>\?type\=jpg\&transform=compress```

## Docker
To run in Docker Containers use the following docker-compose.yml
```
version: '3'

services:
  store:
    build: './ImageStore'
    container_name: store
    ports:
      - 8000:8000
    environment:
      STORAGE_FOLDER: "/app/tmp"

  compress:
    build: './ImageCompress'
    ports:
      - 9000:9000
    links:
      - "store:imagestore"
    environment:
      STORE_URL: "http://store:8000"
```

## A more practical architecture

![ImageStore Implementation](https://github.com/anilnairxyz/Geoview/blob/master/ImageStore2.png)

