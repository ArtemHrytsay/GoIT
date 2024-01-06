from datetime import date, datetime, timedelta
from collections import defaultdict

# .strftime('%Y-%m-%d')

def get_birthdays_per_week(users):
   
    birthdays = defaultdict(list)
    current_date = date(2023, 12, 30)
    days_of_week = [(current_date + timedelta(days=i)) for i in range(0, 7)]
    print()

    for user in users:
        bd_date = user["birthday"]
        
        if current_date.weekday() == 0:
            weekend = [(current_date + timedelta(days=i-2)) for i in range(0, 2)]
            print(bd_date in weekend)
            if bd_date in weekend:
                birthdays["Monday"].append(user["name"])

        if bd_date in days_of_week:
            if bd_date.weekday() == 0:
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


print(get_birthdays_per_week(users = [
        {"name": "Jan Koum", "birthday": datetime(2024, 1, 3).date()},
        {"name": "Peter", "birthday": datetime(2024, 1, 7).date()}
    ]))