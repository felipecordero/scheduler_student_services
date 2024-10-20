import matplotlib
import pandas as pd
import streamlit as st
from shared import crud

# st.set_page_config(layout="wide")

# cmap = plt.cm.get_cmap('RdYlGn')

# Method for rendering the details for the specific event
def render_details(db, event_name):

    # # Ejemplo de uso
    # collection_name = 'week_sept_3_6'
    data = crud.get_students_registered(db, event_name)

    # Crear la lista de días con gente registrada
    if data:
        days = list(data[0].keys())

        days.remove("name")
        days.remove("student_id")

        new_data = []

        for student in data:
            for day in days:
                for hour in student[day]:
                    new_data.append({day: student["name"], "hour": hour}) 

        df = pd.DataFrame(new_data)

        df_days = list(df.columns)
        df_days.remove("hour")

        names = set()
        for col in df_days:
            names.update(df[col].dropna().unique())

        names = list(names)
        names.sort()

        cmap = matplotlib.colormaps["RdYlGn"]

        df_count = df.groupby("hour").count().reset_index().style.background_gradient(cmap=cmap,vmin=0,vmax=5)

        new_df = df.groupby("hour")[df_days].agg(lambda x: '<br>'.join(x.dropna().astype(str))).reset_index()

        tab1, tab2 = st.tabs(["All Students", "Specific Student"])

        name = tab2.selectbox("Select One Student", options=names)

        especific_student = []
        especific_students_days = []
        for student in data:
            if student["name"] == name:
                for day in days:
                    if len(student[day]) > 0:
                        especific_students_days.append(day)
                        for hour in student[day]:
                            especific_student.append({day: "✓", "hour": hour})

        student_df = pd.DataFrame(especific_student, columns=["hour"].extend(especific_students_days))

        tab2.write(student_df.groupby("hour")[especific_students_days].agg(lambda x: '<br>'.join(x.dropna().astype(str))).reset_index().to_html(index=False), unsafe_allow_html=True)

        # col1, col2 = tab1.columns(2)

        tab1.header("Number of people per day")

        tab1.write(df_count.to_html(index=False, escape=False), unsafe_allow_html=True)

        tab1.header("Names of people per day")

        # Display the DataFrame in Streamlit with HTML line breaks rendered correctly
        tab1.write(new_df.to_html(escape=False, index=True), unsafe_allow_html=True)

        # tab1.write(new_df)

        # Display the dataframe for the specific user

        # df_grouped = student_df.groupby("hour")[especific_students_days].agg(lambda x: '<br>'.join(x.dropna().astype(str))).reset_index()

        # tab2.write(df_grouped)

    else:
        st.warning("There are no students registered yet")
