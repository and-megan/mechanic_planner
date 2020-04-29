import unittest

from scheduler.controllers.appointments import AppointmentsController
from scheduler.models.appointments.tuneup import Tuneup
from scheduler.models.schedule import Schedule


class TestAppointmentsController(unittest.TestCase):
    def setUp(self):
        self.schedule = Schedule()
        self.appointments_controller = AppointmentsController(self.schedule)

    def test_create(self):
        start_str = '04/01/2020 11:30'
        appt_type = 'tuneup'

        appt = self.appointments_controller.create(appt_type, start_str)

        self.assertEqual(type(appt), Tuneup)

    def test_create_with_invalid_time(self):
        start_str = '04/11/2020 25:00'
        appt_type = 'tuneup'

        with self.assertRaises(Exception) as cm:
            self.appointments_controller.create(appt_type, start_str)

        self.assertIn('Invalid start time', str(cm.exception))

    def test_create_with_invalid_appointment_type(self):
        start_str = '04/01/2020 11:30'
        appt_type = 'tacocat'

        with self.assertRaises(Exception) as cm:
            self.appointments_controller.create(appt_type, start_str)

        self.assertEqual(str(cm.exception), 'Invalid appointment name')

    def test_create_with_overlapping_appointment(self):
        start_str = '04/01/2020 11:30'
        appt_type = 'tuneup'
        self.appointments_controller.create(appt_type, start_str)

        pending_str = '04/01/2020 11:45'

        with self.assertRaises(Exception) as cm:
            self.appointments_controller.create(appt_type, pending_str)

        self.assertEqual(
            str(cm.exception), 'Overlapping appointment(s) already exist')

    def test_create_wheel_true_and_tuneup(self):
        start_str = '04/01/2020 11:30'
        appt_type = 'wheel_true_and_tuneup'

        appt = self.appointments_controller.create(appt_type, start_str)
        sub_appts = appt.sub_appointments
        sub_appt_names = [appt.name for appt in sub_appts]
        sub_appt_durations = [appt.duration for appt in sub_appts]

        self.assertEqual(appt.duration, 60)
        self.assertEqual(sorted(sub_appt_names), ['tuneup', 'wheel_true'])
        self.assertEqual(sub_appt_durations, [30, 30])

    def test_create_back_to_back_appointments(self):
        s_and_h_start = '04/01/2020 11:30'
        s_and_h_appt = 'wheel_true_and_tuneup'

        wheel_true_and_tuneup = self.appointments_controller.create(
            s_and_h_appt, s_and_h_start)

        tuneup_start = '04/01/2020 12:30'
        tuneup_appt = 'tuneup'
        tuneup = self.appointments_controller.create(tuneup_appt, tuneup_start)

        self.assertIsNotNone(wheel_true_and_tuneup)
        self.assertIsNotNone(tuneup)


if __name__ == '__main__':
    unittest.main()
