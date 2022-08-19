from datetime import datetime, date


class Date:
    def __init__(self, value: str) -> None:
        self.value = value

    def str_to_date(self) -> date:
        tdatetime = datetime.strptime(self.value, '%Y-%m-%d HH:MM:ss')
        tdate = date(tdatetime.year, tdatetime.month)
        return tdate
