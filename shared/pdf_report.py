from datetime import datetime
from io import BytesIO, StringIO

import pandas as pd
from firebase_admin import firestore
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Frame,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from shared import crud

styles = getSampleStyleSheet()

table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    # ('FONTSIZE', (0, 0), (-1, 0), 14),
    # ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])


# Function to draw the header
def draw_header(canvas, doc):
    canvas.saveState()
    header_text = "Repeating Header"
    header = Paragraph(header_text, styles['Heading1'])
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
    canvas.restoreState()

def encabezado(canvas, doc):
    h = 27.94 * cm
    w = 21.59 * cm
    canvas.saveState()
#    canvas.setFont('Times-Roman',9)
    canvas.setFontSize(9)
    canvas.drawString(inch, letter[1] - 2.1 * cm, "Student Services - Schedule Report ")
    canvas.drawImage("logos/logo_college.png",
                        w - 5 * cm,
                        h - 2.8 * cm,
                        3 * cm,
                        2.5 * cm,
                        preserveAspectRatio=True)
    canvas.line(2 * cm, h - 2.2 * cm, w - 2 * cm, h - 2.2 * cm)
    canvas.restoreState()

def calculate_hours(rango_horario: str) -> float:
    """
    Calcula la diferencia en horas, cuando el input
    viene así:
    07:00-08-00
    """
    # Define the two times
    time_format = "%H:%M"
    time1, time2 = rango_horario.split("-") 

    # Convert the times to datetime objects
    datetime1 = datetime.strptime(time1, time_format)
    datetime2 = datetime.strptime(time2, time_format)

    # Calculate the difference
    return (datetime2 - datetime1).seconds / 3600


def create_simple_pdf():
    # Create a canvas object
    pdf = canvas.Canvas("simple_report.pdf", pagesize=letter)

    # Set the font and size
    pdf.setFont("Helvetica", 12)

    # Add a title
    pdf.drawString(100, 750, "Simple PDF Report")

    # Add some text
    pdf.drawString(100, 700, "This is a simple PDF report generated using reportlab.")

    # Add an image
    pdf.drawImage("example_image.png", 100, 500, width=100, height=100)

    # Save the PDF
    pdf.save()


def create_complex_pdf(data):
    # Create a SimpleDocTemplate object
    doc = SimpleDocTemplate("complex_report.pdf", pagesize=letter)

    # # Create a list of data for the table
    # data = [
    #     ["Name", "Age", "City"],
    #     ["Alice", 30, "New York"],
    #     ["Bob", 25, "Los Angeles"],
    #     ["Charlie", 35, "Chicago"],
    # ]

    # Create a Table object
    table = Table(data)

    table.setStyle(table_style)

    # Build the PDF
    elements = [table]
    doc.build(elements)

def create_student_attendance_report(student_id: str, db: firestore.client, event: str):

    students_info = crud.get_all_users()

    for i in students_info:
        if i["user"] == student_id:

            firstname = i["first_name"]
            last_name = i["last_name"]
            student_name = f"{firstname} {last_name}"
            break

    pdf_buffer = BytesIO()

    story = []

    attendance_info = crud.get_attendance_doc(db, event)

    print("Building attendance report")
    df = pd.DataFrame(attendance_info)
    df.sort_index(inplace=True)

    tables = []

    total_hours = {}

    for day in df.columns:
        day_tabla = []
        for row in df[[day]].itertuples():
            df_filtered = pd.read_json(StringIO(row._1))
            df_filtered = df_filtered[(df_filtered["student_id"] == student_id) & (df_filtered["attendace"])]

            df_filtered = df_filtered[["student_id", "attendace"]]

            if not df_filtered.empty:

                aux: list = df_filtered.values.tolist()
                for i in aux:
                    i.insert(0, row.Index)
                    i.insert(1, calculate_hours(row.Index))
                day_tabla.extend(aux)

        if day_tabla:
            total_day = pd.DataFrame(day_tabla, columns=["hour amount_hours name attendance".split()])
            total_hours[day] = total_day["amount_hours"].sum()
            day_tabla.insert(0, ["Hour", "Amount of hours", "Student", "Attendance"])
            tables.append((day, Table(day_tabla)))

    # Create a SimpleDocTemplate object using the BytesIO object
    # doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=1*inch, bottomMargin=1*inch)
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Create frames for the header and the main content
    header_frame = Frame(doc.leftMargin, doc.height + doc.topMargin - 1*inch, doc.width, 1*inch, id='header')
    # main_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2*inch, id='main')
    main_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.8*inch, id='main')

    # Create a PageTemplate with the header frame and the main frame
    header_template = PageTemplate(id='header_template', frames=[header_frame, main_frame], onPage=encabezado)

    # Add the PageTemplate to the SimpleDocTemplate
    doc.addPageTemplates(header_template)

    # Add a main heading to the story
    story.append(Paragraph("Attendance Report", styles['Heading1']))

    story.append(Paragraph(f"Event: {event}", styles['Heading2']))

    # story.append(Paragraph(event, styles["Heading4"]))
    
    story.append(Paragraph(f"Student: {student_name}", styles['Heading2']))

    total_hours_per_event = 0.0

    for hours in total_hours.values():
        total_hours_per_event += hours

    story.append(Paragraph(f"Total Hours during the event = {float(total_hours_per_event)}", styles["Heading4"]))

    story.append(Paragraph("Details by days", styles['Heading3']))

    for day, table in tables:
        table: Table
        table.setStyle(table_style)
        day: str
        story.append(Paragraph(day, styles["Heading4"]))
        story.append(Paragraph(f"Hours = {float(total_hours[day])}", styles["Heading5"]))
        story.append(table)

    # Build the PDF
    doc.build(story)
    return pdf_buffer.getvalue()