from django.contrib import admin
from django.core import paginator
from django.core.paginator import Paginator
from django.db import reset_queries
from django.http import request
from django.shortcuts import render, redirect #restricly access
from django.http import HttpResponse #HttpResponse is a fucntion to show content on site
from .models import *
from datetime import datetime

########Line Notify########
from songline import Sendline
token ='ZDXWM1wd3IhrbZjeq882GXgIBk8OnRk8qFDklLPXn7c'
messenger = Sendline(token)

######Generate token#########
import random
import string
def GenerateToken(domain='http://localhost:8000/confirm/'):
	allchar = [ i for i in list(string.ascii_letters)] #Generate ascii to list
	allchar.extend([str(i) for i in range(10)])# extending number 0-9 in the list
	emailtoken = ''
	for i in range(40):
		emailtoken += random.choice(allchar)

	url = domain + emailtoken
	#print(url)
	return (url,emailtoken)

def Confirm(request,token):
	try:
		check = VerifyEmail.objects.get(token=token)
		status = 'found'
		check.approved = True
		check.save()
		context = {'status':status,'username':check.user.username,'name':check.user.first_name}
	except:
		status = 'notfound'
		context = {'status':status}
	
	return render(request, 'myapp/confirm.html',context)

#######EMAIL########
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
def EmailConfirm(email,name,token):
	subject = 'ยืนยันการสมัครเว็บไซต์ Best Fruit'
	newmember_name = name
	content = '''
	ขอบคุณที่ท่านทำการสัมครสามาชิก Best Fruit! ปลอดภัยของการเข้าใช้
	กรุณายืนยันอีเมลล์ ผ่านลิ้งค์ด้านล่างนี้:
	ขอให้สนุกกับการเลือกสินค้า และถ้าต้องการติดต่อ เสนอแนะเราท่านสามารถติต่อเราได้ทันที.
	'''

	#link = 'http://best-fruit.com/confirm/fawtkataktaktkawkejtjka'
	link = token

	msg = 'สวัสดีครับ คุณ{} \n\n {}\n Verify Link: {}'.format(newmember_name,content,link)
	sendthai(email,subject,msg)
###############


# Create your views here.
def Home(request):
	product = Allproduct.objects.all().order_by('id').reverse()[:3] #query data form all products by descending order
	preorder = Allproduct.objects.filter(quantity__lte=0 ) 
	#quantity__lte=0 (find the quantity is less than or equal zero (<=0))
	#quantity__gt=0 (find the quantity is greater than zero (>))
	context = {'product':product,'preorder':preorder}
	return render(request, 'myapp/home.html', context)


	#return HttpResponse('<h1>สวัสดี Hello world</h1><p></p>')

def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Apple(request):
	return render(request, 'myapp/apple.html')

from django.core.files.storage import FileSystemStorage

def Addproduct(request):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')


	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')


		new = Allproduct()
		new.name = name
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit
		############Save Image################
		try:
			file_image = request.FILES['imageupload']
			file_image_name = request.FILES['imageupload'].name.replace(' ','')
			print('FILE_IMAGE:', file_image)
			print('IMAGE_NAME:', file_image_name)
			fs = FileSystemStorage()
			filename = fs.save(file_image_name,file_image)
			upload_file_url = fs.url(filename)
			new.image = upload_file_url[6:]
		except:
			new.image = '/default-product.jpg'
		###############################
		new.save()

	return render(request, 'myapp/addproduct.html')

from django.core.paginator import Paginator

def Products(request):
	product = Allproduct.objects.all().order_by('id').reverse() #query data from all products by descending order
	paginator = Paginator(product,3) #1 หน้าโชว์ 3 ชิ้นเท่านั้น
	page = request.GET.get('page') # http://localhost:8000/allproduct/?page=2
	product = paginator.get_page(page)
	context = {'product':product}
	return render(request, 'myapp/allproduct.html', context)

