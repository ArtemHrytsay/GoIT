from datetime import date, datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):

    birthdays = defaultdict(list)
    current_date = date.today()
    days_of_week = [(current_date + timedelta(days=i)) for i in range(0, 7)]

    for user in users:
        bd_date = user["birthday"]
        
        if bd_date < current_date:
            bd_date = bd_date.replace(year=current_date.year + 1)
            
        if current_date.weekday() == 0:
            days_of_week = [(current_date + timedelta(days=i-2)) for i in range(0, 7)]

        if bd_date in days_of_week:
            if bd_date.weekday() == 0 or bd_date.weekday() == 5 or bd_date.weekday() == 6:
                birthdays["Monday"].append(user["name"])
            if bd_date.weekday() == 1:
                birthdays["Tuesday"].append(user["name"])
            if bd_date.weekday() == 2:
                birthdays["Wednesday"].append(user["name"])
            if bd_date.weekday() == 3:
                birthdays["Thursday"].append(user["name"])
            if bd_date.weekday() == 4:
                birthdays["Friday"].append(user["name"])

    return birthdays