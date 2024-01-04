from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout, login as dj_login
from django.views import View
from.models import *
from ebook_apps.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django_user_agents.utils import get_user_agent
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from ebook_apps.views import View
from django.core.files.storage import default_storage
from django.db.models import Sum,F
from django.urls import reverse
from django.db.models import Subquery, OuterRef
from django.db.models import Avg
from datetime import datetime
from datetime import timedelta
from django.db.models.functions import Coalesce
from django.db.models import F, ExpressionWrapper, fields,Value
import pdf2image
from django.core.mail import send_mail

from itertools import groupby
# Create your views here.
class HomeView(View):
    def get(self, request):
        user_visit = UserVisit.objects.all().count()
        home_banner = Home.objects.all()
        faq = Faq.objects.all()
        how_does = HowDoesebooks.objects.all()
        ebook_exp = EBookExperience.objects.all()
        our_service = OurServices.objects.all()
        our_partner = OurPartner.objects.all()
        studio = StudioExperience.objects.all()
        my_collection = Collections.objects.all().order_by('-id')[:3]
        newest_books = Books.objects.filter(is_active=True).order_by('-id')[0:3]
        # popular_books = Books.objects.filter(is_active=True).order_by('-id')[:3]
        learn = LearnEverything.objects.all()
        footer = Footer.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        visit_count = User.objects.filter(is_superuser=False).count()


        popular_books = BookVisit.objects.values('books__title', 'books__image', 'books__category__book_category', 'books__created_at','books__updated_at','books_id').annotate(total_visits=Sum('visit_count')).order_by('-total_visits')[:3]
        for book in popular_books:
            book['book_url'] = reverse('BookDetail', kwargs={'id': book['books_id']})


        books_category = BookVisit.objects.filter().order_by('-visit_count')[:3]
        return render(request,'lowafrecia/home.html',{'book_category':book_category,'home_banner': home_banner,'how_does': how_does,'ebook_exp': ebook_exp,'our_service': our_service,'our_partner': our_partner,
        'studio': studio,'my_collection': my_collection,'newest_books': newest_books,'learn': learn,
        'footer': footer,'active': 'active12','visit_count':visit_count,'user_visit':user_visit,'faq':faq,'books_category':books_category,'popular_books':popular_books})
    def post(self, request):
        email = request.POST.get('email')
        RequestDemo.objects.create(email=email)
        messages.success(request,'Demo Informations Send Successfully')
        return redirect('home')



######## books by category ##
class BooksByCategory(View):
    def get(self, request):
        footer = Footer.objects.all()
        st = request.GET.get('searchname')
        category_filter = Q()
        if st is not None:
            category_filter |= Q(category__book_category__icontains=st)
            category_filter |= Q(author__icontains=st)
            category_filter |= Q(publication_date__icontains=st)
            category_filter |= Q(price__icontains=st)
            category_filter |= Q(title__icontains=st)
        category_books = Books.objects.filter(category_filter, is_active=True)
        books_by_category = {}
        categories = category_books.values_list('category__book_category', flat=True).distinct()
        for category in categories:
            books_in_category = category_books.filter(category__book_category=category).order_by('-id')[:3]
            books_by_category[category] = books_in_category
        return render(request, 'lowafrecia/book_by_category.html', {'books_by_category': books_by_category, 'footer': footer})



class Contact_Us(View):
    def get(self,request):
        data = ContactUs.objects.all()
        contact_banner = ContactBanner.objects.all()
        getin_touch = GetInTouch.objects.all()
        footer = Footer.objects.all()
        learn = LearnEverything.objects.all()
        faq = Faq.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/contactus.html',{'data':data, 'book_category':book_category,'contact_banner':contact_banner,'getin_touch':getin_touch,'footer':footer,'active5':'active12','learn':learn,'faq':faq,'book_category':book_category})
    def post(self,request):
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        company = request.POST.get('company')
        business_email = request.POST.get('business_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        ContactUs.objects.create(name=name,mobile_number=mobile_number,company=company,business_email=business_email,subject=subject,message=message)
        messages.success(request,'Contact Us Informations Send Successfully')
        return redirect('home')



class AboutUs(View):
    def get(self,request):
        about_banner = AboutBanner.objects.all()
        the_foundation = TheFoundation.objects.all()
        the_book = AboutTheBook.objects.all()
        our_partner = OurPartner.objects.all()
        overview = Overview.objects.all()
        learn = LearnEverything.objects.all()
        footer = Footer.objects.all()
        faq = Faq.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/AboutUs.html',{'footer':footer,'about_banner':about_banner,'the_foundation':the_foundation,'the_book':the_book,'our_partner':our_partner,'learn':learn,'overview':overview,'faq':faq,'book_category':book_category})




class CollectionAll(View):
    def get(self, request):
        if request.user.is_authenticated:  
            collection_all = Collections.objects.all().order_by('-id')
            footer = Footer.objects.all()
            book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
            book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
            return render(request, 'lowafrecia/viewall.html', {'book_category':book_category,'collection_all': collection_all, 'footer': footer,'user': request.user,'book_category':book_category})
        else:
            return redirect("home")

class StudentsLibrary(View):
    def get(self, request):
        if request.user.is_authenticated:
            is_student = request.user.is_student
            user_ = User.objects.get(id=request.user.added_user)

            if is_student:
                book_list = user_.books.all().order_by('-id')
            else:
                book_list = user_.books.filter(is_active=True).order_by('-id')

            st = request.GET.get('searchname')

            if st is not None:
                book_list = book_list.filter(
                    Q(title__icontains=st) |
                    Q(author__icontains=st) |
                    Q(publication_date__icontains=st) |
                    Q(price__icontains=st) |
                    Q(category__book_category__icontains=st)
                )

            book_lists = []

            for book in book_list:
                favorite = 1 if Favorite.objects.filter(fav_book=book, user=request.user).exists() else 0

                completed = 'Progress'
                if BookVisit.objects.filter(user=request.user, books=book, completed=True).exists():
                    completed = 'Completed'

                d = {
                    "id": book.id,
                    "category": book.category.book_category,
                    "title": book.title,
                    "image": book.image,
                    "favorite": favorite,
                    "readingStatus": completed
                }
                book_lists.append(d)
            # Group books by category
            grouped_books = {key: list(group) for key, group in groupby(book_lists, key=lambda x: x['category'])}

            return render(request, 'lowafrecia/student_library.html', {
                'active16': 'active20',
                'grouped_books': grouped_books,
                'book_list': book_list if is_student else None
            })
        else:
            messages.error(request, 'Login is required to access books. Please log in or register as a new user.')
            return redirect('home')



class BlogsView(View):
    def get(self,request):
        blog_banner = BlogsBanner.objects.all()
        footer = Footer.objects.all()
        blog_details = BlogsDetails.objects.all()
        recent_blogsdetails = BlogsDetails.objects.all().order_by('-id')[:5]
        # home_banner = Home.objects.all()
        faq = Faq.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/Blogs.html',{'recent_blogsdetails':recent_blogsdetails,'blog_banner':blog_banner,'footer':footer,'blog_details':blog_details,'faq':faq,'book_category':book_category})

class RequestAdemo(View):
    def get(self,request):
        request_data = RequestADemo.objects.all()
        blog_details = BlogsDetails.objects.all()
        blog_banner = BlogsBanner.objects.all()
        footer = Footer.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/Blogs.html',{'request_data':request_data,'blog_details':blog_details,
        'blog_banner':blog_banner,'footer':footer,'book_category':book_category})
    def post(self,request):
        request_data = RequestADemo.objects.all()
        blog_details = BlogsDetails.objects.all()
        blog_banner = BlogsBanner.objects.all()
        footer = Footer.objects.all()
        first_name =request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        message = request.POST.get('message')
        business_email = request.POST.get('business_email')
        messages.success(request,"Message Send Sucessfully")
        RequestADemo.objects.create(first_name=first_name,last_name=last_name,message=message,business_email=business_email)
        return render(request,'lowafrecia/Blogs.html',{'request_data':request_data,'blog_details':blog_details,
        'blog_banner':blog_banner,'footer':footer})






