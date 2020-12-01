from django.contrib import admin
from feewaiver.models import *

@admin.register(FeeWaiver)
class FeeWaiverAdmin(admin.ModelAdmin):
    pass
    #list_display = ['name', 'description', 'version']

@admin.register(ContactDetails)
class ContactDetailsAdmin(admin.ModelAdmin):
    pass

@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    pass

@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    pass

