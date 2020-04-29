from scheduler.models.appointments.abstract.abstract_appointment import AbstractAppointment

DURATION = 30
APPOINTMENT_NAME = 'wheel_true'

class WheelTrue(AbstractAppointment):
    def __init__(self, start_time, duration=DURATION, name=APPOINTMENT_NAME):
        super().__init__(start_time, duration=duration, name=name)
