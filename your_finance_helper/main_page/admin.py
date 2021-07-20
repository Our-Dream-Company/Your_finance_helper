from django.contrib import admin
from .models import Section, Category, NameOperation, GeneralTable


admin.site.register(Section)
admin.site.register(Category)
admin.site.register(NameOperation)
admin.site.register(GeneralTable)
