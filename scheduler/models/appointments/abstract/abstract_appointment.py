import json
from abc import ABC
from datetime import datetime, timedelta

class AbstractAppointment(ABC):
    def __init__(self, start_time, duration=None, name=None):
        self.name = name
        self.duration = duration

        self.start_dt = start_time
        self.end_dt = self.start_dt + timedelta(minutes=duration)

    def render(self):
        start_date = datetime.strftime(self.start_dt, '%m/%d/%Y %H:%M')
        end_date = datetime.strftime(self.end_dt, '%m/%d/%Y %H:%M')
        print('----------')
        print(f'Start: {start_date}')
        print(f'End: {end_date}')
        print(f'Type: {self.name}')
        print('----------')
