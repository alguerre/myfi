from datetime import date, timedelta
from random import sample, gauss
from typing import List

import pandas as pd


years = list(range(2018, 2023))
mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def generate_fix_expense(
    initial_value: float, yearly_increment: float, concept: str, day: int = 1
) -> pd.DataFrame:
    amount = initial_value
    data = {"date": [], "amount": []}

    for year in years:
        for month in range(1, 13):
            data["date"].append(date(year, month, day))
            data["amount"].append(amount)
        amount *= yearly_increment

    data = pd.DataFrame(data)
    data["concept"] = concept
    return data


def generate_variable_expense(
    mean_value: float,
    std_value: float,
    concepts: List[str],
    monthly_frequency: int,
) -> pd.DataFrame:
    data = {"date": [], "amount": [], "concept": []}

    for year in years:
        for month in range(1, 13):
            days = sorted(sample(range(1, mdays[month]), monthly_frequency))

            for day in days:
                try:
                    data["date"].append(date(year, month, day))
                except ValueError:
                    print(year, month, day)
                data["amount"].append(-abs(gauss(mean_value, std_value)))
                data["concept"].append(sample(concepts, 1)[0])

    return pd.DataFrame(data)


def generate_eventual_expense(date_: date, amount: float, concept: str):
    data = {"date": [date_], "amount": [amount], "concept": [concept]}
    return pd.DataFrame(data)


def generate_travel(start: date, finish: date):
    flights = pd.concat(
        [
            generate_eventual_expense(start, gauss(-200, 10), "Skyline Airways"),
            generate_eventual_expense(finish, gauss(-180, 10), "Oceanic Airlines"),
        ]
    )

    num_days = (finish - start).days
    days = [start + timedelta(days=i) for i in range(num_days)]
    hotel_names = ["King's Bliss Hotel", "Cozy Hotel", "Deluxe Hotel"]
    hotels = pd.concat(
        [
            generate_eventual_expense(d, gauss(-60, 20), sample(hotel_names, 1)[0])
            for d in days
        ]
    )

    return pd.concat([flights, hotels])


def salary() -> pd.DataFrame:
    return generate_fix_expense(2000, 1.2, "Acme Corporation")


def gym() -> pd.DataFrame:
    return generate_fix_expense(-50, 1.1, "Hulking Center", 3)


def electricity() -> pd.DataFrame:
    return generate_fix_expense(-30, 2, "Electricity", 28)


def internet() -> pd.DataFrame:
    return generate_fix_expense(-20, 0, "Internet", 5)


def rental() -> pd.DataFrame:
    return generate_fix_expense(-800, 1.04, "TRANSFER TO MR. HOUSE HOLDER")


def netflix() -> pd.DataFrame:
    return generate_fix_expense(-15, 0, "netflix")


def secret() -> pd.DataFrame:
    return generate_fix_expense(-50, 0, "secret payment")


def supermarket() -> pd.DataFrame:
    return generate_variable_expense(
        -40, 10, ["Yum Market", "Yums N Food", "Marineara"], 10
    )


def restaurant() -> pd.DataFrame:
    return generate_variable_expense(
        -20, 5, ["The Hungry Harvest", "Bistro Captain", "Deli Feast"], 6
    )


def cinema() -> pd.DataFrame:
    return generate_variable_expense(-12, 0, ["Yum Popcorn Horizon", "Cinemasi"], 2)


def transport() -> pd.DataFrame:
    return generate_variable_expense(-2, 0.5, ["Public bus", "Public train"], 20)


def gas() -> pd.DataFrame:
    return generate_variable_expense(-30, 5, ["Roadside Petrol", "Fun Gas"], 2)


def new_car() -> pd.DataFrame:
    return generate_eventual_expense(date(2021, 5, 10), -18300, "Opel Corsa")


def travels() -> pd.DataFrame:
    return pd.concat(
        [
            generate_travel(date(2019, 6, 10), date(2019, 6, 15)),
            generate_travel(date(2019, 9, 10), date(2019, 9, 15)),
            generate_travel(date(2020, 8, 10), date(2020, 8, 15)),
            generate_travel(date(2021, 6, 10), date(2021, 6, 15)),
            generate_travel(date(2021, 12, 10), date(2021, 12, 13)),
            generate_travel(date(2022, 3, 10), date(2022, 6, 12)),
        ]
    )


if __name__ == "__main__":
    movements = pd.concat(
        [
            salary(),
            gym(),
            electricity(),
            internet(),
            netflix(),
            secret(),
            rental(),
            supermarket(),
            restaurant(),
            cinema(),
            transport(),
            gas(),
            new_car(),
            travels(),
        ]
    )
    movements["origin"] = "dummy"
    movements = movements.sort_values(by=["date"]).reset_index(drop=True)
    movements["total"] = movements["amount"].cumsum()

    movements.to_csv("source_dummy_01012018_to_31122022.csv")
