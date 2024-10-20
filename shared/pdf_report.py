from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


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

    # Add style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    # Build the PDF
    elements = [table]
    doc.build(elements)