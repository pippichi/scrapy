import datetime
import re


# 判断爬的数据是否是今天
def check_if_today(text):
    pattern = re.compile(r".*(\d+)月(\d+)日", re.S)
    gs = re.search(pattern, text)

    today = datetime.date.today().strftime("%m%d")
    mouth = today[0:2] if today[0] != '0' else today[1:2]
    day = today[2:4] if today[2] != '0' else today[3:4]
    if mouth == gs.group(1) and day == gs.group(2):
        return True
    return False


# 解析总共多少条记录
def parse_total_records(text):
    pattern = re.compile(r"总(\d+)记录", re.S)
    return re.search(pattern, text).group(1)


# 解析title
def parse_title(text):
    index = text.find("（")
    return text[0: index]


# 解析date
def parse_date(text):
    pattern = re.compile(r".*?([-\d]+\d)")
    return re.search(pattern, text).group(1)


# 生成excel
def gen_excel(content, excel):
    try:
        first_row_name = None
        if len(content[0]) == 5:
            sheet = excel.create_sheet("国内生猪及仔猪市场交易日报")
            for i in range(len(content) - 1):
                for j in range(len(content[i])):
                    if len(content[i]) == 5:
                        sheet.cell(i + 1, j + 1).value = content[i][j]
                        first_row_name = content[i][0]
                    else:
                        sheet.cell(i + 1, 1).value = first_row_name
                        sheet.cell(i + 1, j + 2).value = content[i][j]
            last_row = content[len(content) - 1]
            if last_row[0] == '全国均价':
                for j in range(len(last_row)):
                    if j == 1 or j == 2:
                        continue
                    else:
                        sheet.cell(len(content), j + 1).value = last_row[j]
            else:
                for j in range(len(last_row)):
                    if len(last_row) == 5:
                        sheet.cell(len(content), j + 1).value = last_row[j]
                    else:
                        sheet.cell(len(content), 1).value = first_row_name
                        sheet.cell(len(content), j + 2).value = last_row[j]

        if len(content[0]) == 7:
            sheet = excel.create_sheet("国内肉鸡市场交易日报")
            for i in range(len(content) - 1):
                for j in range(len(content[i])):
                    if len(content[i]) == 7:
                        sheet.cell(i + 1, j + 1).value = content[i][j]
                        first_row_name = content[i][0]
                    else:
                        sheet.cell(i + 1, 1).value = first_row_name
                        sheet.cell(i + 1, j + 2).value = content[i][j]

            last_row = content[len(content) - 1]
            if last_row[0] == '全国均价':
                for j in range(len(last_row)):
                    sheet.cell(len(content), j + 2).value = content[len(content) - 1][j]
            else:
                for j in range(len(last_row)):
                    if len(last_row) == 7:
                        sheet.cell(len(content), j + 1).value = last_row[j]
                    else:
                        sheet.cell(len(content), 1).value = first_row_name
                        sheet.cell(len(content), j + 2).value = last_row[j]
    except Exception as e:
        print('!' * 30)
        print(e)
        print('!' * 30)
