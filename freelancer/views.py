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
from django.contrib import messages #import messages

def index(request):
	all_data =add_project.objects.filter(status="Approved").order_by('-create_at')
		
	return render(request, 'freelancer/index.html',{'job_data':all_data})

	# return render(request, 'freelancer/index.html')

def searchMatch(query,item):
	# return true  only if query matches the item
	if query in item.front_end.lower() or query in item.back_end.lower():
		return True
	else:
		return False

def search(request):
	query = request.GET.get('search')
	if len(query)==0:
		messages.success(request,'please enter keywords to find')
		return redirect('freelancer/jobfeed')
	else:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
		if len(check_status) == 1:
			all_data1 =add_project.objects.filter(status="Approved").order_by('-create_at')
			all_data = [item for item in all_data1 if searchMatch(query,item)]
	
			return render(request, 'freelancer/search.html',{'job_data':all_data,'keyword':query})
		
		# return render(request, 'freelancer/search.html',{'job_data':"No Results Found",'keyword':query})
		else:
			return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})


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
			messages.success(request,'fisrt logout from another user account')
			return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})
	else:
		messages.success(request,'Please Check Credentials')
		return render(request, 'freelancer/index.html')
	
def update_profile(request,id):
	if request.user.is_authenticated:
		check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
		if len(check_status) == 1:
			if request.method == 'POST':
				user = User.objects.filter(id=id).update(username=request.POST['username'], first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'])

				hirer_profile=profile.objects.filter(user_id=id).update(phonenumber=request.POST['phonenumber'], address=request.POST['address'], technology=request.POST['technology'], status="Not Active", is_login="freelancer")
				messages.success(request,'Profile updated successfully')
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
		# all_data = project_bid_rate.objects.filter(status="Not Approved")

		# private_galleries = add_project.objects.filter(status="Approved").filter(root_gallery__isnull = True).exclude(id__in = [x.gallery.id for x in user_galleries])
		paginator = Paginator(all_data, 4)
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


def report(request):
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		project_bid_detail = project_bid_rate.objects.filter(user=request.user)
		payment_received_status = payment_report.objects.all()
		return render(request, 'freelancer/report.html',{'project_bid_detail':project_bid_detail, 'payment_received_status':payment_received_status})
	else:
		return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})

def user_signup(request):
	if request.method == 'POST':
		if request.POST['password'] == request.POST['confirmpassword']:
			try:
				user = User.objects.get(username=request.POST['username'])
				messages.success(request,'This username is taken, please choose another username')
				return render(request, 'freelancer/registration.html', {'error':'please change username'})
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
				messages.success(request, 'Welcome user, registered successfully')
				return redirect('/')
		else:
			messages.success(request,'password and confirm password should match')
			return render(request, 'freelancer/index.html' , {'error':'please check password and confirmpassword'})
	else:
		return render(request, 'freelancer/index.html')
	

def logout(request):
	auth.logout(request)
	return redirect('/')

# def login(request):
# 	if request.method == 'POST' :
# 		username= request.POST['username']
# 		password= request.POST['password']
# 		user=authenticate(request, username=username, password=password)
# 		check_status = profile.objects.filter(user_id=user).filter(is_login='freelancer')
# 		if len(check_status) == 1:
# 			if user is not None:
# 				auth.login(request, user)
# 				return redirect('/')
# 			else:
# 				# messages.error(request,'Please Check Credentials')
# 				return redirect('/')
# 		else:
# 			messages.error(request,'Please Check Credentials and try again')
			
# 			return render(request, 'freelancer/index.html', {'error_login': "Please Check Credentials"})
# 	else:
# 		return redirect('/')

def bidding_rate(request, id):
	
	check_status = profile.objects.filter(user_id=request.user).filter(is_login='freelancer')
	if len(check_status) == 1:
		if request.method == 'POST':
			bid_rate = request.POST['bid_rate']
			comments = request.POST['comment']
			status = "Not Approved"
			progress = ""
			if len(bid_rate)==0 and len(comments)==0:
				messages.success(request,' please enter your bidrate and comments before submit')
				return redirect('/jobfeed')
			else:
				project_bid_rate_store = project_bid_rate(bid_rate=bid_rate, project=id, user=request.user, comments=comments, status=status,progress=progress)
				project_bid_rate_store.save()
				messages.success(request,'your bidrate has been sent,We wil get back to you very soon!')
				return redirect('/freelancer/jobfeed')
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
		messages.success(request,'Project status has been sent to hirer')
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
		messages.success(request,'Project status has been sent to hirer')
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
		messages.success(request,'Project status has been sent to hirer')
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
		messages.success(request,'Project status has been sent to hirer')
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
		messages.success(request,'Project status has been sent to hirer')
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
			messages.success(request, 'Thanks for contacting us. We wil get back to you soon!')
			return redirect('/')
			# return render_to_response('template_name', message='Save complete')
		else:
			messages.error(request, 'oops!!! something went wrong')

			return render(request, '/', {'error_login': "Please Check Credentials"})


def registration(request):
	return render(request, 'freelancer/registration.html')

def logins(request):
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
				messages.error(request,'Please Check Credentials')
				return redirect('/')
		else:
			messages.error(request,'Please Check Credentials and try again')
			
			return render(request, 'freelancer/login.html', {'error_login': "Please Check Credentials"})
	else:
		return redirect('/')

def login(request):
	return render(request, 'freelancer/login.html')