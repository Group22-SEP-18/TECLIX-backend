## TECLIX-backend
### Deployed url
https://teclix.herokuapp.com/
### Guide
clone the repository using the HTTPS link
### Environment setup
```bash
$ python -m virtualenv teclixenv
$ source teclixenv/Scripts/activate
```
After the environment is created and activated, install the necessary dependencies using the [requirements.txt](requirements.txt) file.
```bash
$ pip install -r requirements.txt 
```
To run the project.
```bash
$ python manage.py runserver 
```
To reset the database.
```bash
$ python manage.py reset_db 
```
