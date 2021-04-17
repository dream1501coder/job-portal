from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from freelancer.models import profile
from django.contrib.auth.models import User
from .models import User
from admin1.models import add_project
from django.http import HttpResponse
from hirer.models import project_bid_rate, payment_report

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
			return redirect('/hirer/postjob')
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')


def project_biding_rate(request):

	if request.user.is_authenticated:

		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			
			profile_bid_rate_detail = project_bid_rate.objects.all()
			for x in profile_bid_rate_detail:
				project_name = add_project.objects.filter(user_id=request.user)
				for y in project_name:
					if x.project == y.projectname:
						all_project = project_bid_rate.objects.filter(project=y.projectname)
					else:
						all_project=''
			profile_data = profile.objects.filter(user_id=request.user)
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
			payment_received_status = payment_report.objects.all()
			return render(request, 'hirer/paystatus.html',{'profile_payent_status':profile_payent_status,'payment_received_status':payment_received_status})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})	
	else:
		return redirect('/hirer/login')

# def workstatus(request):
# 	if request.user.is_authenticated:
# 		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
# 		if len(check_status) == 1:
# 			profile_bid_rate_detail = project_bid_rate.objects.filter(user__username=request.user)
# 			profile_data = profile.objects.filter(user_id=request.user)
# 			return render(request, 'hirer/workstatus.html', {'profile_data':profile_data, 'profile_bid_rate_detail':profile_bid_rate_detail})
# 		else:
# 			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
# 	else:
# 		return redirect('/hirer/login')


def workstatus(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			profile_data = add_project.objects.filter(user_id=request.user)
			if len(profile_data)==0:
				profile_bid_rate_detail=''
				return render(request, 'hirer/workstatus.html', {'profile_data':profile_data, 'profile_bid_rate_detail':profile_bid_rate_detail})
			else:
				
				for x in profile_data:
					profile_bid_rate_detail = project_bid_rate.objects.filter(project=x.projectname)
					
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
				return render(request, 'hirer/layout/master.html', {'error':'please change username'})
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=request.POST['password'])
				hirer_profile=profile(user_id=user, phonenumber=request.POST['phonenumber'], address=request.POST['address'], technology=request.POST['technology'], status="Not Active", is_login="hirer")
				hirer_profile.save()
				return redirect('/hirer')
		else:
			return render(request, 'hirer/layout/master.html' , {'error':'please check password and confirmpassword'})
	else:
		return render(request, 'hirer/layout/master.html')


def bid_rate_show(request, id):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='hirer')
		if len(check_status) == 1:
			project_bid_show_detail = project_bid_rate.objects.filter(project=id)
			for x in project_bid_show_detail:
				project_id = x.project
			project_information = 	add_project.objects.filter(projectname=project_id)
			return render(request, 'hirer/project_bid.html', {'project_bid_show_detail':project_bid_show_detail, 'project_information':project_information})
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/hirer/login')

def project_bidding_approval(request, id):
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
			project_bid_rate_store = project_bid_rate(id=id, bid_rate=bid_rate, project=project, user=user, comments=comments, status=status)
			project_bid_rate_store.save()
			return redirect('/hirer/project_bid_rate')
		else:
			return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})

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
			return redirect('/hirer/paystatus')
		else:
			project_bidding_rate_detail = project_bid_rate.objects.filter(project=id)
			return render(request, 'hirer/paystatus.html', {'project_bidding_rate_detail':project_bidding_rate_detail})
	else:
		return render(request, 'hirer/login.html', {'error_login': "Please Check Credentials"})
