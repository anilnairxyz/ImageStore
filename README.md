# An image post / get flask microservice

This microservice:
- Receives an uploaded image and returns a unique identifier which can then be used to retrieve the image
- Different image formats can be returned by using different extensions against the image request URL

## To run
```pip install -r requirements.txt```<br>
```mkdir log```<br>
```python app.py```<br>

## To Test
```curl -X GET http://localhost:8000/```
