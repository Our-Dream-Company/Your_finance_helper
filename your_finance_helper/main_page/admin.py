from django.contrib import admin
from .models import Section
from .models import Category
from .models import NameOperation
from .models import GeneralTable

admin.site.register(Section)
admin.site.register(Category)
admin.site.register(NameOperation)
admin.site.register(GeneralTable)
