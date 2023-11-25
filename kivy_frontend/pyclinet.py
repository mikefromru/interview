import requests
url = 'http://iammike.pythonanywhere.com/api/'
r = requests.get(url + '/app/subjects/')
print(r.json())

