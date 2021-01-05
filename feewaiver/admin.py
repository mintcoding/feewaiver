from django.contrib import admin
from feewaiver.models import *
from feewaiver.main_models import GlobalSettings

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


#@admin.register(CampGround)
#class CampGroundAdmin(admin.ModelAdmin):
 #   pass


@admin.register(AssessorsGroup)
class AssessorsGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    #exclude = ('site',)
    actions = None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            #kwargs["queryset"] = EmailUser.objects.filter(email__icontains='@dbca.wa.gov.au')
            kwargs["queryset"] = EmailUser.objects.filter(is_staff=True)
        return super(AssessorsGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return True if AssessorsGroup.objects.count() == 0 else False

    def has_delete_permission(self, request, obj=None):
        return False 

@admin.register(ApproversGroup)
class ApproversGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    #exclude = ('site',)
    actions = None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            #kwargs["queryset"] = EmailUser.objects.filter(email__icontains='@dbca.wa.gov.au')
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

    #def get_form(self, request, obj=None, **kwargs):
    #    form = super(GlobalSettingsAdmin, self).get_form(request, obj, **kwargs)
    #    if obj.key == GlobalSettings.KEY_APIARY_SITES_LIST_TOKEN:
    #        link_to = '/api/apiary_site/export/?' + ApiaryGlobalSettings.KEY_APIARY_SITES_LIST_TOKEN + '=' + obj.value
    #        http_host = request.META['HTTP_HOST']
    #        display_link_to = http_host + link_to
    #        form.base_fields['value'].help_text = '<a href="' + link_to + '">' + display_link_to + '</a>'
    #    return form

    list_display = ['key', 'value', '_file',]
    ordering = ('key',)


