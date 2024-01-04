from import_export import resources
from .models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = False
        name = "Export/Import All Fiels Of Organization"



