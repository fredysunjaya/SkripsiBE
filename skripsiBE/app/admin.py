from django.contrib import admin
from .models.users import *
from .models.roles import *
from .models.work_types import *
from .models.groups import *
from .models.user_groups import *

# Register your models here.
admin.site.register(User)