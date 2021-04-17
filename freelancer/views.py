from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import auth
from admin1.models import add_project
from hirer.models import project_bid_rate, comment, payment_report
from django.core.files.storage import FileSystemStorage
from .models import profile
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
	return render(request, 'freelancer/index.html')


def show_profile(request):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		profile_data = profile.objects.filter(user_id=request.user)
		return render(request, 'freelancer/profile.html',{'profile_data':profile_data})
		# return HttpResponse(request,profile_data)
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})


def edit_profile(request,id):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
		if len(check_status) == 1:
			profile_data = profile.objects.filter(user_id=id)
			return render(request, 'freelancer/edit_profile.html', {'profile_data':profile_data})
		else:
			return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})
	else:
		return render(request, 'freelancer/index.html')
	
def update_profile(request,id):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
		if len(check_status) == 1:
			if request.method == 'POST':
				user = User.objects.filter(id=id).update(username=request.POST['username'], first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'])
				hirer_profile=profile.objects.filter(user_id=id).update(phonenumber=request.POST['phonenumber'], address=request.POST['address'], technology=request.POST['technology'], status="Not Active", is_login="freelancer")
				return redirect('/profile')
			else:
				profile_data = profile.objects.filter(user_id=id)
				return render(request,  'freelancer/edit_profile.html', {'profile_data':profile_data})
		else:
			return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})
	else:
		return render(request, 'freelancer/index.html')



def jobfeed(request):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		all_data =add_project.objects.filter(status="Approved").order_by('-create_at')
		paginator = Paginator(all_data, 5)
		page = request.GET.get('page')
		try:
			all_data = paginator.page(page)
		except PageNotAnInteger:
			all_data = paginator.page(1)
		except EmptyPage:
			all_data = paginator.page(paginator.num_pages)
		return render(request, 'freelancer/jobfeed.html',{'job_data':all_data})
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})

def user_signup(request):
	if request.method == 'POST':
		if request.POST['password'] == request.POST['confirmpassword']:
			try:
				user = User.objects.get(username=request.POST['username'])
				return render(request, 'freelancer/index.html', {'error':'please change username'})
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=request.POST['password'])
				auth.login(request, user)
				user_id = request.user
				phonenumber = request.POST['phonenumber']
				address = request.POST['address']
				technology = request.POST['technology']
				image = request.FILES['image']
				fs= FileSystemStorage()
				filename= fs.save(image.name, image)
				url1=fs.url(filename)
				status = "Not Active"
				is_login = "freelancer"
				profile_data_store = profile(user_id=user, phonenumber=phonenumber, address=address, technology=technology, image=url1, status=status, is_login=is_login)
				profile_data_store.save()
				return redirect('/')
		else:
			return render(request, 'freelancer/index.html' , {'error':'please check password and confirmpassword'})
	else:
		return render(request, 'freelancer/index.html')
	

def logout(request):
	auth.logout(request)
	return redirect('/')

def login(request):
	if request.method == 'POST' :
		username= request.POST['username']
		password= request.POST['password']
		user=authenticate(request, username=username, password=password)
		check_status = profile.objects.filter(user_id=user).filter(is_login='freelancer')
		if len(check_status) == 1:
			if user is not None:
				auth.login(request, user)
				return redirect('/')
			else:
				return redirect('/')
		else:
			return render(request, 'index.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/')

def bidding_rate(request, id):
	
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		if request.method == 'POST':
			bid_rate = request.POST['bid_rate']
			comments = request.POST['comment']
			status = "Not Approved"
			progress = ""
			project_bid_rate_store = project_bid_rate(bid_rate=bid_rate, project=id, user=request.user, comments=comments, status=status,progress=progress)
			project_bid_rate_store.save()
			return redirect('/freelancer/jobfeed')
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})

def report(request):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		project_bid_detail = project_bid_rate.objects.filter(user=request.user)
		payment_received_status = payment_report.objects.all()
		return render(request, 'freelancer/report.html',{'project_bid_detail':project_bid_detail, 'payment_received_status':payment_received_status})
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})

