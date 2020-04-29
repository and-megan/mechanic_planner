from scheduler.models.appointments.abstract.abstract_appointment import AbstractAppointment

DURATION = 60
APPOINTMENT_NAME = 'hub_overhaul'

class HubOverhaul(AbstractAppointment):
    def __init__(self, start_time, duration=DURATION, name=APPOINTMENT_NAME):
        super().__init__(start_time, duration=duration, name=name)
