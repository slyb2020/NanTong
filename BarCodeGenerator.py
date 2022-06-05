# code128
from pystrich.code128 import Code128Encoder
def BarCodeGenerator(code):
    encoder = Code128Encoder(code)
    encoder.save("tempBarcode.png", bar_width=2)
