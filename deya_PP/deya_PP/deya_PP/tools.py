import datetime
import re
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PIL import ImageDraw

# 解析爬取的内容
from deya_PP.properties import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_PASSWORD, EMAIL_TO


def parse_en(enterprise, content):
    pattern = re.compile(r"[-\dA-Za-z]+", re.S)
    res = []
    for c in content:
        temp = re.findall(pattern, c)
        if len(temp) == 0:
            res.append(["停车:" + c])
        else:
            res.append(temp)
    return dict(zip(enterprise, res))


# 二值处理
def get_table(threshold=115):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

# 图片降噪
def get_pixel(image, x, y, G, N):

    L = image.getpixel((x, y))

    if L > G:
        L = True
    else:
        L = False

    nearDots = 0

    if L == (image.getpixel((x - 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x, (y - 1)))
    else:
        return None


# 降噪次数
def clear_noise(image, G, N, Z):
    draw = ImageDraw.Draw(image)
    for i in range(0, Z):
        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                color = get_pixel(image, x, y, G, N)
                if color is not None:
                    draw.point((x, y), color)


# 图片预处理
def image_preprocessing(image):
    grey_im = image.convert('L')
    binary_im = grey_im.point(get_table(threshold=150), "1")
    clear_noise(binary_im, 50, 4, 10)
    binary_im.show()
    binary_im.save('./PP_code.png')


# 判断所爬取的网址是否为今天这个日期
def verify_date(url):
    pattern = re.compile(r"\d{4}", re.S)
    res = re.search(pattern, url).group(0)
    today = datetime.date.today().strftime("%m%d")
    return res == today


# 发送邮件
def succeed_and_send_email(file_path):

    sender = EMAIL_HOST_USER
    receivers = EMAIL_TO

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = sender  # 发送者
    message['To'] = ';'.join(receivers)  # 接收者
    subject = "PP网址爬虫成功！请查看附件获取excel文件！"
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = "您好！\n系统检测到您于北京时间：" + now + "进行了一次PP网址的爬虫，爬取到的数据经过处理已经发送到您的邮箱，请查看附件收取！"
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    # 构造附件
    att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att.add_header("Content-Disposition", "attachment", filename=("gbk", "", file_path))
    message.attach(att)
    post_email(sender, receivers, message)


def failed_and_send_email():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject = "PP网址爬虫提醒！"
    message = "您好！\n系统检测到您于北京时间：" + now + "进行了一次PP网址的爬虫，但是今日的最新PP网址还没有发出来，请稍后再试！\n（建议下午4点以后执行该爬虫程序）"

    sender = EMAIL_HOST_USER
    receivers = EMAIL_TO

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = sender  # 发送者
    message['To'] = ';'.join(receivers)  # 接收者

    message['Subject'] = Header(subject, 'utf-8')
    post_email(sender, receivers, message)


def post_email(sender, receivers, message):
    try:
        smtp = smtplib.SMTP()
        smtp.connect(host=EMAIL_HOST, port=EMAIL_PORT)
        smtp.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)
        smtp.sendmail(sender, receivers, message.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("邮件发送失败")
