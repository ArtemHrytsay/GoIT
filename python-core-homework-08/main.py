from datetime import date, datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):
   
    birthdays = defaultdict(list)
    current_date = date.today()
    days_of_week = [(current_date + timedelta(days=i)) for i in range(0, 7)]


    for user in users:
        bd_date = user["birthday"]
        
        if current_date.weekday() == 0:
            weekend = [(current_date + timedelta(days=i-2)) for i in range(0, 2)]
            if bd_date in weekend:
                birthdays["Monday"].append(user["name"])
        if current_date.weekday() == 1:
            weekend_day = [current_date - timedelta(days=2)]
            if bd_date in weekend_day:
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


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
