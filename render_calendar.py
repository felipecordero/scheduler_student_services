import streamlit as st
import calendar_settings
import dateparser
import datetime
from streamlit_calendar import calendar

@st.fragment
def render_calendar(eventos):
    calendar_options = {
            "editable": "true",
            "navLinks": "true",
            "resources": calendar_settings.calendar_resources,
            "selectable": "true",
            }

    calendar_events = []
    
    for evento in eventos:
        try:
            start_date = dateparser.parse(evento["fecha_inicio"], settings={'DATE_ORDER': 'DMY'})
        except TypeError:
            start_date = evento["fecha_inicio"].date()
        end_date = start_date + datetime.timedelta(weeks=evento["duracion"])
        # print(str(dateparser.parse(evento["fecha_inicio"], settings={'DATE_ORDER': 'DMY'})))
        calendar_events.append({
            "title": evento["nombre"],
            # "start": str(start_date),
            # "end": str(end_date),
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        })

    mode = st.selectbox(
        "Calendar Mode:",
        (
            "daygrid",
            "timegrid",
            "timeline",
            # "resource-daygrid",
            # "resource-timegrid",
            # "resource-timeline",
            "list",
            "multimonth",
        ),
    )

    calendar_options = calendar_settings.get_calendar_options(mode, calendar_options)

    calendar_options = {
                **calendar_options,
                "initialDate": datetime.date.today().strftime("%Y-%m-%d"),
                "firstDay": 1,
                "weekends": True,
            }
    
    calendar(events=calendar_events,
            options=calendar_options)