from django.contrib import admin
from feewaiver.models import *
from feewaiver.main_models import GlobalSettings

@admin.register(FeeWaiver)
class FeeWaiverAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactDetails)
class ContactDetailsAdmin(admin.ModelAdmin):
    pass


@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    pass


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    pass


#@admin.register(CampGround)
#class CampGroundAdmin(admin.ModelAdmin):
 #   pass


@admin.register(AssessorsGroup)
class AssessorsGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    actions = None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = EmailUser.objects.filter(is_staff=True)
        return super(AssessorsGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return True if AssessorsGroup.objects.count() == 0 else False

    def has_delete_permission(self, request, obj=None):
        return False 

@admin.register(ApproversGroup)
class ApproversGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    actions = None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = EmailUser.objects.filter(is_staff=True)
        return super(ApproversGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return True if ApproversGroup.objects.count() == 0 else False

    def has_delete_permission(self, request, obj=None):
        return False 


@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        if obj.key == GlobalSettings.KEY_FEEWAIVER_TEMPLATE_FILE:
            return ['key', '_file',]
        else:
            return ['key', 'value',]

    def get_readonly_fields(self, request, obj=None):
        return ['key',]

    list_display = ['key', 'value', '_file',]
    ordering = ('key',)


