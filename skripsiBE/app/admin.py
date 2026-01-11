from django.contrib import admin
from .models.approval_requests import *
from .models.attendance_types import *
from .models.groups import *
from .models.invitation_requests import *
from .models.roles import *
from .models.user_groups import *
from .models.user_logs import *
from .models.users import *
from .models.working_hours import *

# Register your models here.
admin.site.register(User)