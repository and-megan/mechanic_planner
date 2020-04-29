from collections import OrderedDict
from datetime import datetime

class Schedule:
    def __init__(self):
        # shard appointments by day
        self.appointments_by_day = {}
    
    def index(self):
        """
        Returns all appointments in order.
        Dedupe the appointments duplicated in overlapping days (edge case 11:30pm - 12:30am appts)
        """
        all_appointments = OrderedDict()
        sorted_days = sorted(list(self.appointments_by_day.keys()))

        for day in sorted_days:
            appts_for_day = self.appointments_by_day[day]
            for appt in appts_for_day:
                all_appointments[appt] = True
        
        return list(all_appointments.keys())

    def add(self, appointment):
        """
        Add an appointment to a day shard.
        If there is an overlapping appointment, raise Exception.
        """
        # if the appointment start & end days are not the same,
        # we will need to check/add two different schedule day shards
        start_day = self._truncate_dt_to_day(appointment.start_dt)
        end_day = self._truncate_dt_to_day(appointment.end_dt)

        overlapping_appts = self._find_overlapping_appointments(
            start_day, end_day, appointment.start_dt, appointment.end_dt)

        if overlapping_appts:
            print('Existing appointments:')
            for appt in overlapping_appts:
                appt.render()
            raise Exception(
                'Overlapping appointment(s) already exist')

        # add appointment to start day shard
        self._add_to_day_shard(start_day, appointment)

        if start_day != end_day:
            # add appointment to end day shard
            self._add_to_day_shard(end_day, appointment)

        return appointment
    
    def _add_to_day_shard(self, day, appointment):
        """
        Add an appointment to a day shard. If a shard doesn't exist, create one.
        """
        if self.appointments_by_day.get(day):
            self.appointments_by_day[day].append(appointment)
            appts = self.appointments_by_day[day]

            # sort day shard
            self.appointments_by_day[day] = sorted(
                appts, key=lambda x: x.start_dt)
        else:
            self.appointments_by_day[day] = [appointment]

    def _find_overlapping_appointments(self, start_day, end_day, appt_start_dt, appt_end_dt):
        overlaps = []

        start_overlap = self._find_overlapping_appointment(
            start_day, appt_start_dt, appt_end_dt)

        if start_overlap:
            overlaps.append(start_overlap)

        if start_day != end_day:
            # edge case where an appointment exists in two separate days
            # e.g. Monday 11:30pm - Tuesday 12:30am
            end_overlap = self._find_overlapping_appointment(
                end_day, appt_start_dt, appt_end_dt)
            if end_overlap:
                overlaps.append(end_overlap)

        return overlaps
    
    def _find_overlapping_appointment(self, day, pending_start_dt, pending_end_dt):
        """
        Checks if any appointment in the day shard overlaps with the pending appointment.
        It is acceptable for a pending appointment's start to equal existing appointment's end.
        It is acceptable for a pending appointment's end to equal an existing appointment's start.
        """
        day_appts = self.appointments_by_day.get(day, [])

        # day appts are sorted
        for appt in day_appts:
            if appt.start_dt <= pending_start_dt < appt.end_dt:
                # pending appointment start overlaps with existing appointment
                return appt
            elif appt.start_dt < pending_end_dt <= appt.end_dt:
                # pending appointment end overlaps with existing appointment
                return appt
            elif appt.end_dt < pending_start_dt:
                # passed by the appt_start_dt dt already and there is no overlap
                break

        return None

    @staticmethod
    def _truncate_dt_to_day(dt):
        """
        Truncate dt to day
        """
        return dt.replace(hour=0, minute=0)
