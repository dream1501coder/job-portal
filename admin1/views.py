from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import auth
from freelancer.models import profile
from .models import add_project
from hirer.models import project_bid_rate, payment_report, comment



def show_profile(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
		if len(check_status) == 1:
			profile_data = profile.objects.filter(user_id=request.user)
			return render(request, 'admin1/profile.html',{'profile_data':profile_data})
		else:
			return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/admin1/login')


def project_status(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
		if len(check_status) == 1:
			project_detail = add_project.objects.order_by('-id')
			profile_data = profile.objects.filter(user_id=request.user)
			return render(request, 'admin1/project_status.html',{'profile_data':profile_data, 'project_detail':project_detail})
		else:
			return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/admin1/login')

def freelancer(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
		if len(check_status) == 1:
			freelancer_data = profile.objects.filter(is_login="freelancer").order_by('-id')
			return render(request, 'admin1/freelancer.html',{'freelancer_data':freelancer_data})
		else:
			return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/admin1/login')

def hirer(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
		if len(check_status) == 1:
			hirer_detail = profile.objects.filter(is_login="hirer").order_by('-id')
			return render(request, 'admin1/hirer.html',{'hirer_detail':hirer_detail})
		else:
			return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/admin1/login')

def paymentsection(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
		if len(check_status) == 1:
			profile_data = profile.objects.filter(user_id=request.user)
			payment_received_status = payment_report.objects.all()
			project_info = project_bid_rate.objects.all()
			return render(request, 'admin1/paymentsection.html',{'payment_received_status':payment_received_status, 'project_info':project_info, 'profile_data':profile_data})
		else:
			return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/admin1/login')

def projectbids(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
		if len(check_status) == 1:
			project_bid_detail = project_bid_rate.objects.filter(status="Approved").order_by("-id")
			return render(request, 'admin1/projectbids.html',{'project_bid_detail':project_bid_detail})
		else:
			return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})

def reports(request):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
		if len(check_status) == 1:
			all_comment = comment.objects.all().order_by('-id')
			return render(request, 'admin1/reports.html', {'all_comment':all_comment})
		else:
			return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/admin1/login')

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['pass']
		user = authenticate(request, username=username, password=password)
		
		check_status = profile.objects.filter(user_id=user).filter(is_login='admin1')
		
		if len(check_status) == 1:
			if user is not None:
				auth.login(request, user)
				return redirect('/admin1')
		else:
			return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})
	else:
		return render(request, 'admin1/login.html')

def logout(request):
	auth.logout(request)
	return redirect('/admin1/login')

def hirer_delete(request, id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
	if len(check_status) == 1:
		hirer_delete_detail = profile.objects.filter(id=id)
		hirer_delete_detail.delete()
		return redirect('/admin1')
	else:
		return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})

def hirer_activation(request, id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
	if len(check_status) == 1:
		hirer_activation_detail = profile.objects.filter(id=id)
		for x in hirer_activation_detail:
			user_id = x.user_id
			phonenumber =  x.phonenumber
			address = x.address
			technology = x.technology
			print(user_id)
			hirer_profile_stored=profile(id=id, user_id=user_id, phonenumber=phonenumber, address=address, technology=technology, status="Activate", is_login="hirer")
			hirer_profile_stored.save()	
		return redirect('/admin1/hirer')
	else:
		return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})

def freelance_data_delete(request, id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
	if len(check_status) == 1:
		freelancer_profile_delete = profile.objects.filter(id=id)
		freelancer_profile_delete.delete()
		return redirect('/admin1/freelancer')
	else:
		return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})

def bid_rate_show(request):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
	if len(check_status) == 1:
		return render(request, 'admin1/projectbids.html')
	else:
		return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})

def project_approve(request, id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
	if len(check_status) == 1:
		project_approve_detail = add_project.objects.filter(id=id)
		for x in project_approve_detail:
			user_id = x.user_id
			projectname = x.projectname
			description = x.description
			amount = x.amount
			start_time = x.start_time
			end_time = x.end_time
			front_end = x.front_end
			back_end = x.back_end
			status = "Approved"
			project_detail_store = add_project(id=id, user_id=user_id, projectname=projectname, description=description, start_time=start_time, end_time=end_time, amount=amount, front_end=front_end,back_end=back_end, status=status)
			project_detail_store.save()
			return redirect('/admin1/Project')
	else:
		return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})

def freelance_data_active(request, id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
	if len(check_status) == 1:
		freelance_active = profile.objects.filter(id=id)
		for x in freelance_active:
			user_id = x.user_id
			phonenumber =  x.phonenumber
			address = x.address
			technology = x.technology
			freelancer_profile_stored=profile(id=id, user_id=user_id, phonenumber=phonenumber, address=address, technology=technology, status="Activate", is_login="freelancer")
			freelancer_profile_stored.save()	
		return redirect('/admin1/freelancer')
	else:
		return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})


def freelance_data_delete(request, id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='admin1')
	if len(check_status) == 1:
		freelance_delete = profile.objects.filter(id=id)
		freelance_delete.delete()
		return redirect('/admin1/freelancer')
	else:
		return render(request, 'admin1/login.html', {'error_login': "Please Check Credentials"})
