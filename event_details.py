import matplotlib
import pandas as pd
import streamlit as st
from shared import crud

cmap = matplotlib.colormaps["RdYlGn"]

# Method for rendering the details for the specific event
@st.fragment
def render_details(db, event_name):

    students_registered = crud.get_students_registered(db, event_name)

    students_info = crud.get_all_users(db)

    # Proceder si hay estudiantes registrados
    if students_registered:
        days = []
        for student in students_registered.values():
            days.extend(list(student.keys()))
        days = list(set(days))

        full_df_data = []

        for username, student in students_registered.items():
            for day in days:
                for hour in student[day]:
                    full_df_data.append({day: username, "hour": hour}) 

        full_df = pd.DataFrame(full_df_data)

        # Reemplazar los id por los nombres de los estudiantes

        for student_data in students_info:
            if "last_name" in student_data:
                full_df = full_df.replace(student_data["user"], 
                                          f"""{student_data["first_name"]} {student_data["last_name"]}""")

        # st.dataframe(full_df)

        # other_df = full_df.merge(right=)

        # Convert the remaining column names to datetime objects and sort them
        sorted_columns = sorted([col for col in full_df.columns if col != 'hour'], key=lambda x: pd.to_datetime(x))

        # Separate the "hour" column
        hour_column = full_df.pop('hour')

        # Reorder the DataFrame columns
        full_df = full_df[sorted_columns]

        # Add the "hour" column back to the DataFrame
        full_df.insert(0, 'hour', hour_column)

        days_list = list(full_df.columns)
        days_list.remove("hour")

        df_count = full_df.groupby("hour").count().reset_index()
        df_count = df_count.style.background_gradient(cmap=cmap,vmin=0,vmax=5)

        df_students_names_full = full_df.groupby("hour")[days_list].agg(lambda x: '<br>'.join(x.dropna().astype(str)))

        # TABS

        tab1, tab2 = st.tabs(["All Students", "Specific Student"])

        # TAB de todos los estudiantes

        with tab1:
            
            with st.container(border=True):
                st.subheader("Number of students per day")
                st.write(df_count.to_html(), unsafe_allow_html=True)
                
            with st.container(border=True):

                st.subheader("Names of students per day")

                # Display the DataFrame in Streamlit with HTML line breaks rendered correctly
                st.write(df_students_names_full.reset_index().to_html(escape=False, index=False), unsafe_allow_html=True)
        
                # df_students_names_full = full_df.groupby("hour")[days_list].agg(lambda x: list(x.dropna()))

                # st.write(full_df.groupby("hour")[full_df_days].agg(lambda x: '\n'.join(x.dropna().astype(str))))

                # st.data_editor(df_students_names_full)
                                # column_config={
                                #     columns[0]: st.column_config.Column(disabled=True),
                                #     "student_id": st.column_config.Column(disabled=True),
                                # },
                                # hide_index=True)

        # TAB de un solo estudiante

        with tab2:

            # Lista de nombres

            names = pd.unique(full_df[days_list].stack().dropna().values.ravel())

            selected_student = st.selectbox("Select One Student", options=names, key="select_one_student_details")

            student_df = full_df[full_df.eq(selected_student).any(axis=1)]

            student_df = student_df.replace(selected_student, "✓")

            st.write(student_df.groupby("hour").agg(lambda x: ''.join(x.dropna().astype(str))).reset_index().to_html(index=False), unsafe_allow_html=True)

    else:
        st.info("There are no students registered yet")