######### digital publishing
class DigitalPublishing(View):
    def get(self,request):
        digital_banner = DigitalPubBanner.objects.all()
        footer = Footer.objects.all()
        learn = LearnEverything.objects.all()
        cater_to = CaterToVarious.objects.all()
        secure_dis = SecuredDistribution.objects.all()
        get_your = GetYourBranded.objects.all()
        multi_device = MultiDevices.objects.all()
        easily_inter = Easilyintegrates.objects.all()
        faq = Faq.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/DigitalPublishing.html',{'cater_to':cater_to,'digital_banner':digital_banner,'footer':footer,
        'secure_dis':secure_dis,'get_your':get_your,'learn':learn,'multi_device':multi_device,'easily_inter':easily_inter,'active1':'active12','faq':faq,'book_category':book_category})
    def post(self,request):
        data = RequestDemo.objects.all()
        email = request.POST.get('email')
        RequestDemo.objects.create(email=email)
        return redirect('home')



class EbookStore(View):
    def get(self,request):
        book_banner = BookStoreBanner.objects.all()
        your_webstore = YourBrandedWebstore.objects.all()
        footer = Footer.objects.all()
        learn = LearnEverything.objects.all()
        easy_inte = EasyIntegration.objects.all()
        social_network = SocialNetwork.objects.all()
        fully_responsive = FullyResponsive.objects.all()
        faq = Faq.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/ebookStore.html',{'book_banner':book_banner,'your_webstore':your_webstore,'footer':footer,'learn':learn,
        'easy_inte':easy_inte,'social_network':social_network,'fully_responsive':fully_responsive,'active6':'active12','faq':faq,'book_category':book_category})
    def post(self,request):
        data = RequestDemo.objects.all()
        email = request.POST.get('email')
        RequestDemo.objects.create(email=email)
        return redirect('home')
    
from pdf2image import convert_from_path
class BookDetails(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            user = request.user.institute
            footer = Footer.objects.all()
            book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
            member = User.objects.filter(is_student=True, is_active=True, is_superuser=False, is_staff=False, is_organization=False).count()
            book_list = Books.objects.filter(id=id,is_active=True)  
            book = Books.objects.get(id=id,is_active=True)

            book.viewed_at = timezone.now()
            book.save() 
            book = Books.objects.get(id=id,is_active=True)
            add_recent_view_book = Recently_Viewed.objects.create(user=request.user, book=book)
            completed = False
            if BookVisit.objects.filter(user=request.user, books=book).exists():
                last_visit_book = BookVisit.objects.filter(user=request.user, books=book).last()
                
                if last_visit_book.completed == True:
                    completed = True
                else:
                    completed = False
            book_visit = ''
            if request.user.is_student == True:
                book_visit = BookVisit.objects.create(user=request.user, books=book, completed=completed, institute_name=request.user.institute)
            return render(request, 'lowafrecia/BookDetails.html', { 'book_obj':book,'footer': footer,'book_list': book_list,'member':member, "id":id, "book_visit":book_visit,'book_category':book_category})
        else:
            messages.error(request, 'Login is required to access book, Please login if register account or register as new user')
            return redirect('home')
    

class UpdateEndTimeView(View):
    def get(self, request, id):
        book_id = request.GET.get('book_id')
        book = Books.objects.get(id=id, is_active=True)
        # Get the latest BookVisit for the user and book
        book_visit = BookVisit.objects.filter(user=request.user, books=book).latest('start_time')

        # Update end_time
        book_visit.end_time = timezone.now()
        book_visit.save()

        return JsonResponse({'success': True})

class UpdateBookReadingStatus(View):
    def get(self, request, id):
        try:
            # Fetch the book visit record
            book_visit = BookVisit.objects.filter(books_id=id)

            # Update the book status
           
            for book in book_visit:
                book.completed = not book.completed
                book.save()
            book_visit = BookVisit.objects.filter(books_id=id).last()
            
            return JsonResponse({'success': True, 'completed': book_visit.completed})
        except BookVisit.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'BookVisit record not found'})

