from django.db.models.fields import EmailField
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from freelancer.models import profile
from django.contrib.auth.models import User
from .models import User
from admin1.models import add_project
from django.http import HttpResponse
from hirer.models import project_bid_rate, payment_report
from django.contrib import messages #import messages
import datetime
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt
from .paytm  import Checksum

MERCHANT_KEY = 'bKMfNxPPf_QdZppa'
def show_profile(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			profile_data = profile.objects.filter(user_id=request.user)
			return render(request, 'hirer/profile.html', {'profile_data':profile_data})
		else:
			param={"error_login":"Please Check Credentials"}
			return render(request, 'hirer/login.html', param)
	else:
		return redirect('/hirer/login')


def edit_profile(request,id):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			profile_data = profile.objects.filter(user_id=id)
			return render(request, 'hirer/edit_profile.html', {'profile_data':profile_data})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')


def update_profile(request,id):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			if request.method == 'POST':
				user = User.objects.filter(id=id).update(username=request.POST['username'], first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'])
				hirer_profile=profile.objects.filter(user_id=id).update(phonenumber=request.POST['phonenumber'], address=request.POST['address'], technology=request.POST['technology'], status="Not Active", is_login="hirer")
				messages.success(request,'Profile updated successfully')
				
				return redirect('/hirer/profile')
			else:
				profile_data = profile.objects.filter(user_id=id)
				return render(request, 'hirer/edit_profile.html', {'profile_data':profile_data})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')


def freelancelist(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			freelancer_list = profile.objects.filter(is_login="freelancer")
			return render(request, 'hirer/freelancelist.html',{'freelancer_list':freelancer_list})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')

def postjob(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			if request.method == "POST":
				projectname = request.POST['projectname']
				description = request.POST['description']
				amount = request.POST['amount']
				start_time = request.POST['start_time']
				end_time = request.POST['end_time']
				front_end = request.POST['front_end']
				back_end = request.POST['back_end']
				status = "Not Active"
				project_detail_store = add_project(user_id=request.user, projectname=projectname, description=description, start_time=start_time, end_time=end_time, amount=amount, front_end=front_end,back_end=back_end, status=status)
				project_detail_store.save()
				messages.success(request,'Project added successfully')
				
				return redirect('/hirer/postjob')
			else:
				project_detail = add_project.objects.filter(user_id=request.user).order_by('-id')
				profile_data = profile.objects.filter(user_id=request.user)

				return render(request, 'hirer/postjob.html',{'profile_data':profile_data, 'project_detail':project_detail})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')

def delete_project(request,id):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			delete_project_find = add_project.objects.filter(id=id).delete()
			messages.success(request,'Project deleted successfully')

			return redirect('/hirer/postjob')
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')


def project_biding_rate(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:	
			profile_data1 = add_project.objects.filter(user_id=request.user)		
			profile_bid_rate_detail = project_bid_rate.objects.all()
			all_project = []
			for x in profile_bid_rate_detail:
				project_name = add_project.objects.filter(user_id=request.user)
				profile_data = profile.objects.filter(user_id=request.user)
				for y in project_name:
					if x.project == y.projectname:
						all_project = project_bid_rate.objects.filter(project=y.projectname)				
							
					else:
						all_project=''
						
			
			return render(request, 'hirer/project_bid.html', {'profile_data':profile_data, 'profile_bid_rate_detail':all_project})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')

def paystatus(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			profile_payent_status = project_bid_rate.objects.filter(status="Approved")
			# .filter(user=request.user)
			# profile_data = profile.objects.filter(user_id=request.user)
			payment_received_status = payment_report.objects.all()
			# payment_received_status = add_project.objects.filter(user_id_id=request.user)
			return render(request, 'hirer/paystatus.html',{'profile_payent_status':profile_payent_status,'payment_received_status':payment_received_status})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})	
	else:
		return redirect('/hirer/login')


def workstatus(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			
			profile_data = add_project.objects.filter(user_id=request.user)
			if len(profile_data)==0:
				profile_bid_rate_detail=''
				last_date=''
				return render(request, 'hirer/workstatus.html', {'profile_data':profile_data, 'profile_bid_rate_detail':profile_bid_rate_detail})
			else:
				
				for x in profile_data:
					profile_bid_rate_detail = project_bid_rate.objects.filter(project=x.projectname)
					last_date=project_bid_rate.objects.filter(end_date=x.end_time)
					
						# for str to date
					date_time_obj = datetime.strftime(x.end_time, '%b %d, %y')
					endd=date_time_obj[:10]
					cdate=datetime.today()
					to_date = datetime.strftime(cdate, '%b %d, %y')
					comdate=to_date[:10]
					today=datetime.today()
					# if(date_time_obj==comdate):
					# 	for i in profile_bid_rate_detail:
					# 		sub=f'remainder for {x.projectname}'
					# 		message=f'Hello {i.user.first_name} {i.user.last_name},You have to submit complete {x.projectname} project today, because {today} is last date for {x.projectname} '
					# 		email=settings.EMAIL_HOST_USER
					# 		recep=[i.user.email, ]
					# 		send_mail(sub, message, email, recep)
					
				return render(request, 'hirer/workstatus.html', {'profile_data':profile_data, 'profile_bid_rate_detail':profile_bid_rate_detail})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')

		
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['pass']
		user = authenticate(request, username=username, password=password)
		check_status = profile.objects.filter(user_id=user).filter(is_login='hirer')
		if len(check_status) == 1:
			if user is not None:
				auth.login(request, user)
				
				return redirect('/hirer')
		else:
			messages.error(request,'Please Check Credentials')
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		
		return render(request, 'hirer/login.html')

def logout(request):
	auth.logout(request)
	return redirect('/hirer/login')


def user_signup(request):
	if request.method == 'POST':
		if request.POST['password'] == request.POST['confirmpassword']:
			try:
				user = User.objects.get(username=request.POST['username'])
				messages.success(request,'This username is taken, please choose another username')
				return render(request, 'hirer/login.html', {'error':'please change username'})
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=request.POST['password'])
				hirer_profile=profile(user_id=user, phonenumber=request.POST['phonenumber'], address=request.POST['address'], technology=request.POST['technology'], status="Not Active", is_login="hirer")
				hirer_profile.save()
				messages.success(request,'Successfully Registerd, Now you can login')
				return redirect('/hirer')
		else:
			messages.success(request,'please check password and confirmpassword')
			return render(request, 'hirer/login.html' , {'error':'please check password and confirmpassword'})
	else:
		return render(request, 'hirer/login.html')


def bid_rate_show(request, id,end_date):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			project_bid_show_detail = project_bid_rate.objects.filter(project=id)
			datefor = project_bid_rate.objects.filter(end_date=end_date)
			for x in project_bid_show_detail:
				project_id = x.project
			project_information = 	add_project.objects.filter(projectname=project_id)
			return render(request, 'hirer/project_bid.html', {'project_bid_show_detail':project_bid_show_detail, 'project_information':project_information,'datefor':datefor})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')

def project_bidding_approval(request, id,end_date):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			project_bid_rate_detail = project_bid_rate.objects.filter(id=id)
			for x in project_bid_rate_detail:
				user = x.user
				project=x.project
				bid_rate = x.bid_rate
				comments = x.comments
				status = "Approved"
			project_bid_rate_store = project_bid_rate(id=id, bid_rate=bid_rate, project=project, user=user, comments=comments, status=status,end_date=end_date)
			project_bid_rate_store.save()
			messages.success(request,'thanks for Project Approving to Freelancer')

			return redirect('/hirer/project_bid_rate')
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})

# def payment_given(request, id):
# 	check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
# 	if len(check_status) == 1:
# 		if request.method == 'POST':
# 			project_bidding_rate = project_bid_rate.objects.filter(project=id)
# 			for x in project_bidding_rate:
# 				project = x.project
# 				user = x.user
# 				total_amount = x.bid_rate
# 			received_amount = request.POST['received_amount']
# 			payment_record = payment_report(project=project, user=user, total_amount=total_amount, received_amount=received_amount)
# 			payment_record.save()
# 			return redirect('/hirer/paystatus')
# 		else:
# 			project_bidding_rate_detail = project_bid_rate.objects.filter(project=id)
# 			return render(request, 'hirer/paystatus.html', {'project_bidding_rate_detail':project_bidding_rate_detail})
# 	else:
# 		return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})


def payment_given(request, id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
	if len(check_status) == 1:
		if request.method == 'POST':
			project_bidding_rate = project_bid_rate.objects.filter(project=id)
			for x in project_bidding_rate:
				project = x.project
				user = x.user
				total_amount = x.bid_rate
			received_amount = request.POST['received_amount']
			payment_record = payment_report(project=project, user=user, total_amount=total_amount, received_amount=received_amount)
			payment_record.save()
			param_dict={
            # 'MID': 'YOUR MERCHANT ID',
            'MID': 'DIY12386817555501617',
            'ORDER_ID': payment_record.project,
            'TXN_AMOUNT': received_amount,
            'CUST_ID': 'profile.email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/hirer/handlerequest/',
    		}
		
			param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
			
			return  render(request, 'hirer/paytm.html', {'param_dict': param_dict})
			return redirect('/hirer/paystatus')
			
		else:
			project_bidding_rate_detail = project_bid_rate.objects.filter(project=id)
			return render(request, 'hirer/paystatus.html', {'project_bidding_rate_detail':project_bidding_rate_detail})
	else:
		return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})

# @csrf_exempt
# def handlerequest(request):
# 	# pass
# 	return HttpResponse('Payment is Done')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Payment Successful')

        else:
            print('Payment was not successful because' + response_dict['RESPMSG'])
    return render(request, 'hirer/paymentstatus.html', {'response': response_dict})
