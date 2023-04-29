from django.contrib import admin

# Register your models here.
from .models import Teams,Matches,Liga
admin.site.register(Teams)
admin.site.register(Matches)
admin.site.register(Liga)