class CollectionDetails(View):
    def get(self,request,id):
        if request.user.is_authenticated: 
            footer = Footer.objects.all()
            learn = LearnEverything.objects.all()
            collection_member = User.objects.filter(is_superuser=False).count()
            collection = CollectionsList.objects.filter(Collections_name=Collections.objects.get(id=id)).order_by('-id')
            st = request.GET.get('searchname')
            if st is not None:
                collection = CollectionsList.objects.filter(
                    Q(books_id__author__icontains=st) |
                    Q(books_id__title__icontains=st) |
                    Q(books_id__heading__icontains=st)
                )
            paginator = Paginator(collection, per_page=1)
            page_number = request.GET.get("page", 1)
            page_object = paginator.get_page(page_number)
            return render(request,'lowafrecia/collectionDetails.html',{'learn':learn,'footer':footer,'collection':collection,'page_object':page_object,'collection_member':collection_member})
        else:
            return redirect('home')


class NewestViewAll(View):
    def get(self,request):
        if request.user.is_authenticated: 
            newestbook_all = Books.objects.filter(is_active=True).order_by('-id')
            footer = Footer.objects.all()
            return render(request,'lowafrecia/newestview_all.html',{'newestbook_all':newestbook_all,'footer':footer})
        else:
            return redirect('home')




class TermConditions(View):
    def get(self,request):
        terms_condition = TermsCondition.objects.all()
        footer = Footer.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/Term&Condition.html',{'terms_condition':terms_condition,'footer':footer,'book_category':book_category})


class PrivacyPolicys(View):
    def get(self,request):
        privacy_policy = PrivacyPolicy.objects.all()
        footer = Footer.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/privacy_policy.html',{'privacy_policy':privacy_policy,'footer':footer,'book_category':book_category})





class EbookReader(View):
    def get(self, request):
        if request.user.is_authenticated:
            ebook_reader = EbookReaderBanner.objects.all()
            footer = Footer.objects.all()
            is_student = request.user.is_student
            user_ = User.objects.get(id=request.user.added_user)
   
            if is_student:
                book_list = user_.books.all()
                st = request.GET.get('searchname')
                if st is not None:
                    book_list = book_list.filter(
                    Q(title__icontains=st) |
                    Q(author__icontains=st) |
                    Q(publication_date__icontains=st) |
                    Q(price__icontains=st) |
                    Q(category__book_category__icontains=st)
                )
                all_books = Books.objects.none()
            else:
                book_list = book_list.filter(is_active=True).order_by('-id')
                st = request.GET.get('searchname')
                if st is not None:
                    book_list = book_list.filter(
                    Q(title__icontains=st) |
                    Q(author__icontains=st) |
                    Q(publication_date__icontains=st) |
                    Q(price__icontains=st) |
                    Q(category__book_category__icontains=st)
                )

               
            book_lists = []
            completed = 'Progress'
            for book in book_list:
                if Favorite.objects.filter(fav_book=book, user=request.user).exists():
                    favorite = 1
                    
                else:
                    favorite = 0
                completed = "Progress"
                if BookVisit.objects.filter(user=request.user, books=book).exists():
                    last_visit_book = BookVisit.objects.filter(user=request.user, books=book).last()
                    
                    if last_visit_book.completed == True:
                        completed = 'Completed'
                    else:
                        completed = 'Progress'
                
                d = {
                    "id": book.id,
                    "category": book.category,
                    "title": book.title,
                    "image": book.image,
                    "favorite": favorite,
                    "readingStatus":completed
                }
                book_lists.append(d)
            science_books = book_list.filter(category__book_category="science")
            history_books = book_list.filter(category__book_category="history")
            story_books = book_list.filter(category__book_category="story")
            return render(request, 'lowafrecia/customerDashboard.html', {
                'ebook_reader': ebook_reader,
                'footer': footer,
                'active12': 'active20',
                'all_books': book_lists,
                'science_books': science_books,
                'history_books': history_books,
                'story_books': story_books,
                'book_list': book_list if is_student else None  # Use book_list here for students
            })
        else:
            messages.error(request, 'Login is required to access book, Please login if register account or register as new user')
            return redirect('home')







# def recently_view(request):
#     user = request.user
#     recently_viewed = Recently_Viewed.objects.filter(user=user).order_by('-id')[:4]
#     search_query = request.GET.get('searchname')
#     if search_query:
#         # Perform your search on the Books model, not on viewing history.
#         data = Books.objects.filter(
#             Q(title__icontains=search_query) |
#             Q(author__icontains=search_query) |
#             Q(publication_date__icontains=search_query) |
#             Q(price__icontains=search_query) |
#             Q(category__book_category__icontains=search_query)
#             )

#     return render(request, 'lowafrecia/recently_view.html', {'recently_viewed': recently_viewed, 'active13': 'active20'})

from django.db.models import Count

def recently_view(request):
    user = request.user
    st = request.GET.get('searchname')
    recently_viewed = Recently_Viewed.objects.filter(user=user).order_by('-id')

    # Apply search filter if 'st' is not None
    if st:
        recently_viewed = recently_viewed.filter(
            Q(book__title__icontains=st) |
            Q(book__author__icontains=st) |
            Q(book__publication_date__icontains=st) |
            Q(book__price__icontains=st) |
            Q(book__category__book_category__icontains=st)
        )

    unique_book_ids = []
    unique_recently_viewed = []
    for rv in recently_viewed:
        if rv.book_id not in unique_book_ids:
            unique_book_ids.append(rv.book_id)  
            unique_recently_viewed.append(rv)
    unique_recently_viewed = unique_recently_viewed[:3]
    recently_viewed = Recently_Viewed.objects.values('book').annotate(view_count=Count('book')).order_by('-view_count')[:3]

    # Get the top 3 recently viewed books
    top_books = Books.objects.filter(id__in=[item['book'] for item in recently_viewed])
    return render(request, 'lowafrecia/recently_view.html', {'recently_viewed': unique_recently_viewed, 'active13': 'active20'})


