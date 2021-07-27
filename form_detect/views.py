from django.shortcuts import render
from django.shortcuts import HttpResponse
from tinydb import TinyDB, Query
import os
import datetime
import re
import json

def is_date(text):
    try:
        datetime.datetime.strptime(text, '%Y-%m-%d')  # DD.MM.YYYY or YYYY-MM-DD
        return True
    except:
        try:
            datetime.datetime.strptime(text, '%d.%m.%Y')  # DD.MM.YYYY or YYYY-MM-DD
            return True
        except:
            return False


def is_phone(text):
    if len(text) != 16:
        return False
    if text[0] != "+" or text[2] != " " or text[6] != " " or text[10] != " " or text[13] != " ":
        print("simbol")
        return False
    phone_num = re.sub(r'\D', '', text)
    result = re.match(r'^[78]?\d{10}$', phone_num)
    return (bool(result))


def is_email(text):
    result = re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', text)
    return (bool(result))


def index(request, value_1, value_2):
    data = {}
    path_to_db = os.getcwd() + os.sep + "form_detect" + os.sep + "db.json"
    try:
        db = TinyDB(path_to_db)
    except:
        db = None
        print("DB not fount")



    response_data = ["text", "text"]
    if is_date(value_1):
        response_data[0] = "date"
    elif is_phone(value_1):
        response_data[0] = "phone"
    elif is_email(value_1):
        response_data[0] = "email"

    if is_date(value_2):
        response_data[1] = "date"
    elif is_phone(value_2):
        response_data[1] = "phone"
    elif is_email(value_2):
        response_data[1] = "email"

    for item in db:
        vals = []
        for k, v in item.items():
            print(k)
            if k == "name":
                form_name = v

                continue
            else:
                vals.append(v)
        if vals[0] == response_data[0] and vals[1] == response_data[1]:
            data["name"] = form_name


    if len(data) == 0:
        data = {
            "f_name1": response_data[0],
            "f_name2": response_data[1],
        }

    data = json.dumps(data)
    return HttpResponse(data)
