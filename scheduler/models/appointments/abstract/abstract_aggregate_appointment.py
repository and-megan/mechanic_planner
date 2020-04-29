from abc import ABC
from scheduler.models.appointments.abstract.abstract_appointment import AbstractAppointment

class AbstractAggregateAppointment(AbstractAppointment, ABC):
    def __init__(self, sub_appointments, start_time, name):
        self.sub_appointments = sub_appointments

        duration = 0
        for appointment in sub_appointments:
            duration += appointment.duration

        super().__init__(start_time, duration=duration, name=name)
