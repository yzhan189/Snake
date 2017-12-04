import pyrebase

# Initialize Firebase
config = {
    "apiKey": "AIzaSyA_B0bRJjxAsVW_m5OC8xJqPkHazHI-cuA",
    "authDomain": "snake-ab217.firebaseapp.com",
    "databaseURL": "https://snake-ab217.firebaseio.com",
    "projectId": "snake-ab217",
    "storageBucket": "snake-ab217.appspot.com",
    "messagingSenderId": "196087795509"
}

firebase = pyrebase.initialize_app(config)