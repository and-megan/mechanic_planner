import argparse

from scheduler.controllers.appointments import AppointmentsController
from scheduler.models.appointments.hub_overhaul import HubOverhaul
from scheduler.models.appointments.tuneup import Tuneup
from scheduler.models.appointments.wheel_true_and_tuneup import WheelTrueAndTuneUp
from scheduler.models.schedule import Schedule

VALID_APPTS = ['tuneup', 'wheel_true_and_tuneup', 'hub_overhaul']
VALID_CMDS = ['schedule', 'list', 'exit']


def _handle_list_cmd(schedule):
    print('All appointments (ordered by date & time):')
    all_appts = schedule.index()
    for appt in all_appts:
        appt.render()


def _handle_schedule_cmd(args, appointments_controller):
    try:
        _validate_schedule_args(args)
        _schedule_appointment(args, appointments_controller)
    except Exception as e:
        print(f'Error: {e}')


def _schedule_appointment(args, appointments_controller):
    # convert args.start from ["04/01/2020", "11:30"] to "04/01/2020 11:30"
    start_str = ' '.join(args.start)
    appt = appointments_controller.create(args.type, start_str)

    print('Appointment created:')
    appt.render()


def _validate_schedule_args(args):
    # ensure name & start arguments are present
    if not args.type:
        raise Exception(
            'Type of appointment not included. Missing --type arg.')

    if not args.start:
        raise Exception(
            'Start time of appointment not included. Missing --start arg.')

    return True


def main():
    running = True
    parser = argparse.ArgumentParser(
        prog='SCHEDULER', description='Simple command line program to create and display appointments.')
    parser.add_argument('cmd', choices=VALID_CMDS)
    parser.add_argument(
        '-t', '--type', help='type of appointment to book', choices=VALID_APPTS)
    parser.add_argument(
        '-s', '--start', help='start date & time of appointment in format "MM/DD/YYYY HH:MM" (24 hr time)', nargs='+')

    print('Welcome!')

    # used as singleton
    schedule = Schedule()
    appointments_controller = AppointmentsController(schedule)

    while running:
        astr = input('What would you like to do?\n')
        try:
            args = parser.parse_args(astr.split())
            print(args)
        except SystemExit:
            # handle argparse error
            continue

        if args.cmd == 'schedule':
            _handle_schedule_cmd(args, appointments_controller)

        elif args.cmd == 'list':
            _handle_list_cmd(schedule)

        elif args.cmd == 'exit':
            print('Goodbye!')
            running = False

    return None


if __name__ == '__main__':
    main()
