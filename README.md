# Mechanic Planner

## Description
This is a simple command line program that allows a single bike mechanic to
1. Book 3 types of appointments: tuneup, hub overhaul, and wheel true & tuneup (bike mechanic refuses to do a wheel true without a tuneup)
2. List all appointments (ordered by date & time)

## How to run the command line program
1. Ensure Python3+ is installed on the machine.
2. `cd mechanic_planner/`
3. run `python main.py`
4. Enter valid prompts

**available prompts**
1. list - lists all appointments sorted by date & time (asc)
2. exit - exits program
3. schedule - schedules an appointment
  * required arguments:
    * --s / -start MM/DD/YYYY HH:MM (Note: 24 hour time required).
      * e.g. 04/11/2020 14:00
    * --t / -type type of appointment to book
      * valid values: tuneup, wheel_true_and_tuneup, hub_overhaul

## How to run tests
- `python -m unittest discover test/`

## Code Description
This program is written with Python 3.7.

`main.py`
Starting with `main.py`, `argparse` is used to process input from the command line. Errors are handled and displayed in the console.

`scheduler/controllers/appointments/py`
This controller is responsible for taking the input from the `Schedule` cmd on the command line. It validates and formats the given start string & appointment type. It finds the correct appointment class and creates an instance. The controller attempts to insert the new appointment in the `Schedule` singleton.

`scheduler/models/schedule.py`
`main.py` imports `Schedule` as a singleton. The `Schedule` instance holds all of the appointments. Appointments are sharded by day, e.g. (pseudocode): `{ 04/01/2020: [{tuneup, 11:30}, {tuneup, 13:00}] }`. Each of the shards are sorted by time. I chose to implement the schedule this way so that I didn't need to rely on hardcoding 15 min increments to check for overlapping appointments. Since I decided to not hardcode the increments, I need to iterate through all the appointments to see if a proposed appointment overlaps with an existing appointment. By sharding the appointments by day, I reduce the number of appointments to increment over.

`scheduler/appointments/*`
The base class for all appointments is `AbstractAppointment`, which simply consists of an object with a name (appointment type), start_dt (in python datetime), end_dt, and duration (in minutes).
I added a simple "render" method so that we can view the appointment in the console easily.

`AbstractAggregateAppointment` inherits from `AbstractAppointment`.

`Tuneup` inherits from `AbstractAppointment`. `WheelTrue` also inherits from `AbstractAppointment`.

### Notable Decisions
One tricky case in the Schedule logic to handle was the edge case where an appointment begins on Day 1 and ends on Day 2. This is unlikely to happen in the real world. I chose to insert this edge case appointment into both the starting and ending day shards. When `index` is called on schedule to return all of the appointments, I dedupe the appointment using an OrderedSet. I use an OrderedSet to preserve the ordered nature of the shards.

`AbstractAggregateAppointment` inherits from `AbstractAppointment`. The difference is that the aggregate appointment has an attribute `sub_appointments` which is an array of `AbstractAppointments`. `duration` is calculated by summing up the duration of each sub_appointment. This will easily allow future changes to appointments. I can imagine a bike mechanic wanting to book an appointment made up of "FlatFix", "Tuneup", and "HubOverhaul". This architecture will allow that change easily.

Although the `WheelTrue` class isn't used as a first class Appointment, I chose to create it as a standalone class. That way, it can be easily repurposed to be used a first class appointment or be used as part of a combo of appointments to make up a new `AbstractAggregateAppointment`.

This command line program allows you to schedule appointments in the past. Walk-ins would need to be "back-scheduled". I have also known contractors to want to switch around a few appointment times after the fact in order to balance their books.