def ProductsCategory(request,code):
	select = Category.objects.get(id=code)
	product = Allproduct.objects.filter(catname=select).order_by('id').reverse() #query data from all products by descending order
	paginator = Paginator(product,3) #1 หน้าโชว์ 3 ชิ้นเท่านั้น
	page = request.GET.get('page') # http://localhost:8000/allproduct/?page=2
	product = paginator.get_page(page)
	context = {'product':product,'catname':select.catname}
	return render(request, 'myapp/allproductcat.html', context)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def Register(request):
	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')
		#ยังไม่ได้ใส่ try except เพื่อป้องกันการสมัครซ้ำ
		#+ alret ไปหน้าสมัครว่าอีเมลล์นี้เคยสมัครแล้ว
		#สอนคู่กับหัวข้อ reset password

		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()

		##### send email for verify #### **** <<<testing>>>
		token,token_code = GenerateToken()
		EmailConfirm(email,first_name,token)
		getuser = User.objects.get(username=email)
		addverify = VerifyEmail()
		addverify.user = getuser
		addverify.token = token_code
		addverify.save()

		#from django.contrib.auth import authenticate, login
		user = authenticate(username=email, password=password)
		login(request,user) 
		#Auto login

	return render(request, 'myapp/register.html')


def AddtoCart(request,pid):
	# localhost:8000/addtocart/pid
	# or {% url 'addtocart-page' pd.id %}
	print('CURRENT USER:',request.user)
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)
	try:
		#กรณีที่สินค้ามีซ้ำ
		newcart = Cart.objects.get(user=user,productid=str(pid))
		#print('EXISTS: ', pcheck.exists())
		newquan = newcart.quantity + 1
		newcart.quantity = newquan
		calculate = newcart.price * newquan
		newcart.total = calculate
		newcart.save()

		#update items amount in cart
		count = Cart.objects.filter(user=user)
		count =  sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')

	except:
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()

		count = Cart.objects.filter(user=user)
		count =  sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')


def MyCart(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}
	if request.method == 'POST':
		#ใช้สำหรับการลบเท่านั้น
		data =request.POST.copy()
		productid = data.get('productid')
		print('PID',productid)
		item = Cart.objects.get(user=user,productid=productid)
		item.delete()
		context['status'] = 'delete'

		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

	mycart = Cart.objects.filter(user=user)
	count = sum([ c.quantity for c in mycart])
	total = sum([ c.total for c in mycart])

	context['mycart'] = mycart
	context['count'] = count
	context['total'] = total


	return render(request, 'myapp/mycart.html',context)

