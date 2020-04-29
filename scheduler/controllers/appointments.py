from datetime import datetime

from scheduler.models.appointments.tuneup import Tuneup
from scheduler.models.appointments.wheel_true_and_tuneup import WheelTrueAndTuneUp
from scheduler.models.appointments.hub_overhaul import HubOverhaul

APPOINTMENT_CLS_LOOKUP = {
    'hub_overhaul': HubOverhaul,
    'tuneup': Tuneup,
    'wheel_true_and_tuneup': WheelTrueAndTuneUp
}

# Appointments
# 1. create an appointment
# 2. attempt to save appointment to schedule

class AppointmentsController:
    def __init__(self, schedule):
        self.schedule = schedule

    def create(self, name, start_time):
        # format appointment name
        # convert 24 hour time str MM/DD/YYYY HH:MM to datetime
        formatted_name, formatted_start = self._validate_and_format(name, start_time)
        appointment_cls = APPOINTMENT_CLS_LOOKUP[formatted_name]

        appointment = appointment_cls(formatted_start, name=formatted_name)
        self.schedule.add(appointment)

        return appointment

    def _validate_and_format(self, name, start_time):
        formatted_name = self._validate_name(name)
        formatted_start = self._validate_start_time(start_time)

        return formatted_name, formatted_start

    @staticmethod
    def _validate_name(name):
        formatted_name = name.lower()
        if not formatted_name in list(APPOINTMENT_CLS_LOOKUP.keys()):
            raise Exception('Invalid appointment name')

        return formatted_name

    @staticmethod
    def _validate_start_time(time_str):
        try:
            return datetime.strptime(time_str, '%m/%d/%Y %H:%M')
        except Exception as e:
            raise Exception(f'Invalid start time: {e}')
