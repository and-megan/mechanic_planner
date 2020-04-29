import unittest

from scheduler.controllers.appointments import AppointmentsController
from scheduler.models.schedule import Schedule


class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.schedule = Schedule()
        self.appointments_controller = AppointmentsController(self.schedule)

    def test_index(self):
        # test that appointments are returned in order of date & time
        # regardless of creation order
        appt_type = 'tuneup'

        second_start_str = '04/01/2020 13:30'
        second_appt = self.appointments_controller.create(
            appt_type, second_start_str)

        first_start_str = '03/31/2020 10:45'
        first_appt = self.appointments_controller.create(
            appt_type, first_start_str)

        third_start_str = '04/01/2020 15:45'
        third_appt = self.appointments_controller.create(
            appt_type, third_start_str)

        all_appts = self.schedule.index()

        self.assertEqual(all_appts, [first_appt, second_appt, third_appt])


    def test_index_does_not_return_duplicate_appts(self):
        # in the case of an appointment that begins at 11:30PM day 1
        # and ends 12:30 day 2, return only 1 appointment
        start_str = '04/01/2020 23:30'
        appt_type = 'wheel_true_and_tuneup'

        appt = self.appointments_controller.create(appt_type, start_str)

        all_appts = self.schedule.index()

        self.assertEqual(all_appts, [appt])