from collections import defaultdict
class CustomerDashboard(View):
    def get(self, request):
        user = request.user
        fav_count = Favorite.objects.filter(user=request.user, ).count()
        unique_book_visit_count = BookVisit.objects.filter(user=request.user, institute_name=request.user.institute).values('user', 'books').distinct().count()
        total_time = 0
        book_visits = BookVisit.objects.filter(user=request.user)
        total_time_per_book = defaultdict(int)
        for visit in book_visits:
            # Calculate time difference if start_time and end_time are present
            if visit.start_time and visit.end_time:
                time_difference = visit.end_time - visit.start_time
                total_time_per_book[visit.books_id] += time_difference.total_seconds()

        formatted_times_per_book = {}
        # Convert total_time to hours and minutes for each book
        for book_id, total_time in total_time_per_book.items():
            hours, remainder = divmod(total_time, 3600)
            minutes = remainder / 60

            # Format the time for each book
            if hours >= 1:
                formatted_time = "{:.0f} hours {:.0f} minutes".format(hours, minutes)
            else:
                formatted_time = "{:.2f} minutes".format(minutes).rstrip('0').rstrip('.')

            formatted_times_per_book[book_id] = formatted_time

        total_book = len(formatted_times_per_book)

        # Check if total_book is greater than zero before calculating avg_reading_time
        if total_book > 0:
            total_minutes = sum(float(duration.split()[0]) for duration in formatted_times_per_book.values())
            avg_reading_time = total_minutes / total_book

            hours, minutes = divmod(avg_reading_time, 60)
            if hours >= 1:
                formatted_time = "{:.0f} hours {:.0f} minutes".format(hours, minutes)
            else:
                formatted_time = "{:.2f} minutes".format(minutes).rstrip('0').rstrip('.')
        else:
            formatted_time = 0
        return render(request, 'lowafrecia/Front_Dashboard.html', {'book_visit_count': unique_book_visit_count, 'active11': 'active20', 'formatted_duration_str': formatted_time,'fav_count':fav_count})



class BookVisistList(View):
    def get(self,request):
        recently_viewed = Recently_Viewed.objects.filter(user=request.user).order_by('-id')

    # Apply search filter if 'st' is not None
        unique_book_ids = []
        unique_recently_viewed = []
        for rv in recently_viewed:
            if rv.book_id not in unique_book_ids:
                unique_book_ids.append(rv.book_id)
                unique_recently_viewed.append(rv)
        unique_recently_viewed = unique_recently_viewed[:4]


        # Get the top 3 recently viewed books
        # top_books = Books.objects.filter(id__in=[item['book'] for item in recently_viewed])
        return render(request,'lowafrecia/book_view_list.html',{'book_visit_list':unique_recently_viewed})


class MostPopularBooks(View):
    def get(self, request):
        institute_name = getattr(request.user, 'institute', 'guest')  # Use getattr to provide a default value
        book_visits = BookVisit.objects.filter(institute_name=institute_name)

        total_time_per_book = defaultdict(int)
        visits_per_book = defaultdict(int)
        num_books_to_process = 5  # Set the number of books you want to process

        for visit in book_visits:
            user_visit = BookVisit.objects.filter(books=visit.books, institute_name=request.user.institute).count()
            visits_per_book[visit.books_id] += 1  # Increment the visit count for the book

            if visit.start_time and visit.end_time:
                time_difference = visit.end_time - visit.start_time
                total_time_per_book[visit.books_id] += time_difference.total_seconds()

        # Sort books based on total time spent in descending order
        sorted_data_desc = sorted(total_time_per_book.items(), key=lambda item: item[1], reverse=True)[:num_books_to_process]
        
        # Create a dictionary to store formatted times, visit count, and book objects for each book
        formatted_data_per_book = {}
        for book_id, total_time in sorted_data_desc:
            hours, remainder = divmod(total_time, 3600)
            minutes = remainder / 60
            if hours >= 1:
                formatted_time = "{:.0f} h {:.0f} min".format(hours, minutes)
            else:
                formatted_time = "{:.0f} min".format(minutes)

            try:
                book_object = Books.objects.get(id=book_id)
            except Books.DoesNotExist:
                book_object = None

            formatted_data_per_book[book_id] = {
                'formatted_time': formatted_time,
                'visit_count': visits_per_book[book_id],  # Add visit count to the dictionary
                'book_object': book_object,
            }

        context = {'formatted_data_per_book': formatted_data_per_book,'active10':'active20'}
        return render(request, 'lowafrecia/most-populor-books.html', context)


class AverageTimeSpentBookList(View):
    def get(self, request):
        # Get all book visits for the user
        book_visits = BookVisit.objects.filter(user=request.user)

        total_time_per_book = defaultdict(int)
        for visit in book_visits:
            # Calculate time difference if start_time and end_time are present
            if visit.start_time and visit.end_time:
                time_difference = visit.end_time - visit.start_time
                total_time_per_book[visit.books_id] += time_difference.total_seconds()

        # Create a dictionary to store formatted times and book objects for each book
        formatted_data_per_book = {}

        # Convert total_time to hours and minutes for each book
        for book_id, total_time in total_time_per_book.items():
            hours, remainder = divmod(total_time, 3600)
            minutes = remainder / 60

            # Format the time for each book
            if hours >= 1:
                formatted_time = "{:.0f} h {:.0f} min".format(hours, minutes)
            else:
                formatted_time = "{:.0f} min".format(minutes)

            # Retrieve the Book object
            book_object = Books.objects.get(id=book_id)
            # Add data to the dictionary
            formatted_data_per_book[book_id] = {
                'formatted_time': formatted_time,
                'book_object': book_object,
            }
       
        return render(request, 'lowafrecia/customer_avg_time_book.html', {'formatted_data_per_book': formatted_data_per_book,})
           
        



@require_POST
def favorite(request, book_id):
    user = request.user
    book = get_object_or_404(Books, pk=book_id)
    try:
        favorite = Favorite.objects.get(user=user, fav_book=book)
        favorite.delete()
        is_favorite = False
    except Favorite.DoesNotExist:
        favorite = Favorite(user=user, fav_book=book)
        favorite.save()
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})






