import os
import xlwings as xw

def create_excel(now):
    if not os.path.isfile( ".\\output\\" + now + "\\result.xlsx" ):
        app=xw.App(visible=False,add_book=False)
        wb=app.books.add()
        wb.save( ".\\output\\" + now + "\\result.xlsx" )
        wb.close()
        #结束进程

    app=xw.App(visible=True,add_book=False)
    wb=app.books.open(".\\output\\" + now + "\\result.xlsx")

    return wb

def get_sheet(wb,sheetname):
    #查看工作表是否建立
    if sheetname not in [s.name for s in wb.sheets]:
        wb.sheets.add(name=sheetname)

    sheet = wb.sheets[sheetname]
    
    init_sheet(sheet)

    return sheet 

def init_sheet(sheet):
    sheet.range('A1').value = "場館名稱"
    sheet.range('A2').value = "免費遊戲"

def checkrow(sheet):
    start_cell = 'B'
    while True:
        # 檢查目標儲存格是否有值
        if sheet.range(start_cell+"1").value:
            # 設定下一個目標儲存格位置
            start_cell= chr(ord(start_cell) + 1) 
        else:
            return start_cell