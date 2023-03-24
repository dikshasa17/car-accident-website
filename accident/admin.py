from django.contrib import admin

class AccidentAdmin(admin.ModelAdmin):
    readonly_fields = ('created')

# Register your models here.