def MyCartEdit(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}
	if request.method == 'POST':
		data = request.POST.copy()
		#print(data)
		if data.get('clear') == 'clear':
			print(data.get('clear'))
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')
		
		editlist = []
		for k,v in data.items(): 
			#print([k,v])
			if k[:2] == 'pd':
				pid = int(k.split('_')[1])
				dt = [pid,int(v)]
				editlist.append(dt)
		#print('EDITLIST:', editlist) #[[productID,quan]]

		for ed in editlist:
			edit = Cart.objects.get(productid=ed[0],user=user)#productid
			edit.quantity = ed[1] #quantity
			calculate = edit.price * ed[1]
			edit.total = calculate
			edit.save()


		count = Cart.objects.filter(user=user)
		count = sum([ c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		return redirect('mycart-page')
		

	mycart = Cart.objects.filter(user=user)
	context['mycart'] = mycart


	return render(request, 'myapp/mycartedit.html',context)

def Checkout(request):
	username = request.user.username
	user = User.objects.get(username=username)
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')
		if page == 'information':
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['address'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other

			mycart = Cart.objects.filter(user=user)
			count = sum([ c.quantity for c in mycart])
			total = sum([ c.total for c in mycart])

			context['mycart'] = mycart
			context['count'] = count
			context['total'] = total

			return render(request, 'myapp/checkout2.html', context)

		if page == 'confirm':
			print('Confirm')
			print(data)
			mycart = Cart.objects.filter(user=user)
			# generate order no. and save to Order Models
			# id = OD 0007 2020 09 03 22 00 30
			# id = OD 0230 20200903220030
			mid = str(user.id).zfill(4)
			dt = datetime.now().strftime('%Y%m%d%H%M%S')
			orderid = 'OD'+ mid + dt
			productorder = ''
			producttotal = 0

			for pd in mycart:    
				order = OrderList()
				order.orderid = orderid
				order.productid = pd.productid
				order.productname = pd.productname
				order.price = pd.price
				order.quantity = pd.quantity
				order.total = pd.total
				order.save()
				productorder = productorder + '- {}\n'.format(pd.productname)#รายการสินค้า
				producttotal += pd.total

			
			# Send to LINE Notify in Group
			texttoline = 'ODID: {}\n---\n{}ยอดรวม: {:,.2f} บาท\n ({})'.format(orderid,productorder,producttotal,name)
			# เช็คยอดสินค้าว่ามากกว่า 10000 หรือไม่หากจริงจะส่งสติกเกอร์ไปด้วย
			if producttotal > 10000:
				messenger.sticker(14,1,texttoline)
			else:
				messenger.sendtext(texttoline)


			# save product in cart to OrderProduct models
			# creat order pending
			odp = OrderPending()
			odp.orderid = orderid
			odp.user = user
			odp.name = name
			odp.tel = tel
			odp.address = address
			odp.shipping = shipping
			odp.payment = payment
			odp.other = other
			odp.save()

			# clear cart
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')

	return render(request, 'myapp/checkout1.html')

# redirect to order list page
def OrderListPage(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}
	order = OrderPending.objects.filter(user=user)
	'''
	-order
		-order id: OD000220201202131342
		-user:
		-name: ผู้รับ
	'''
	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		'''
			-odlist
			-object (1)
				-orderid: OD1033134
				-product: ทุเรียน
				-total: 500
			-object (2)
				-orderid: OD1033134
				-product: กล้วย
				-total: 300
			-object (3)
				-orderid: OD1033134
				-product: ส้ม
				-total: 200

		'''
		# total = summation from orderlist sum([500,300,200])
		total = sum([c.total for c in odlist])
		od.total = total
		# สั่งนับ order ทั้งหมดมีจำนวนกี่ชิ้น
		count = sum([c.quantity for c in odlist])

		if od.shipping == 'ems':
			shipcost = sum([50 if i == 0 else 10 for i in range(count)])
			# shipcost = รวมค่าทั้งหมด (หากเป็นชิ้นแรกค่าส่งจะคิด 50 บาท ชิ้นถัดไปชิ้นละ 10 บาท)
		else:
			shipcost = sum([35 if i == 0 else 10 for i in range(count)])

		if od.payment == 'cod':
			shipcost += 20 # shipcost = shipcost + 20 for 'COD'
		od.shipcost = shipcost

	
	context['allorder'] = order

	return render(request, 'myapp/orderlist.html',context)

def AllOrderListPage(request):
	
	context = {}
	order = OrderPending.objects.all()


	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([ c.total for c in odlist])
		od.total = total

		count = sum([ c.quantity for c in odlist])

		if od.shipping == 'ems':
			shipcost = sum([ 50 if i == 0 else 10 for i in range(count)])
			# shipcost = รวมค่าทั้งหมด (หากเป็นชิ้นแรกค่าส่งจะคิด 50 บาท ชิ้นถัดไปชิ้นละ 10 บาท)
		else:
			shipcost = sum([ 35 if i == 0 else 10 for i in range(count)])

		if od.payment == 'cod':
			shipcost += 20 # shipcost = shipcost + 20
		od.shipcost = shipcost

	paginator = Paginator(order,5)
	page = request.GET.get('page') # http://localhost:8000/allorderlist/?page=
	order = paginator.get_page(page)
	context['allorder'] = order
	
	return render(request, 'myapp/allorderlist.html',context)

def UploadSlip(request,orderid):
	print('order ID:',orderid)

	if request.method == 'POST' and request.FILES['slip']:
		data = request.POST.copy()
		sliptime = data.get('sliptime')

		update = OrderPending.objects.get(orderid=orderid)
		update.sliptime = sliptime
		##########Save ImageSlip#########
		file_image = request.FILES['slip']
		file_image_name  = request.FILES['slip'].name.replace(' ','')
		print('FILE_IMAGE:',file_image)
		print('IMAGE_NAME:',file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		update.slip = upload_file_url[6:]
		#################################
		update.save()


	odlist = OrderList.objects.filter(orderid=orderid)
	total = sum([c.total for c in odlist])
	oddetail = OrderPending.objects.get(orderid=orderid)
	# สั่งนับ order ทั้งหมดมีจำนวนกี่ชิ้น
	count = sum([c.quantity for c in odlist])

	if oddetail.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		# shipcost = รวมค่าทั้งหมด (หากเป็นชิ้นแรกค่าส่งจะคิด 50 บาท ชิ้นถัดไปชิ้นละ 10 บาท)
	else:
		shipcost = sum([35 if i == 0 else 10 for i in range(count)])

	if oddetail.payment == 'cod':
		shipcost += 20 # shipcost = shipcost + 20 for 'COD'
	
	context= {'orderid':orderid,
			  'total':total,
			  'shipcost':shipcost,
			  'grandtotal':total+shipcost,
			  'oddetail':oddetail,
			  'count':count}
	
	return render(request, 'myapp/uploadslip.html',context)

def UpdatePaid(request,orderid,status):
		
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	
	order = OrderPending.objects.get(orderid=orderid)
	if status == 'confirm':
		order.paid = True
	elif status == 'cancel':
		order.paid = False
	order.save()
	return redirect('allorderlist-page')

def UpdateTracking(request,orderid):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
		
	if request.method == 'POST':
		order = OrderPending.objects.get(orderid=orderid)
		data = request.POST.copy()
		trackingnumber = data.get('trackingnumber')
		order.trackingnumber = trackingnumber
		order.save()
		return redirect('allorderlist-page')
		
	order = OrderPending.objects.get(orderid=orderid)
	odlist = OrderList.objects.filter(orderid=orderid)
	#### shipcost calculate
	total = sum([ c.total for c in odlist])
	order.total = total

	count = sum([ c.quantity for c in odlist])

	if order.shipping == 'ems':
		shipcost = sum([ 50 if i == 0 else 10 for i in range(count)])
		# shipcost = รวมค่าทั้งหมด (หากเป็นชิ้นแรกค่าส่งจะคิด 50 บาท ชิ้นถัดไปชิ้นละ 10 บาท)
	else:
		shipcost = sum([ 35 if i == 0 else 10 for i in range(count)])

	if order.payment == 'cod':
		shipcost += 20 # shipcost = shipcost + 20
	order.shipcost = shipcost

	context = {'orderid':orderid,'order':order,'odlist':odlist,'total':total,'count':count}

	return render(request, 'myapp/updatetracking.html', context)

def MyOrder (request,orderid):
	username = request.user.username
	user = User.objects.get(username=username)

	order = OrderPending.objects.get(orderid=orderid)
	#เช็คว่าเป็นของตัวเองไหม?
	if user != order.user:
		return redirect('allproduct-page')

	odlist = OrderList.objects.filter(orderid=orderid)
	#### shipcost calculate
	total = sum([ c.total for c in odlist])
	order.total = total

	count = sum([ c.quantity for c in odlist])

	if order.shipping == 'ems':
		shipcost = sum([ 50 if i == 0 else 10 for i in range(count)])
		# shipcost = รวมค่าทั้งหมด (หากเป็นชิ้นแรกค่าส่งจะคิด 50 บาท ชิ้นถัดไปชิ้นละ 10 บาท)
	else:
		shipcost = sum([ 35 if i == 0 else 10 for i in range(count)])

	if order.payment == 'cod':
		shipcost += 20 # shipcost = shipcost + 20
	order.shipcost = shipcost

	context = {'order':order,'odlist':odlist,'total':total,'count':count}

	return render(request, 'myapp/myorder.html', context)