def bidding_starting_progress(request,id):

	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		project_bid_starting_detail_fetch = project_bid_rate.objects.filter(id=id).filter(status='Not Approved')
		if len(project_bid_starting_detail_fetch) == 1:
			return redirect('/freelancer/report')
		project_bid_starting_detail = project_bid_rate.objects.filter(id=id)
		for x in project_bid_starting_detail:
				user = x.user
				project = x.project
				bid_rate = x.bid_rate
				comments = x.comments
				status = "Approved"
				progress = "starting"
		project_bid_rate_store = project_bid_rate(id=id, bid_rate=bid_rate, project=project, user=user, comments=comments, status=status, progress=progress)
		project_bid_rate_store.save()
		return redirect('/freelancer/report')
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})


def bidding_intermediate_progress(request,id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		project_bid_intermidiate_detail_fetch = project_bid_rate.objects.filter(id=id).filter(status='Not Approved')
		if len(project_bid_intermidiate_detail_fetch) == 1:
			return redirect('/freelancer/report')
		project_bid_intermidiate_detail = project_bid_rate.objects.filter(id=id)
		for x in project_bid_intermidiate_detail:
				user = x.user
				project = x.project
				bid_rate = x.bid_rate
				comments = x.comments
				status = "Approved"
				progress = "intermediate"
		project_bid_rate_store = project_bid_rate(id=id, bid_rate=bid_rate, project=project, user=user, comments=comments, status=status, progress=progress)
		project_bid_rate_store.save()
		return redirect('/freelancer/report')
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})

def bidding_mediate_progress(request,id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		project_bid_intermidiate_detail_fetch = project_bid_rate.objects.filter(id=id).filter(status='Not Approved')
		if len(project_bid_intermidiate_detail_fetch) == 1:
			return redirect('/freelancer/report')
		project_bid_intermidiate_detail = project_bid_rate.objects.filter(id=id)
		for x in project_bid_intermidiate_detail:
				user = x.user
				project = x.project
				bid_rate = x.bid_rate
				comments = x.comments
				status = "Approved"
				progress = "mediate"
		project_bid_rate_store = project_bid_rate(id=id, bid_rate=bid_rate, project=project, user=user, comments=comments, status=status, progress=progress)
		project_bid_rate_store.save()
		return redirect('/freelancer/report')
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})

def bidding_finished_progress(request,id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		project_bid_intermidiate_detail_fetch = project_bid_rate.objects.filter(id=id).filter(status='Not Approved')
		if len(project_bid_intermidiate_detail_fetch) == 1:
			return redirect('/freelancer/report')
		project_bid_intermidiate_detail = project_bid_rate.objects.filter(id=id)
		for x in project_bid_intermidiate_detail:
				user = x.user
				project = x.project
				bid_rate = x.bid_rate
				comments = x.comments
				status = "Approved"
				progress = "finished"
		project_bid_rate_store = project_bid_rate(id=id, bid_rate=bid_rate, project=project, user=user, comments=comments, status=status, progress=progress)
		project_bid_rate_store.save()
		return redirect('/freelancer/report')
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})

def bidding_completed_progress(request,id):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		project_bid_intermidiate_detail_fetch = project_bid_rate.objects.filter(id=id).filter(status='Not Approved')
		if len(project_bid_intermidiate_detail_fetch) == 1:
			return redirect('/freelancer/report')
		project_bid_intermidiate_detail = project_bid_rate.objects.filter(id=id)
		for x in project_bid_intermidiate_detail:
				user = x.user
				project = x.project
				bid_rate = x.bid_rate
				comments = x.comments
				status = "Approved"
				progress = "completed"
		project_bid_rate_store = project_bid_rate(id=id, bid_rate=bid_rate, project=project, user=user, comments=comments, status=status, progress=progress)
		project_bid_rate_store.save()
		return redirect('/freelancer/report')
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})

def contact(request):
		if request.method == 'POST':
			fname = request.POST['fname']
			lname = request.POST['lname']
			email = request.POST['email']
			subject = request.POST['subject']
			message = request.POST['message']
			message_stored = comment(fname=fname,lname=lname,email=email,subject=subject,message=message)
			message_stored.save()
			return redirect('/freelancer/index.html')
		else:
			return render(request, 'freelancer/contact.html', {'error_login': "Please Check Credentials"})

def registration(request):
	return render(request, 'freelancer/registration.html')