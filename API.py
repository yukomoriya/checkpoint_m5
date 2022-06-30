import requests

def get_phone(name):
    r = requests.get(f'http://localhost:5000/api?action=phone&name={name}')
    return r.text

def get_name(phone):
    r = requests.get(f'http://localhost:5000/api?action=name&phone={phone}')
    return r.text