## Test run log
```
megan@Megans-Air:~/Projects/mechanic_planner on$ python main.py
Welcome!
What would you like to do?
schedule --type tuneup --start 4/28/2020 10:00
Namespace(cmd='schedule', start=['4/28/2020', '10:00'], type='tuneup')
Appointment created:
----------
Start: 04/28/2020 10:00
End: 04/28/2020 10:30
Type: tuneup
----------
What would you like to do?
schedule --type hub_overhaul --start 4/28/2020 11:00
Namespace(cmd='schedule', start=['4/28/2020', '11:00'], type='hub_overhaul')
Appointment created:
----------
Start: 04/28/2020 11:00
End: 04/28/2020 12:00
Type: hub_overhaul
----------
What would you like to do?
list
Namespace(cmd='list', start=None, type=None)
All appointments (ordered by date & time):
----------
Start: 04/28/2020 10:00
End: 04/28/2020 10:30
Type: tuneup
----------
----------
Start: 04/28/2020 11:00
End: 04/28/2020 12:00
Type: hub_overhaul
----------
```

## Test run log - overlapping appointments
```
megan@Megans-Air:~/Projects/mechanic_planner on$ python main.py
Welcome!
What would you like to do?
schedule --type hub_overhaul --start 4/28/2020 11:00
Namespace(cmd='schedule', start=['4/28/2020', '11:00'], type='hub_overhaul')
Appointment created:
----------
Start: 04/28/2020 11:00
End: 04/28/2020 12:00
Type: hub_overhaul
----------
What would you like to do?
schedule --type hub_overhaul --start 4/28/2020 11:30
Namespace(cmd='schedule', start=['4/28/2020', '11:30'], type='hub_overhaul')
Existing appointments:
----------
Start: 04/28/2020 11:00
End: 04/28/2020 12:00
Type: hub_overhaul
----------
Error: Overlapping appointment(s) already exist
What would you like to do?
schedule --type hub_overhaul --start 4/28/2020 12:00
Namespace(cmd='schedule', start=['4/28/2020', '12:00'], type='hub_overhaul')
Appointment created:
----------
Start: 04/28/2020 12:00
End: 04/28/2020 13:00
Type: hub_overhaul
----------
What would you like to do?
list
Namespace(cmd='list', start=None, type=None)
All appointments (ordered by date & time):
----------
Start: 04/28/2020 11:00
End: 04/28/2020 12:00
Type: hub_overhaul
----------
----------
Start: 04/28/2020 12:00
End: 04/28/2020 13:00
Type: hub_overhaul
----------
```
## Test run log - invalid inputs
```
megan@Megans-Air:~/Projects/mechanic_planner on$ python main.py
Welcome!
What would you like to do?
banana
usage: SCHEDULER [-h] [-t {tuneup,wheel_true_and_tuneup,hub_overhaul}]
                 [-s START [START ...]]
                 {schedule,list,exit}
SCHEDULER: error: argument cmd: invalid choice: 'banana' (choose from 'schedule', 'list', 'exit')
What would you like to do?
schedule -t tuneup
Namespace(cmd='schedule', start=None, type='tuneup')
Error: Start time of appointment not included. Missing --start arg.
What would you like to do?
schedule -t tacocat -s 4/28/2020 11:15
usage: SCHEDULER [-h] [-t {tuneup,wheel_true_and_tuneup,hub_overhaul}]
                 [-s START [START ...]]
                 {schedule,list,exit}
SCHEDULER: error: argument -t/--type: invalid choice: 'tacocat' (choose from 'tuneup', 'wheel_true_and_tuneup', 'hub_overhaul')
What would you like to do?
schedule -t hub_overhaul -s 4/28/2020 11:15
Namespace(cmd='schedule', start=['4/28/2020', '11:15'], type='hub_overhaul')
Appointment created:
----------
Start: 04/28/2020 11:15
End: 04/28/2020 12:15
Type: hub_overhaul
----------
What would you like to do?
schedule -t hub_overhaul -s 4/28 11:15
Namespace(cmd='schedule', start=['4/28', '11:15'], type='hub_overhaul')
Error: Invalid start time: time data '4/28 11:15' does not match format '%m/%d/%Y %H:%M'
What would you like to do?
exit
Namespace(cmd='exit', start=None, type=None)
Goodbye!
```