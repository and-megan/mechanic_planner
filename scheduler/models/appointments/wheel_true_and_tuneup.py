from datetime import timedelta

from scheduler.models.appointments.abstract.abstract_aggregate_appointment import AbstractAggregateAppointment
from scheduler.models.appointments.tuneup import Tuneup
from scheduler.models.appointments.wheel_true import DURATION as WHEEL_TRUE_DURATION, WheelTrue

APPOINTMENT_NAME = 'wheel_true_and_tuneup'

class WheelTrueAndTuneUp(AbstractAggregateAppointment):
    def __init__(self, start_time, name):
        sub_appointments = []
        sub_appointments.append(Tuneup(start_time))

        wheel_true_start_time = start_time + timedelta(minutes=WHEEL_TRUE_DURATION)
        sub_appointments.append(WheelTrue(wheel_true_start_time))

        super().__init__(sub_appointments, start_time, name=APPOINTMENT_NAME)
