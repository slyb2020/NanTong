import PyPDF2
import os
import glob
import fitz # 导入本模块需安装pymupdf库

# 将文件夹中所有jpg图片全部转换为一个指定名称的pdf文件，并保存至指定文件夹
def pic2pdf_1(img_path, pdf_path, pdf_name):
    doc = fitz.open()
    for img in sorted(glob.glob(img_path + "\*.jpg")):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(pdf_path + pdf_name)
    doc.close()

# 将文件夹中指定jpg图片转换为指定名称的pdf文件，并保存至指定文件夹
def pic2pdf_2(img_path, pdf_path, img_list, pdf_name):
    doc = fitz.open()
    pic_list = [img_path+i for i in img_list]
    for img in sorted(pic_list):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(pdf_path + pdf_name)
    doc.close()

# 将文件夹中所有jpg图片分别转换为同一名称的pdf文件，并保存至指定文件夹
def pic2pdf_3(img_path, pdf_path):
    for img in glob.glob(img_path + "\*.jpg"):
        file_name = os.path.basename(img).replace('jpg', 'pdf')
        doc = fitz.open()
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(pdf_path + '\\' + file_name)
    doc.close()

# if __name__ == '__main__':
#     img_path = r'E:\test\jpg'
#     pdf_path = r'E:\test\jpg'
#     img_list1, pdf_name1 = [r'\001.jpg', r'\002.jpg'], r'\2.pdf'
#     pic2pdf_1(img_path=img_path, pdf_path=pdf_path, pdf_name=r'\1.pdf')
#     pic2pdf_2(img_path=img_path, pdf_path=pdf_path, img_list=img_list1, pdf_name=pdf_name1)
#     pic2pdf_3(img_path=img_path, pdf_path=pdf_path)def ConvertPDF():
#     pass
def MergePDF():
    filenames=os.listdir("D:\\BaiduNetdiskWorkspace\\2022年工作\\Luka\\天花板图纸\\pdf\\")
    merger=PyPDF2.PdfFileMerger()
    for filename in filenames:
        merger.append(PyPDF2.PdfFileReader("D:\\BaiduNetdiskWorkspace\\2022年工作\\Luka\\天花板图纸\\pdf\\"+filename))
    merger.write('天花板图纸.pdf')

if __name__ == "__main__":
    pic2pdf_1(img_path="D:\\BaiduNetdiskWorkspace\\2022年工作\\Luka\\天花板图纸\\TNF CEILING PANEL\\", pdf_path="D:\\BaiduNetdiskWorkspace\\2022年工作\\Luka\\天花板图纸\\pdf\\", pdf_name='3.pdf')
    # MergePDF()
