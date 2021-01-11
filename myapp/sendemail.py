import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

	myemail = 'noreply.teamtesting@gmail.com'
	mypassword = "gsHofh;p96"
	receiver = sendto

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj
	msg['From'] = 'Team Best Fruit'
	msg['To'] = receiver
	text = detail

	part1 = MIMEText(text, 'plain')
	msg.attach(part1)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()

	s.login(myemail, mypassword)
	s.sendmail(myemail, receiver.split(','), msg.as_string())
	s.quit()


###########Start sending#############
subject = 'ยืนยันการสมัครเว็บไซต์ Best Fruit'
newmember_name = 'ใหม่'
content = '''
ขอบคุณที่ท่านทำการสัมครสามาชิก Best Fruit! ปลอดภัยของการเข้าใช้
กรุณายืนยันอีเมลล์ ผ่านลิ้งค์ด้านล่างนี้:
ขอให้สนุกกับการเลือกสินค้า และถ้าต้องการติดต่อ เสนอแนะเราท่านสามารถติต่อเราได้ทันที.
'''

link = 'http://best-fruit.com/confirm/fawtkataktaktkawkejtjka'

msg = 'สวัสดีครับ คุณ{} \n\n {}\n Verify Link: {}'.format(newmember_name,content,link)

sendthai('skakanaporn@gmail.com',subject,msg)

# หากต้องการส่งหลายคนสามารถใส่คอมม่าใน string ได้เลย เช่น 'loongTu1@gmail.com,loongTu2@gmail.com'


