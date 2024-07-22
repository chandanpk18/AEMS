from django.contrib import admin
from .models import Equipment,HelpRequest,Booking

#Register your models here.

class HelpAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('email',)
    list_filter = ('status',)


#registration
admin.site.register(Equipment)
admin.site.register(HelpRequest,HelpAdmin)
admin.site.register(Booking)