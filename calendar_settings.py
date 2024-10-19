
calendar_resources = [
    {"id": "a", "building": "Building A", "title": "Room A"},
    {"id": "b", "building": "Building A", "title": "Room B"},
    {"id": "c", "building": "Building B", "title": "Room C"},
    {"id": "d", "building": "Building B", "title": "Room D"},
    {"id": "e", "building": "Building C", "title": "Room E"},
    {"id": "f", "building": "Building C", "title": "Room F"},
]

def get_calendar_options(mode, calendar_options):
    if "resource" in mode:
        if mode == "resource-daygrid":
            calendar_options = {
                **calendar_options,
                "initialDate": "2023-07-01",
                "initialView": "resourceDayGridDay",
                "resourceGroupField": "building",
            }
        elif mode == "resource-timeline":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
                },
                "initialDate": "2023-07-01",
                "initialView": "resourceTimelineDay",
                "resourceGroupField": "building",
            }
        elif mode == "resource-timegrid":
            calendar_options = {
                **calendar_options,
                "initialDate": "2023-07-01",
                "initialView": "resourceTimeGridDay",
                "resourceGroupField": "building",
            }
    else:
        if mode == "daygrid":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "dayGridDay,dayGridWeek,dayGridMonth",
                },
                "initialDate": "2023-07-01",
                "initialView": "dayGridMonth",
            }
        elif mode == "timegrid":
            calendar_options = {
                **calendar_options,
                "initialView": "timeGridWeek",
            }
        elif mode == "timeline":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "timelineDay,timelineWeek,timelineMonth",
                },
                "initialDate": "2023-07-01",
                "initialView": "timelineMonth",
            }
        elif mode == "list":
            calendar_options = {
                **calendar_options,
                "initialDate": "2023-07-01",
                "initialView": "listMonth",
            }
        elif mode == "multimonth":
            calendar_options = {
                **calendar_options,
                "initialView": "multiMonthYear",
            }
    return calendar_options


# calendar_options = {
#     "editable": "true",
#     "selectable": "true",
#     "headerToolbar": {
#         "left": "today prev,next",
#         "center": "title",
#         "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
#     },
#     # "slotMinTime": "06:00:00",
#     # "slotMaxTime": "18:00:00",
#     # "initialView": "resourceTimelineDay",
#     # "resourceGroupField": "building",
#     # "resources": [
#     #     {"id": "a", "building": "Building A", "title": "Building A"},
#     #     {"id": "b", "building": "Building A", "title": "Building B"},
#     #     {"id": "c", "building": "Building B", "title": "Building C"},
#     #     {"id": "d", "building": "Building B", "title": "Building D"},
#     #     {"id": "e", "building": "Building C", "title": "Building E"},
#     #     {"id": "f", "building": "Building C", "title": "Building F"},
#     # ],
# }