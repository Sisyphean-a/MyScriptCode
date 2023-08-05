from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

# 打开 PDF 文件
with open('a.pdf', 'rb') as pdf_file:
    # 创建资源管理器、设备和解释器对象
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # 遍历 PDF 的每一页
    for page in PDFPage.get_pages(pdf_file):
        # 处理当前页
        interpreter.process_page(page)

        # 获取当前页中的文本
        page_text = retstr.getvalue()

        # 清空字符串缓冲区以便于处理下一页
        retstr.truncate(0)
        retstr.seek(0)

        # 打印文本（或执行其他操作）
        print(page_text)
