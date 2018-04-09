from django.contrib import admin
from blogApp.models import Article,Category

# Register your models here.
admin.site.register([Article,Category])
