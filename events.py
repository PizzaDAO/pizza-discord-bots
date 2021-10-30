import datetime
from utils import get_random_hype_msg


class PizzaDaoEvent:

    def __init__(self, month, day, name, enabled=True):
        self.month = month
        self.day = day
        self.name = name
        self.enabled = enabled
        self.today = datetime.date.today()
        self.event_date = datetime.date(self.today.year, self.month, self.day)

    def days_until_event(self) -> int:
        return (self.event_date - self.today).days

    def message(self) -> str:
        return f"Hello everyone! Today is {self.today}, which means there are **{self.days_until_event()} DAYS until {self.month} {self.day}, {self.today.year}**, {self.name}! {get_random_hype_msg()}"