def favorite_list(request):
    st = request.GET.get('searchname')
    fav_books = Favorite.objects.filter(user=request.user) 
    if st is not None:
        fav_books = fav_books.filter(
            Q(fav_book__title__icontains=st) |
            Q(fav_book__author__icontains=st) |
            Q(fav_book__publication_date__icontains=st) |
            Q(fav_book__price__icontains=st) |
            Q(fav_book__category__book_category__icontains=st)
        )
    return render(request, 'lowafrecia/favorite.html', {'fav_books': fav_books, 'active14': 'active20'})



# class EbookReader(View):
#     def get(self,request):
#         # if request.user.is_authenticated:
#             ebook_reader = EbookReaderBanner.objects.all()
#             footer = Footer.objects.all()
#             all_book = Books.objects.filter(is_active=True).order_by('-id')
#             st = request.GET.get('searchname')
#             if st is not None:
#                 all_book = Books.objects.filter(
#                     Q(heading__icontains=st) | Q(author__icontains=st) | Q(publication_date__icontains=st) | Q(price__icontains=st) | Q(category__book_category__icontains=st)).exclude(is_active=False)
#                 paginator = Paginator(all_book, per_page=5) 
#             else:
#                 all_book = Books.objects.filter(is_active=True).order_by('-id')  
#                 paginator = Paginator(all_book,per_page=5)  
#             page_number = request.GET.get("page")
#             page_obj = paginator.get_page(page_number)
#             return render(request,'lowafrecia/ebookReader.html',{'ebook_reader':ebook_reader,'footer':footer,'active3':'active12','all_book':all_book,'page_obj':page_obj})
#         # else:
#         #     return redirect('home')


######### indybot views start here.
class Indybot(View):
    def get(self,request):
        footer = Footer.objects.all()
        indy_banner = IndyBotBanner.objects.all()
        use_primary = Useprimary.objects.all()
        indy_responsive = IndybotResponsive.objects.all()
        read_book = ReadYourBook.objects.all()
        learn = LearnEverything.objects.all()
        faq = Faq.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request,'lowafrecia/indyBot.html',{'footer':footer,'indy_banner':indy_banner,'active2':'active12','use_primary':use_primary,'indy_responsive':indy_responsive,'read_book':read_book,'learn':learn,'faq':faq,'book_category':book_category})







class Notification(View):
    def get(self, request):
        notifications = Notifications.objects.filter(receiver=request.user, is_read=False)
        book_invitations = BookInvitation.objects.filter(invited_user=request.user, is_read=False)
        total_count = len(notifications) + len(book_invitations)
        footer = Footer.objects.all()
        book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
        return render(request, 'lowafrecia/notification.html', {'notifications': notifications, 'footer': footer, 'total_count': total_count,'book_category':book_category})


        




##### like views start here..
class Like(View):
    def post(self,request):
        id=request.POST.get('id')
        data= BlogsDetails.objects.get(id=id)
        data.like=data.like+1
        data.save()
        context = {'like_count':data.like}
        return JsonResponse(context)




# class TotalVisits(View):
#     def post(self,request):
#         id = request.POST.get('id')
#         data = TotalVisit.objects.get(id=id)
#        
#         data.user_id += 1
#         data.save()
#         context = {'user_count':data.user_id}
#         return JsonResponse(context)

class EndUserRegister(View):
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        institute =request.POST.get('institute')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email id  Already Exist...? Use Diffrent Email id to Create Account.')
        else:
            user = User.objects.create_user(institute=institute, first_name=first_name,last_name=last_name, email=email, phone_number=phone_number,password=password)
            user.is_enduser=True
            user.save()
            messages.success(request,'User Registration Successfully..!!')
        return redirect('home')



### enduser login views 
def enduser_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request=request, email=email, password=password)
        if user is not None:
            user_agent = get_user_agent(request)
            browser_name = user_agent.browser.family
            try:
                user_visit, created = UserVisit.objects.get_or_create(user=user)
                user_visit.browser_name = browser_name
                user_visit.visit_count += 1
                user_visit.save()
            except Exception as e:
                return redirect('home')
            if user.is_superuser:
                messages.warning(request, 'Superusers are not allowed to log in here.')
            else:
                try:
                    dj_login(request, user)
                    login_time = datetime.now().strftime('%H:%M:%S')

                    ManageLoginTime.objects.create(users=user, login_start_time=login_time,institute=user.institute)
                    return redirect('Customer_dashboard')
                except Exception as e:
                   
                    messages.error(request, 'An error occurred during login.')
                    return redirect('home')
        else:
            messages.warning(request, 'Invalid Email or Password')
    return redirect('home')
  

def enduser_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request=request, email=email, password=password)
        if user is not None:
            user_agent = get_user_agent(request)
            browser_name = user_agent.browser.family
            try:
                user_visit, created = UserVisit.objects.get_or_create(user=user)
                user_visit.browser_name = browser_name
                user_visit.visit_count += 1
                user_visit.save()
            except Exception as e:
                return redirect('home')
            if user.is_superuser or user.is_organization:
                messages.warning(request, 'Superusers and organization are not allowed to log in here.')
            else:
                try:
                    dj_login(request, user)
                    login_time = datetime.now().strftime('%H:%M:%S')
                    messages.success(request, 'Your account has been activated. You can now log in.')
                    if user.is_student:
                        ManageLoginTime.objects.create(users=user, login_start_time=login_time,institute=user.institute)
                        # messages.success(request,'Login successfully!!')
                        return redirect('Customer_dashboard')
                    else:
                        ManageLoginTime.objects.create(users=user, login_start_time=login_time)
                        # messages.success(request,'Login successfully!!')
                        return redirect('NormalDashboard')
                except Exception as e:
                    
                    messages.error(request, 'An error occurred during login.')
                    return redirect('home')
        else:
            messages.warning(request, 'Pls check your email and active your account ')
    return redirect('home')


# a
# def enduser_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request=request, email=email, password=password)
#         if user is not None:
#             user_agent = get_user_agent(request)
#             browser_name = user_agent.browser.family
#             
#             if user.is_superuser:
#                 messages.warning(request, 'Superusers are not allowed to log in here.')
#             else:
#                 dj_login(request, user)
#                 messages.success(request, 'Login Successfully!..')
#                 return redirect('home')
#         else:
#             messages.warning(request, 'Invalid Email or Password')
#     return redirect('home')


