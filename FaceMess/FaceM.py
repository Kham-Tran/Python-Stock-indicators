import fbchat
import getpass
import pandas as p
username = "kayler.tran.thanh@gmail.com"
password = "Asdfghjkl0)"


def login():
    session = p.read_json('session.json')
    return session


def logout():
    pass


def message():
    pass


print((login().to_string()))
