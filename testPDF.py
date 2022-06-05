# from reportlab.platypus import SimpleDocTemplate, Image
#
# from reportlab.lib.styles import getSampleStyleSheet
#
# doc = SimpleDocTemplate("Hello.pdf")
# styles = getSampleStyleSheet()
# style = styles['Normal']
# story =[]
#
# t = Image("bitmaps/镀锌板.jpg")
# story.append(t)
#
# doc.build(story)

from reportlab.pdfgen import canvas
c= canvas.Canvas("hello.pdf")
c.drawString(100,100,"Welcome to Reportlab")
c.drawString(100,300,"Welcome to Reportlab")
c.showPage()
c.drawString(100,400,"Welcome to Reportlab")
c.save()