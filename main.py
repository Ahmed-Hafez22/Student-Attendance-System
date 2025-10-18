from libs import *
from DatabaseFunctions import *

insert_date()
make_attendance_dict()
while True:
    take_attendance()
    statement = input("Want to Exit: ")
    if statement == "y":
        break
    else:
        pass