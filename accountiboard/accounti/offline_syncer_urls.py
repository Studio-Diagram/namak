from django.urls import path
from accounti.views import OfflineAPIs

urlpatterns = [
    path('create_member/', OfflineAPIs.create_member),
]


