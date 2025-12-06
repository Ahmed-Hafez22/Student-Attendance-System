# from libs import *
# from DatabaseFunctions import *


# def update_time():
#     today = datetime.now()
#     return today


# intiationTime = update_time()
# endTime = datetime.strptime("15:00", "%H:%M").replace(
#     year=intiationTime.year, month=intiationTime.month, day=intiationTime.day
# )

# insert_date()

# latestDay = database_cursor.execute(
#     """
#         SELECT Date FROM DateTable WHERE id = (SELECT MAX (id) FROM DateTable)
# """
# ).fetchone()[0]

# latestDay = datetime.strptime(latestDay, "%Y-%m-%d").replace(hour=intiationTime.hour, minute=intiationTime.minute)

# make_attendance_dict()

# while(True):
#     updateTime = update_time()
#     latestDay = latestDay.replace(hour=updateTime.hour, minute=updateTime.minute)

#     if(latestDay > endTime):
#         break
#     else:
#         take_attendance()

# # get_subject_percentage(intiationTime.day, intiationTime.month, intiationTime.year, "CF225")
