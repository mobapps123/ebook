from ebook_apps.models import *
from django.contrib.auth import authenticate,logout, login as dj_login




def permission(request):
    if request.user.is_authenticated:
        # print('avc')
        email = request.user
        # print(username)
        staff_menu = Staffmenu.objects.filter(user=email).first()          
        # print(staff_menu,"veena") 
        is_staff = email.is_staff
        selected_permissions = []
        if staff_menu and staff_menu.dashboard == '1':
            selected_permissions.append('dashboard')
            
        if staff_menu and staff_menu.details_book == '1':
            selected_permissions.append('details_book')

        if staff_menu and staff_menu.user_details == '1':
            selected_permissions.append('user_details')

        if staff_menu and staff_menu.manage_home == '1':
            selected_permissions.append('manage_home')

        if staff_menu and staff_menu.manage_contact == '1':
            selected_permissions.append('manage_contact')

        if staff_menu and staff_menu.manage_category == '1':
            selected_permissions.append('manage_category')

        if staff_menu and staff_menu.manage_collection == '1':
            selected_permissions.append('manage_collection')

        if staff_menu and staff_menu.digital_publishing == '1':
            selected_permissions.append('digital_publishing')

        if staff_menu and staff_menu.ebook_store == '1':
            selected_permissions.append('ebook_store')

        if staff_menu and staff_menu.ebook_reader == '1':
            selected_permissions.append('ebook_reader')

        if staff_menu and staff_menu.indybot == '1':
            selected_permissions.append('indybot')

        if staff_menu and staff_menu.notifications == '1':
            selected_permissions.append('notifications')

        if staff_menu and staff_menu.manage_cms == '1':
            selected_permissions.append('manage_cms')
        
        if staff_menu and staff_menu.manage_staff == '1':
            selected_permissions.append('manage_staff')
        
        if staff_menu and staff_menu.manage_blogs == '1':
            selected_permissions.append('manage_blogs')

        context = {
            'is_staff': is_staff,
            'selected_permissions': selected_permissions
        }
        print(selected_permissions)
        print(context)
        return {"context":context}
    else:
        context="abc"
        return {"context":context}
