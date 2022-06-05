from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate,TableStyle,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
styles = getSampleStyleSheet()
doc = SimpleDocTemplate("simple_table.pdf",Paragraph('Here is large field retrieve from database',styles['Normal']),'34')
t=Table(data)
elements.append(t)
doc.build(elements)