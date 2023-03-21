from django.contrib import admin
from .models import Accident
from .models import Emergency

class AccidentAdmin(admin.ModelAdmin):
    readonly_fields = ('created')

admin.site.register(Accident)
admin.site.register(Emergency)
# Register your models here.
