from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
#from commercialoperator import views
#from commercialoperator.admin import commercialoperator_admin_site
#from commercialoperator.components.proposals import views as proposal_views
#from commercialoperator.components.organisations import views as organisation_views
#from commercialoperator.components.bookings import views as booking_views
#
#from commercialoperator.components.users import api as users_api
#from commercialoperator.components.organisations import api as org_api
#from commercialoperator.components.main import api as main_api
#from commercialoperator.components.bookings import api as booking_api

from ledger.urls import urlpatterns as ledger_patterns

# API patterns
router = routers.DefaultRouter()
#router.register(r'organisations',org_api.OrganisationViewSet)
#router.register(r'proposal',proposal_api.ProposalViewSet)
#router.register(r'proposal_park',proposal_api.ProposalParkViewSet)
#router.register(r'proposal_submit',proposal_api.ProposalSubmitViewSet)
#router.register(r'proposal_paginated',proposal_api.ProposalPaginatedViewSet)
#router.register(r'approval_paginated',approval_api.ApprovalPaginatedViewSet)
#router.register(r'booking_paginated',booking_api.BookingPaginatedViewSet)

api_patterns = [
    #url(r'^api/profile$', users_api.GetProfile.as_view(), name='get-profile'),
    #url(r'^api/department_users$', users_api.DepartmentUserList.as_view(), name='department-users-list'),
    #url(r'^api/filtered_users$', users_api.UserListFilterView.as_view(), name='filtered_users'),
    #url(r'^api/filtered_organisations$', org_api.OrganisationListFilterView.as_view(), name='filtered_organisations'),

]

# URL Patterns
urlpatterns = [
    #url(r'^admin/', include(commercialoperator_admin_site.urls)),
    #url(r'^admin/', commercialoperator_admin_site.urls),
    url(r'^ledger/admin/', admin.site.urls, name='ledger_admin'),
    #url(r'', include(api_patterns)),
    #url(r'^$', views.CommercialOperatorRoutingView.as_view(), name='ds_home'),
    #url(r'^contact/', views.CommercialOperatorContactView.as_view(), name='ds_contact'),
    #url(r'^further_info/', views.CommercialOperatorFurtherInformationView.as_view(), name='ds_further_info'),

] + ledger_patterns

if settings.DEBUG:  # Serve media locally in development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