# def enduser_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         passwords = request.POST.get('password')
#         
#         user = authenticate(request=request, email=email, password=passwords)
#        
#         
#         if user is not None:
#           
#             if User.objects.filter(email=email):
#              
#                 dj_login(request, user)
#                 messages.success(request,'Login Successfully!..')
#                 return redirect('home')
#             else:
#                 messages.warning(request, 'You Are Not Admin User')
#         else:
#             messages.warning(request, 'Invalid Email or Password')
#     return redirect('home')


###### logout  views start here ##
def user_logout(request):
    user = ManageLoginTime.objects.filter(users=request.user.id).last()
    user.login_end_time = datetime.now().strftime('%H:%M:%S')
    user.save()
    logout(request)
    messages.success(request, "Logged Out Successfully..!!")
    return redirect('home')



class Updateprofile(View):
    def get(self, request):
        if request.user.is_authenticated:
            data=User.objects.filter(id=request.user.id,is_superuser=False)
            footer = Footer.objects.all()
            book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
            return render(request, 'lowafrecia/my_profile.html',{'data':data,'footer':footer,'book_category':book_category})
        return redirect('login')
    def post(self, request):
        id = request.user.id
        usern = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic is not None:
            id = request.user.id
            user = User.objects.get(id=id)
            user.first_name = usern
            user.email = email
            user.last_name = last_name
            user.phone_number = phone_number
            user.profile_pic = profile_pic
            user.save()
            messages.success(request,"User Profile Updated Successfully")
            return redirect('profile')
        else:
            user = User.objects.get(id=id)
            user.first_name = usern
            user.email = email
            user.last_name = last_name
            user.phone_number = phone_number
            user.profile_pic = user.profile_pic
            user.save()
            messages.success(request,"User Profile Updated Successfully")
            return redirect('profile')
        



