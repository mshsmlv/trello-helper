#!/usr/bin/env python3

import requests
import json
import re

from datetime import datetime, timedelta
    
from config import *

def get_label_id(label_color):
    board_id = get_board()["id"]
    data = {
        "fields": "id,color",
        "key": key,
        "token": token,
    }
    labels = json.loads(requests.request(
                    "GET",
                    "https://api.trello.com/1/boards/{}/labels".format(board_id),
                    params=data
                ).text)
    for label in labels:
        if label_color == label["color"]:
            return label["id"]
    return ""


def generate_day_names():
    today = datetime.now()
    day_number = today.weekday()
    days = weekdays + off_days
    for i in range(7):
        days[day_number] = days[day_number] + " {:02d}.{:02d}".format(today.day, today.month)
        day_number = (day_number + 1)%7
        today = today + timedelta(days=1)
    return days

def get_board():
    data = {
        "fields": "id,name",
        "key": key,
        "token": token,
    }
    board = json.loads(
        requests.request(
            "GET", 
            "https://api.trello.com/1/boards/{}/".format(board_url), 
            params=data).text
        )
    return board


def get_board_lists():
    data = {
        "fields": "id,name",
        "key": key,
        "token": token,
    }
    lists = json.loads(
        requests.request(
        "GET", 
        "https://api.trello.com/1/boards/{}/lists".format(board_url), 
        params=data).text
        )    
    return lists


def check_card_existance(card, cards):
    for c in cards:
        if c["name"] == card["name"]:
            return True
    return False


def add_routine():
    lists = get_board_lists()
    for lst in lists:
        data = {
            "key": key,
            "token": token,
            "fields": "id,name",        
        }
        cards = json.loads(
            requests.request(
                "GET", 
                "https://api.trello.com/1/lists/{}/cards".format(lst["id"]), 
                params=data).text
            )
        day_name = lst["name"].split()[0]
        if day_name in weekdays:
            for routine in weekday_routine + daily_routine:
                if not check_card_existance(routine, cards):
                    data = {
                        "key": key,
                        "token": token,
                        "idList": lst["id"],
                        "name": routine["name"],
                        "idLabels": get_label_id(routine["idLabels"]),
                        "keepFromSource": "all",
                    }
                    requests.request("POST", "https://api.trello.com/1/cards", params=data)
        elif day_name in off_days:
            for routine in daily_routine:
                if not check_card_existance(routine, cards):
                    data = {
                        "key": key,
                        "token": token,
                        "idList": lst["id"],
                        "name": routine["name"],
                        "idLabels": get_label_id(routine["idLabels"]),
                        "keepFromSource": "all",
                    }
                    requests.request("POST", "https://api.trello.com/1/cards", params=data)


def get_calendar_tasks(lists):
    calendar_tasks = {}
    for lst in lists:
        if lst["name"] in inbox_list_name:
            url = "https://api.trello.com/1/lists/{}/cards".format(lst["id"])
            data = {
                "fields":"id,due",
                "key":key,
                "token": token,
            }
            cards = json.loads(requests.request("GET", url, params=data).text)
            for card in cards:
                if card["due"] != None:
                    due = re.findall("-[\d]{2}-[\d]{2}", card["due"])
                    if len(due) > 0:
                        _, month, day = due[0].split("-")
                        calendar_tasks["{}.{}".format(day, month)] = card["id"]
            continue
    return calendar_tasks


def set_calendar_task(day, calendar_tasks, lst):
    date = day[-5:]
    if date in calendar_tasks.keys():
        data = {
            "key": key,
            "token": token,
            "idList": lst["id"]
        }
        response = requests.request(
            "PUT", 
            "https://api.trello.com/1/cards/{}".format(calendar_tasks[date]), 
            params=data
            )


def days_settings():
    days = generate_day_names()
    board = get_board()
    lists = get_board_lists()
    calendar_tasks = get_calendar_tasks(lists)

    for lst in lists:
        for day in days:
            if lst["name"].split()[0] in day:
                url = "https://api.trello.com/1/lists/{}/name/".format(lst["id"], day) 
                data = {
                    "key": key,
                    "token": token,
                    "value": day,
                }
                response = requests.request("PUT", url, params=data)
                set_calendar_task(day, calendar_tasks, lst)
                break
               

if __name__=="__main__":
    add_routine()
    days_settings()
