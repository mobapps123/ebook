from django.urls import path
from django.views import View
from . import views

from django.contrib.auth import views as auth_views
from django.urls import path, include



urlpatterns = [

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    path('',views.login,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('Dashboard/',views.dashboard,name='dashboard'),
    path('Active-Inactive/',views.Active_inActiveUser.as_view(),name='active-inactive'),
    path('profile-update/',views.AdminUpdateprofile.as_view(),name='updateprofile'),
    path('change-password/',views.ChangePassword.as_view(),name='change-password'),
    path('add_category/',views.AddBookCategory.as_view(),name='add_category'),
    path('category_details/',views.Category_details.as_view(),name='category_details'),
    path('category_delete/<int:id>',views.Category_Delete.as_view(),name='category_delete'),
    path('category_edit/<int:id>',views.Category_Edit.as_view(),name='category_edit'),
    path('add-book/',views.Add_book.as_view(),name='add_book'),
    path('book_details/',views.Details_Book.as_view(),name='details_book'),
    path('edit_book/<int:id>',views.Edit_book.as_view(),name='edit_book'),
    path('delete_book/<int:id>',views.Delete_Book.as_view(),name='delete_book'),

    path('contact-us/',views.ContactUsView.as_view(),name='messageus'),
    path('contact_delete/<int:id>',views.ContactUs_Delete.as_view(),name='contact_delete'),

    path('add-organization/',views.Add_Organizations.as_view(),name='organization'),
    path('delete-user/<int:id>',views.Delete_User.as_view(),name='delete_user'),
    path('details-user/',views.Details_User.as_view(),name='user_details'),
    path('details-enduser/',views.Details_Enduser.as_view(),name='enduser_details'),
    path('DemoRequest/',views.Details_DemoRequest.as_view(),name='Demo_request'),

    path('DemoRequest_Delete/<int:id>',views.Deletedemorequest.as_view(),name='Demorequestdelete'),
    path('activate/<int:id>/',views.ActivateAccountView.as_view(),name='activate_account'),

    path('add_home/',views.AddHome.as_view(),name='add_home'),
    path('home_details/',views.HomeDetails.as_view(),name='home_details'),
    path('home_edit/<int:id>',views.EditHome.as_view(),name='home_edit'),
    path('home_delete/<int:id>',views.HomeDelete.as_view(),name='home_delete'),

    path('add_learn/',views.AddLearn.as_view(),name='add_Learn'),
    path('learn_details/',views.LearnDetails.as_view(),name='learn_details'),
    path('learn_edit/<int:id>',views.EditLearn.as_view(),name='learn_edit'),
    path('learn_delete/<int:id>',views.LearnDelete.as_view(),name='learn_delete'),

    path('add_overview/',views.AddOverview.as_view(),name='add_overview'),
    path('overview_details/',views.DetailsOverview.as_view(),name='overview_details'),
    path('overview_edit/<int:id>',views.EditOverview.as_view(),name='overview_edit'),
    path('overview_delete/<int:id>',views.DeleteOverview.as_view(),name='overview_delete'),

    path('active-inactive/', views.Active_inActive.as_view(), name='active_inactive'),


    path('CreateSurvey/',views.CreateSurvey.as_view(),name='CreateSurvey'),
    path('ViewServey/<int:id>',views.ViewStudentsServey.as_view(),name='ViewServey'),



    path('CustomerServeyDetail/',views.CustomerServeyDetail.as_view(),name='CustomerServeyDetail'),

    path('CustomerservayDelete/<int:id>',views.CustomerservayDelete.as_view(),name='CustomerservayDelete'),

    
   




    path('add_howdoes/',views.AddHowDoes.as_view(),name='add_howdoes'),
    path('howdoes_details/',views.Details_HowDoes.as_view(),name='howdoes_details'),
    path('howdoes_edit/<int:id>',views.EditHowDoes.as_view(),name='howdoes_edit'),
    path('howdoes_delete/<int:id>',views.DeleteHowDoes.as_view(),name='howdoes_delete'),

    path('add_ebookexp/',views.AddEbookExp.as_view(),name='add_ebookexp'),
    path('ebookexp_details/',views.Details_EbookExp.as_view(),name='ebookexp_details'),
    path('ebookexp_edit/<int:id>',views.Edit_EbookExp.as_view(),name='ebookexp_edit'),
    path('exp_delete/<int:id>',views.Delete_EbookExp.as_view(),name='exp_delete'),

    path('add_ourservice/',views.AddOurService.as_view(),name='add_ourservice'),
    path('ourservice_details/',views.Details_Service.as_view(),name='ourservice_details'),
    path('ourservice_edit/<int:id>',views.Edit_Ourservice.as_view(),name='ourservice_edit'),
    path('ourservice_delete/<int:id>',views.Delete_Service.as_view(),name='ourservice_delete'),




    path('add_ourpartner/',views.AddOur_Partner.as_view(),name='add_ourpartner'),
    path('ourpartner_details/',views.Details_OurPartner.as_view(),name='ourpartner_details'),
    path('ourpartner_edit/<int:id>',views.EditOur_Partner.as_view(),name='ourpartner_edit'),
    path('ourpartner_delete/<int:id>',views.Delete_OurPartner.as_view(),name='ourpartner_delete'),


    path('add_studio/',views.AddStudio.as_view(),name='add_studio'),
    path('studio_details/',views.Details_studio.as_view(),name='studio_details'),
    path('studio_edit/<int:id>',views.Edit_Studio.as_view(),name='studio_edit'),
    path('studio_delete/<int:id>',views.Delete_studio.as_view(),name='studio_delete'),


    path('add_footer/',views.Add_Footer.as_view(),name='add_footer'),
    path('footer_details/',views.Details_footer.as_view(),name='footer_details'),
    path('footer_edit/<int:id>',views.EditFooter.as_view(),name='footer_edit'),
    path('footer_delete/<int:id>',views.DeleteFooter.as_view(),name='footer_delete'),


    path('Add_collection/',views.AddCollection.as_view(),name='add_collection'),
    path('collection_details/',views.CollectionDetails.as_view(),name='collection_details'),
    path('collection_edit/<int:id>',views.EditCollection.as_view(),name='collection_edit'),
    path('collection_delete/<int:id>',views.CollectionDelete.as_view(),name='collection_delete'),

    path('collection_view/<int:id>',views.CollectionView.as_view(),name='collection_view'),
    path('collection_viewdelete/<int:id>',views.CollectionViewDelete.as_view(),name='collectionviewdelete'),



    path('AddContact/',views.AddContactBanner.as_view(),name='addContactusBanner'),
    path('ContactusBanner_details/',views.DetailsContactBanner.as_view(),name='ContactusBanner_details'),
    path('ContactusBanner_edit/<int:id>',views.EditContactBanner.as_view(),name='ContactusBanner_edit'),
    path('ContactusBanner_delete/<int:id>',views.DeleteContactBanner.as_view(),name='ContactusBanner_delete'),


    path('AddGetintouch/',views.AddGetInTouch.as_view(),name='addGetintouch'),
    path('Getintouch_details/',views.DetailGetInTouch.as_view(),name='Getintouch_details'),
    path('Getintouch_edit/<int:id>',views.EditGetInTouch.as_view(),name='Getintouch_edit'),
    path('Getintouch_delete/<int:id>',views.DeleteGetInTouch.as_view(),name='Getintouch_delete'),


    path('AddAboutBanner/',views.AddAboutBanner.as_view(),name='addAboutBanner'),
    path('AboutBanner_details/',views.DetailsAbout.as_view(),name='AboutBanner_details'),
    path('AboutBanner_edit/<int:id>',views.EditAboutBanner.as_view(),name='AboutBanner_edit'),
    path('AboutBanner_delete/<int:id>',views.DeleteAbout.as_view(),name='AboutBanner_delete'),


    path('Addthefoundation/',views.AddTheFoundation.as_view(),name='addthefoundation'),
    path('thefoundation_details/',views.DetailsTheFoundation.as_view(),name='thefoundation_details'),
    path('thefoundation_edit/<int:id>',views.EditTheFoundation.as_view(),name='thefoundation_edit'),
    path('thefoundation_delete/<int:id>',views.DeleteTheFoundation.as_view(),name='thefoundation_delete'),

    path('Addthebook/',views.AddTheBook.as_view(),name='addthebook'),
    path('thebook_details/',views.DetailsTheBook.as_view(),name='thebook_details'),
    path('thebook_edit/<int:id>',views.EditTheBook.as_view(),name='thebook_edit'),
    path('thebook_delete/<int:id>',views.DeleteTheBook.as_view(),name='thebook_delete'),



    path('AddBlogBanner/',views.AddBlogBanner.as_view(),name='addBlogBanner'),
    path('BlogBanner_details/',views.DetailsBlog.as_view(),name='BlogBanner_details'),
    path('BlogBanner_edit/<int:id>',views.EditBlogBanner.as_view(),name='BlogBanner_edit'),
    path('BlogBanner_delete/<int:id>',views.DeleteBlog.as_view(),name='BlogBanner_delete'),


    path('AddBlogdetail/',views.AddBlogDetails.as_view(),name='addBlogdetail'),
    path('Blogdetails_details/',views.Details_Blogs.as_view(),name='Blogdetail_details'),
    path('Blogdetails_edit/<int:id>',views.EditBlogDetail.as_view(),name='Blogdetail_edit'),
    path('Blogdetails_delete/<int:id>',views.DeleteBlogDetails.as_view(),name='Blogdetail_delete'),



    path('Add_Digital/',views.AddDigitalBanner.as_view(),name='adddigitalbanner'),
    path('DigitaBanner_details/',views.DetailsDigital.as_view(),name='digital_details'),
    path('DigitaBanner_edit/<int:id>',views.EditDigitalBanner.as_view(),name='digital_edit'),
    path('DigitaBanner_delete/<int:id>',views.DeleteDigital.as_view(),name='digital_delete'),


    path('Add_Caterto/',views.AddCatertovarious.as_view(),name='addCaterto'),
    path('Caterto_details/',views.DetailsCaterto.as_view(),name='Caterto_details'),
    path('Caterto_edit/<int:id>',views.EditCaterto.as_view(),name='Caterto_edit'),
    path('Caterto_delete/<int:id>',views.DeleteCaterto.as_view(),name='Caterto_delete'),


    path('Add_Secured/',views.AddSecured.as_view(),name='addSecured'),
    path('Secured_details/',views.DetailsSecured.as_view(),name='Secured_details'),
    path('Secured_edit/<int:id>',views.EditSecured.as_view(),name='Secured_edit'),
    path('Secured_delete/<int:id>',views.DeleteSecured.as_view(),name='Secured_delete'),

    path('Add_GetYour/',views.AddGetYour.as_view(),name='addGetYour'),
    path('GetYour_details/',views.DetailsGetYour.as_view(),name='GetYour_details'),
    path('GetYour_edit/<int:id>',views.EditGetYour.as_view(),name='GetYour_edit'),
    path('GetYour_delete/<int:id>',views.DeleteGetYour.as_view(),name='GetYour_delete'),


    path('Add_MultiDevice/',views.AddMultiDevice.as_view(),name='addMultiDevice'),
    path('MultiDevice_details/',views.DetailsMultiDevice.as_view(),name='MultiDevice_details'),
    path('MultiDevice_edit/<int:id>',views.EditMultiDevice.as_view(),name='MultiDevice_edit'),
    path('MultiDevice_delete/<int:id>',views.DeleteMultiDevice.as_view(),name='MultiDevice_delete'),


    path('Add_EasilyInter/',views.AddEasilyInter.as_view(),name='addEasilyInter'),
    path('EasilyInter_details/',views.DetailsEasilyInter.as_view(),name='EasilyInter_details'),
    path('EasilyInter_edit/<int:id>',views.EditEasilyInter.as_view(),name='EasilyInter_edit'),
    path('EasilyInter_delete/<int:id>',views.DeleteEasilyInter.as_view(),name='EasilyInter_delete'),


    path('Addbookstore/',views.AddBookStoreBanner.as_view(),name='addbookstore'),
    path('bookstore_details/',views.DetailsBookStore.as_view(),name='bookstore_details'),
    path('bookstore_edit/<int:id>',views.EditBookStoreBanner.as_view(),name='bookstore_edit'),
    path('bookstore_delete/<int:id>',views.DeleteBookStore.as_view(),name='bookstore_delete'),

    path('AddYourWebstore/',views.AddYourWebstore.as_view(),name='addYourWebstore'),
    path('YourWebstore_details/',views.DetailsYourWebstore.as_view(),name='YourWebstore_details'),
    path('YourWebstore_edit/<int:id>',views.EditYourWebstore.as_view(),name='YourWebstore_edit'),
    path('YourWebstore_delete/<int:id>',views.DeleteYourWebstore.as_view(),name='YourWebstore_delete'),


    path('AddEasyIntegration/',views.AddEasyIntegration.as_view(),name='addEasyIntegration'),
    path('EasyIntegration_details/',views.DetailsEasyIntegration.as_view(),name='EasyIntegration_details'),
    path('EasyIntegration_edit/<int:id>',views.EditEasyIntegration.as_view(),name='EasyIntegration_edit'),
    path('EasyIntegration_delete/<int:id>',views.DeleteEasyIntegration.as_view(),name='EasyIntegration_delete'),


    path('AddSocialNetwork/',views.AddSocialNetwork.as_view(),name='addSocialNetwork'),
    path('SocialNetwork_details/',views.DetailsSocialNetwork.as_view(),name='SocialNetwork_details'),
    path('SocialNetwork_edit/<int:id>',views.EditSocialNetwork.as_view(),name='SocialNetwork_edit'),
    path('SocialNetwork_delete/<int:id>',views.DeleteSocialNetwork.as_view(),name='SocialNetwork_delete'),



    path('AddFullyResponsive/',views.AddFullyResponsive.as_view(),name='addFullyResponsive'),
    path('FullyResponsive_details/',views.DetailsFullyResponsive.as_view(),name='FullyResponsive_details'),
    path('FullyResponsive_edit/<int:id>',views.EditFullyResponsive.as_view(),name='FullyResponsive_edit'),
    path('FullyResponsive_delete/<int:id>',views.DeleteFullyResponsive.as_view(),name='FullyResponsive_delete'),



    path('AddTermCondition/',views.AddTermCondition.as_view(),name='addTermCondition'),
    path('TermCondition_details/',views.DetailsTermCondition.as_view(),name='TermCondition_details'),
    path('TermCondition_edit/<int:id>',views.EditTermCondition.as_view(),name='TermCondition_edit'),
    path('TermCondition_delete/<int:id>',views.DeleteTermCondition.as_view(),name='TermCondition_delete'),


    path('AddPrivacy/',views.AddPrivacy.as_view(),name='addPrivacy'),
    path('Privacy_details/',views.DetailsPrivacy.as_view(),name='Privacy_details'),
    path('Privacy_edit/<int:id>',views.EditPrivacy.as_view(),name='Privacy_edit'),
    path('Privacy_delete/<int:id>',views.DeletePrivacy.as_view(),name='Privacy_delete'),


    path('AddFaq/',views.AddFaq.as_view(),name='addFaq'),
    path('Faq_details/',views.DetailsFaq.as_view(),name='Faq_details'),
    path('Faq_edit/<int:id>',views.EditFaq.as_view(),name='Faq_edit'),
    path('Faq_delete/<int:id>',views.DeleteFaq.as_view(),name='Faq_delete'),


    path('Add_ebookreader/',views.Addebookreader.as_view(),name='add_ebookreader'),
    path('ebookreader_details/',views.Detailsebookreader.as_view(),name='ebookreader_details'),
    path('ebookreader_edit/<int:id>',views.Editebookreader.as_view(),name='ebookreader_edit'),
    path('ebookreader_delete/<int:id>',views.Deleteebookreader.as_view(),name='ebookreader_delete'),

    path('Add_indybotbanner/',views.AddIndybotBanner.as_view(),name='add_indybot'),
    path('indybotbanner_details/',views.DetailsIndybotBanner.as_view(),name='indybot_details'),
    path('indybotbanner_edit/<int:id>',views.EditIndybotBanner.as_view(),name='indybot_edit'),
    path('indybotbanner_delete/<int:id>',views.DeleteIndybotBanner.as_view(),name='indybot_delete'),

    path('Add_useprimary/',views.AddUseprimary.as_view(),name='add_useprimary'),
    path('useprimary_details/',views.DetailsUseprimary.as_view(),name='useprimary_details'),
    path('useprimary_edit/<int:id>',views.EditUseprimary.as_view(),name='useprimary_edit'),
    path('useprimary_delete/<int:id>',views.DeleteUseprimary.as_view(),name='useprimary_delete'),

    path('Add_indybotrespon/',views.AddIndybotRespon.as_view(),name='add_indyrespo'),
    path('indybot_details/',views.DetailsIndybotRespon.as_view(),name='indyrespo_details'),
    path('indybotrespon_edit/<int:id>',views.EditIndybotRespon.as_view(),name='indyrespo_edit'),
    path('indybotrespon_delete/<int:id>',views.DeleteIndybotRespon.as_view(),name='indyrespo_delete'),


    path('Add_Readbook/',views.AddReadBook.as_view(),name='add_Readbook'),
    path('Readbook_details/',views.DetailsReadBook.as_view(),name='Readbook_details'),
    path('Readbook_edit/<int:id>',views.EditReadBook.as_view(),name='Readbook_edit'),
    path('Readbook_delete/<int:id>',views.DeleteReadBook.as_view(),name='Readbook_delete'),


    path('Demo_details/',views.RequestAdemoDetails.as_view(),name='Demo_details'),
    path('Demo_delete/<int:id>',views.RequestDemoDelete.as_view(),name='Demo_delete'),
    path('Add_notification/',views.AddNotification.as_view(),name='addnotification'),
    path('single_notification/<int:id>',views.SendNotificationSingle.as_view(),name='singlenotification'),

    path('details_notification/',views.DetailNotification.as_view(),name='detailsnotification'),
    path('delete_notification/<int:id>',views.DeleteNotification.as_view(),name='deletenotification'),

    path("staff-login/",views.staff_login,name='stafflogin'),
    path('add_staff/',views.AddStaff.as_view(),name='addstaff'),
    path('details_staff/',views.DetailsStaff.as_view(),name='details_staff'),
    path('edit_staff/<int:id>',views.edit_staff.as_view(),name='edit_staff'),
    path('Staff-Active-Inactive/',views.Active_inActiveStaff.as_view(),name='ActiveInactive'),


    path('profile-view/<int:id>',views.ProfileView.as_view(),name='profile_view'),
    path('book_invitation/',views.BookInvitationSend.as_view(),name='sendbook_invitation'),
    path('book_invitation_details/',views.BookInvitationDetails.as_view(),name='book_invitation'),
    path('invitation_delete/<int:id>',views.BookInvitationDelete.as_view(),name='invitation_delete'),





############# corporate all urls start here..
    path('Corporate-Dashboard/',views.OrganizationsDashboard.as_view(),name='Dashboardorgani'),
    path('Create_Corporate/',views.CreateCorporate.as_view(),name='Create_organizations'),
    path('Details_Corporate/',views.DetailsCorporate.as_view(),name='Detail_organizations'),
    path('delete_Corporate/<int:id>',views.DeleteCorporate.as_view(),name='Delete_organizations'),
    path('delete-staff/<int:id>',views.DeleteStaff.as_view(),name='delete_staff'),
    path('edit_Corporate/<int:id>',views.EditCorporate.as_view(),name='edit_oganization'),
    path('books-stats/', views.BooksStats.as_view(), name="BooksStats"),
    path('Book_Details/<int:id>',views.BookDetails.as_view(),name='CorporateBookDetail'),
    
    path('top-students-lists/', views.TopStudents.as_view(), name='TopStudent'),


    path('profile_updated/',views.CorporateUpdateprofile.as_view(),name='corporate_profile'),

    path('OrganizationChangePassword/',views.OrganizationChangePassword.as_view(),name='change_password'),


    path('Students_create/',views.StudentsCreateXLSX.as_view(),name='students_create'),
    path('Students-Details/',views.StudentsDetails.as_view(),name='students_details'),

    path('edit_student/<int:id>',views.EditStudents.as_view(),name='edit_student'),
    path('delete_student/<int:id>',views.DeleteStudent.as_view(),name='delete-student'),


    path('StudentsListConve/',views.StudentsListConve.as_view(),name='StudentsListConve'),
    path('StudentsList/<int:id>',views.DeleteStudentListConve.as_view(),name='StudentsListDelete'),
    


    path('ActiveUserList/',views.ActiveUserList.as_view(),name='ActiveUserList'),
    path('ActiveUserDelete/<int:id>',views.ActiveUserDelete.as_view(),name='ActiveUserDelete'),


    path('student/',views.StudentCreate.as_view(),name='students'),

    # path('orga_xlsx/',views.OrganizationXLSXView.as_view(),name='organization-xlsx'),
    path('students-upload/',views.StudentsUpload.as_view(),name='students_upload'),


    # path('create_collection/',views.CorporateAddCollection.as_view(),name='createcollectioncorp'),
    
    # path('Corporate_CollectionList/',views.CorporateCollectionList.as_view(),name='listcollectioncorp'),

    # path('Corporate_CollectionView/<int:id>',views.CorporateCollectionView.as_view(),name='viewcollectioncorp'),

    # path('Corporate_CollectionView_delete/<int:id>',views.CorporateCollectionViewDelete.as_view(),name='viewcollectioncorpdelete'),






    path('CorporateAllBooks/',views.CorporateAllBooks.as_view(),name='CorporateAllBooks'),
    path('CorporateBookList/',views.CorporateLibrary.as_view(),name='CorporateBookList'),
    
    path('most-populoar-books/', views.MostPopularCorporateBookList.as_view(), name="MostPopularBooks"),
    path('least-popular-books', views.LeastPopularCorporateBookList.as_view(),  name="LeastPopularBooks"),
    path('average-time-reading-books/', views.AverageTimeReadingBooks.as_view(), name="AverageTimeReadings"),
    path('students_registration/<int:id>',views.StudentsRegister.as_view(),name='students_registration'),

    path('ChangePassword/<int:id>',views.UserChangePassword.as_view(),name='ChangePassword'),
    path('BookAssign/<int:id>',views.BookAssign.as_view(),name='BookAssign'),
    path('students_login/',views.students_login,name='students_login'),
    path('UserservayDetails/',views.UserservayDetails.as_view(),name='UserservayDetails'),
    path('Userservaydelete/<int:id>',views.UserservayDelete.as_view(),name='userservaydelete'),
    path('DeleteMultipleBooks/',views.DeleteMultipleBooks.as_view(),name='Delete_multi_book'),
    path('DeleteMultipleUser/',views.DeleteMultipleUser.as_view(),name='delete_multiple_users'),



    # path('SendInvitationView/',views.SendInvitationView.as_view(),name='SendInvitationView'),

    path('manage_home/',views.home,name='manage_home'),
    path('manage_blogs/',views.blogs,name='blogs'),
    path('digital_publishing/',views.digital_publishing,name='digital_publishing'),
    path('ebook_store/',views.ebook_store,name='ebook_store'),
    path('manage_indybot/',views.indybot,name='manage_indybot'),
    path('manage_contactus/',views.contactus,name='contactus'),
    path('survey/',views.survey,name='survey'),








]