from django.contrib.auth import update_session_auth_hash
class Change_password(View):
    def post(self, request):
        old_password = request.POST.get('old_password')
        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if old_password and password and confirm_password:
            if request.user.check_password(old_password):
                if password == confirm_password:
                    user = User.objects.get(id=request.user.id)
                    user.set_password(password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password changed successfully.')
                    return redirect('home')  # Replace 'home' with the name of your home page URL pattern
                else:
                    messages.error(request, 'New password and confirm password do not match.')
            else:
                messages.error(request, 'Old password is incorrect.')
        else:
            messages.error(request, 'All fields are required.')

        return redirect('profile')






# class Change_password(View):
#     def post(self, request):
#         id=request.user.id
#         old_password = request.POST.get('old_password')

#         new_password = request.POST.get('new_password')

#         confirm_password = request.POST.get('confirm_password')

#         new_password = confirm_password
#         user = User.objects.get(id=id)
#         check=user.check_password(old_password)
#         if check==True:
#             user.set_password(new_password)
#             user.save()
#             messages.success(request, 'New password  Successfully..!!')
#             return redirect("home")
#         else:
#             messages.error(request, '**Incorrect Old Password..!!')
#         return redirect('profile')





############
def add_review(request,id):
    if request.method == 'POST':
        text = request.POST['text']
        rating = request.POST.get('rating', 5)  
        try:
            book = Books.objects.get(id=id)
            review = Review(user=request.user, book=book, text=text, rating=rating)
            review.save()
            return redirect('book_detail', id=id)
        except Books.DoesNotExist:
            return HttpResponse('Book not found', status=404)
    else:
        return HttpResponse('Method not allowed', status=405)




## Usersurveys views start 

# class Usersurveys(View):
#     def get(self, request):
#         data = SurveyResponse.objects.filter(user__is_superuser=True)
#         user = SurveyResponse.objects.filter(user=request.user)
#       
#         return render(request, 'lowafrecia/user_servays.html', {'data': data})

#     def post(self, request):
#         user = request.user

#         # Check if the user has already submitted a response for this survey
#         # existing_response = SurveyResponse.objects.filter(user=user).exists()
#         # if existing_response:
#         #     messages.error(request, 'You have already submitted a response.')
#         #     return redirect('Usersurveys')
#         for key, value in request.POST.items():
#             if key.startswith('answer_'):
#                 question_id = key.split('_')[1]
#                 question = request.POST.get(f'question_{question_id}')
#                 answer_field_name = f'answer{question_id}'
#                 answer = value

#                 # Create SurveyResponse object for each question
#                 data = SurveyResponse.objects.create(
#                     user=user,
#                     question=question,
#                     **{answer_field_name: answer},
#                 )

#         messages.success(request, 'Response saved successfully')
#         return redirect('Customer_dashboard')


class Usersurveys(View):
    def get(self, request):
        data = SurveyResponse.objects.filter(user__is_superuser=True)
        user = SurveyResponse.objects.filter(user=request.user)
        return render(request, 'lowafrecia/user_servays.html', {'data': data,'active17':'active20'})

    def post(self, request):
        user = request.user

        # Check if the user has already submitted a response for this survey
        # existing_response = SurveyResponse.objects.filter(user=user).exists()
        # if existing_response:
        #     messages.error(request, 'You have already submitted a response.')
        #     return redirect('Usersurveys')

        answers = {}  # Dictionary to store answers

        for key, value in request.POST.items():
            if key.startswith('answer_'):
                question_id = key.split('_')[1]
                answer_field_name = f'answer{question_id}'
                answers[answer_field_name] = value

        # Create SurveyResponse object with the collected answers
        data = SurveyResponse.objects.create(
            user=user,
            question=request.POST.get('question'),  # Adjust this based on your actual form structure
            **answers,
        )

        messages.success(request, 'Response saved successfully')
        return redirect('Customer_dashboard')
    
    
    
    

########################## enduser code start here 
class NormalUserRegister(View):
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        institute =request.POST.get('institute')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email id  Already Exist...? Use Diffrent Email id to Create Account.')
        else:
            user = User.objects.create_user(institute=institute, first_name=first_name,last_name=last_name, email=email, phone_number=phone_number,password=password)
            user.is_enduser=True
            user.save()
            activation_link = request.build_absolute_uri(reverse('activate_account', args=[user.id]))
            subject = 'Activate Your Account'
            message = f'Hi {user.first_name},\n\nPlease click on the following link to activate your account:\n\n{activation_link}'
            from_email = 'indy@optimuse-solutions.com'  
            send_mail(subject, message, from_email, [user.email])
            messages.success(request, 'Student registration successfully. Please check your email to activate your account.')
        return redirect('home')



class ActivateAccountView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('enduser-login') 



class NormalUserDashboard(View):
    def get(self, request):
        user = request.user
        fav_count = Favorite.objects.filter(user=request.user, ).count()
        unique_book_visit_count = BookVisit.objects.filter(user=request.user, institute_name=request.user.institute).values('user', 'books').distinct().count()
        total_time = 0
        book_visits = BookVisit.objects.filter(user=request.user)
        total_time_per_book = defaultdict(int)
        for visit in book_visits:
            # Calculate time difference if start_time and end_time are present
            if visit.start_time and visit.end_time:
                time_difference = visit.end_time - visit.start_time
                total_time_per_book[visit.books_id] += time_difference.total_seconds()

        formatted_times_per_book = {}
        # Convert total_time to hours and minutes for each book
        for book_id, total_time in total_time_per_book.items():
            hours, remainder = divmod(total_time, 3600)
            minutes = remainder / 60

            # Format the time for each book
            if hours >= 1:
                formatted_time = "{:.0f} hours {:.0f} minutes".format(hours, minutes)
            else:
                formatted_time = "{:.2f} minutes".format(minutes).rstrip('0').rstrip('.')

            formatted_times_per_book[book_id] = formatted_time

        total_book = len(formatted_times_per_book)

        # Check if total_book is greater than zero before calculating avg_reading_time
        if total_book > 0:
            total_minutes = sum(float(duration.split()[0]) for duration in formatted_times_per_book.values())
            avg_reading_time = total_minutes / total_book

            hours, minutes = divmod(avg_reading_time, 60)
            if hours >= 1:
                formatted_time = "{:.0f} hours {:.0f} minutes".format(hours, minutes)
            else:
                formatted_time = "{:.2f} minutes".format(minutes).rstrip('0').rstrip('.')
        else:
            formatted_time = 0
        return render(request,'NormalUser/Dashboard.html',{'book_visit_count': unique_book_visit_count, 'active1': 'active20', 'formatted_duration_str': formatted_time,'fav_count':fav_count})
    

class NormalUserAllBooks(View):
    def get(self, request):
        if request.user.is_authenticated:
            ebook_reader = EbookReaderBanner.objects.all()
            footer = Footer.objects.all()
            is_enduser = request.user.is_enduser
            user_ = User.objects.get(id=request.user.id)
   
            if is_enduser:
                book_list = Books.objects.all()
                st = request.GET.get('searchname')
                if st is not None:
                    book_list = book_list.filter(
                    Q(title__icontains=st) |
                    Q(author__icontains=st) |
                    Q(publication_date__icontains=st) |
                    Q(price__icontains=st) |
                    Q(category__book_category__icontains=st)
                )
                all_books = Books.objects.none()
            else:
                book_list = book_list.filter(is_active=True).order_by('-id')
                st = request.GET.get('searchname')
                if st is not None:
                    book_list = book_list.filter(
                    Q(title__icontains=st) |
                    Q(author__icontains=st) |
                    Q(publication_date__icontains=st) |
                    Q(price__icontains=st) |
                    Q(category__book_category__icontains=st)
                )

               
            book_lists = []
            completed = 'Progress'
            for book in book_list:
                if Favorite.objects.filter(fav_book=book, user=request.user).exists():
                    favorite = 1
                    
                else:
                    favorite = 0
                completed = "Progress"
                if BookVisit.objects.filter(user=request.user, books=book).exists():
                    last_visit_book = BookVisit.objects.filter(user=request.user, books=book).last()
                    
                    if last_visit_book.completed == True:
                        completed = 'Completed'
                    else:
                        completed = 'Progress'
                
                d = {
                    "id": book.id,
                    "category": book.category,
                    "title": book.title,
                    "image": book.image,
                    "favorite": favorite,
                    "readingStatus":completed
                }
                book_lists.append(d)
            return render(request, 'NormalUser/all_book.html', {
                'ebook_reader': ebook_reader,
                'footer': footer,
                'active2': 'active20',
                'all_books': book_lists,
                'book_list': book_list if is_enduser else None  # Use book_list here for students
            })
        else:
            messages.error(request, 'Login is required to access book, Please login if register account or register as new user')
            return redirect('home')


def normal_favoritelist(request):
    st = request.GET.get('searchname')
    fav_books = Favorite.objects.filter(user=request.user) 
    if st is not None:
        fav_books = fav_books.filter(
            Q(fav_book__title__icontains=st) |
            Q(fav_book__author__icontains=st) |
            Q(fav_book__publication_date__icontains=st) |
            Q(fav_book__price__icontains=st) |
            Q(fav_book__category__book_category__icontains=st)
        )
    return render(request, 'NormalUser/fav_book.html', {'fav_books': fav_books, 'active5': 'active20'})



class NormalBookDetails(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            user = request.user.institute
            footer = Footer.objects.all()
            book_category = Books.objects.values('category__book_category').annotate(book_count=models.Count('id')).order_by('-book_count')[:7]
            member = User.objects.filter(is_enduser=True, is_student=False,is_active=True, is_superuser=False, is_staff=False, is_organization=False).count()
            book_list = Books.objects.filter(id=id,is_active=True)  
            book = Books.objects.get(id=id,is_active=True)
            book.viewed_at = timezone.now()
            book.save() 
            book = Books.objects.get(id=id,is_active=True)
            add_recent_view_book = Recently_Viewed.objects.create(user=request.user, book=book)
            completed = False
            if BookVisit.objects.filter(user=request.user, books=book).exists():
                last_visit_book = BookVisit.objects.filter(user=request.user, books=book).last()
                
                if last_visit_book.completed == True:
                    completed = True
                else:
                    completed = False
            book_visit = ''
            if request.user.is_enduser == True:
                book_visit = BookVisit.objects.create(user=request.user, books=book, completed=completed, institute_name=request.user.institute)
            return render(request, 'NormalUser/BookDetails.html', { 'book_obj':book,'footer': footer,'book_list': book_list,'member':member, "id":id, "book_visit":book_visit,'book_category':book_category})
        else:
            messages.error(request, 'Login is required to access book, Please login if register account or register as new user')
            return redirect('home')


def normalrecentlyView(request):
    user = request.user
    st = request.GET.get('searchname')
    recently_viewed = Recently_Viewed.objects.filter(user=user).order_by('-id')

    # Apply search filter if 'st' is not None
    if st:
        recently_viewed = recently_viewed.filter(
            Q(book__title__icontains=st) |
            Q(book__author__icontains=st) |
            Q(book__publication_date__icontains=st) |
            Q(book__price__icontains=st) |
            Q(book__category__book_category__icontains=st)
        )

    unique_book_ids = []
    unique_recently_viewed = []
    for rv in recently_viewed:
        if rv.book_id not in unique_book_ids:
            unique_book_ids.append(rv.book_id)  
            unique_recently_viewed.append(rv)
    unique_recently_viewed = unique_recently_viewed[:3]
    recently_viewed = Recently_Viewed.objects.values('book').annotate(view_count=Count('book')).order_by('-view_count')[:3]

    # Get the top 3 recently viewed books
    top_books = Books.objects.filter(id__in=[item['book'] for item in recently_viewed])
    return render(request, 'NormalUser/RecentlyView.html', {'recently_viewed': unique_recently_viewed, 'active4': 'active20'})



class NormalUserMostPopularBooks(View):
    def get(self, request):
        institute_name = getattr(request.user, 'institute', 'guest')  # Use getattr to provide a default value
        book_visits = BookVisit.objects.filter(institute_name=institute_name)
        total_time_per_book = defaultdict(int)
        visits_per_book = defaultdict(int)
        num_books_to_process = 5  # Set the number of books you want to process

        for visit in book_visits:
            user_visit = BookVisit.objects.filter(books=visit.books, institute_name=request.user.institute).count()
            visits_per_book[visit.books_id] += 1  # Increment the visit count for the book

            if visit.start_time and visit.end_time:
                time_difference = visit.end_time - visit.start_time
                total_time_per_book[visit.books_id] += time_difference.total_seconds()

        # Sort books based on total time spent in descending order
        sorted_data_desc = sorted(total_time_per_book.items(), key=lambda item: item[1], reverse=True)[:num_books_to_process]
        
        # Create a dictionary to store formatted times, visit count, and book objects for each book
        formatted_data_per_book = {}
        for book_id, total_time in sorted_data_desc:
            hours, remainder = divmod(total_time, 3600)
            minutes = remainder / 60
            if hours >= 1:
                formatted_time = "{:.0f} h {:.0f} min".format(hours, minutes)
            else:
                formatted_time = "{:.0f} min".format(minutes)

            try:
                book_object = Books.objects.get(id=book_id)
            except Books.DoesNotExist:
                book_object = None

            formatted_data_per_book[book_id] = {
                'formatted_time': formatted_time,
                'visit_count': visits_per_book[book_id],  
                'book_object': book_object,
            }

        context = {'formatted_data_per_book': formatted_data_per_book,'active3':'active20'}
        return render(request, 'NormalUser/MostPopularBook.html', context)
    


class NormalUsersurveys(View):
    def get(self, request):
        data = SurveyResponse.objects.filter(user__is_superuser=True)
        user = SurveyResponse.objects.filter(user=request.user)
        return render(request, 'NormalUser/Servey.html', {'data': data,'active6':'active20'})

    def post(self, request):
        user = request.user
        answers = {} 
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                question_id = key.split('_')[1]
                answer_field_name = f'answer{question_id}'
                answers[answer_field_name] = value
        data = SurveyResponse.objects.create(
            user=user,
            question=request.POST.get('question'),  
            **answers,
        )
        messages.success(request, 'Response saved successfully')
        return redirect('Customer_dashboard')
    


class NormalUserBookVisistList(View):
    def get(self,request):
        recently_viewed = Recently_Viewed.objects.filter(user=request.user).order_by('-id')
        unique_book_ids = []
        unique_recently_viewed = []
        for rv in recently_viewed:
            if rv.book_id not in unique_book_ids:
                unique_book_ids.append(rv.book_id)
                unique_recently_viewed.append(rv)
        unique_recently_viewed = unique_recently_viewed[:4]
        return render(request,'NormalUser/BookVisitsList.html',{'book_visit_list':unique_recently_viewed})
    


class NormalUserAverageTimeSpent(View):
    def get(self, request):
        # Get all book visits for the user
        book_visits = BookVisit.objects.filter(user=request.user)
        total_time_per_book = defaultdict(int)
        for visit in book_visits:
            # Calculate time difference if start_time and end_time are present
            if visit.start_time and visit.end_time:
                time_difference = visit.end_time - visit.start_time
                total_time_per_book[visit.books_id] += time_difference.total_seconds()

        # Create a dictionary to store formatted times and book objects for each book
        formatted_data_per_book = {}

        # Convert total_time to hours and minutes for each book
        for book_id, total_time in total_time_per_book.items():
            hours, remainder = divmod(total_time, 3600)
            minutes = remainder / 60

            # Format the time for each book
            if hours >= 1:
                formatted_time = "{:.0f} h {:.0f} min".format(hours, minutes)
            else:
                formatted_time = "{:.0f} min".format(minutes)

            # Retrieve the Book object
            book_object = Books.objects.get(id=book_id)
            # Add data to the dictionary
            formatted_data_per_book[book_id] = {
                'formatted_time': formatted_time,
                'book_object': book_object,
            }
       
        return render(request,'NormalUser/AverageTimeSpent.html', {'formatted_data_per_book': formatted_data_per_book,})
           