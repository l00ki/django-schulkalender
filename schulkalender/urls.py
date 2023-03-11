from django.contrib import admin
from django.contrib.auth import views as authviews
from django.urls import include, path

from . import views
from .settings import base_url

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('detail/<pk>', views.detail),
    path('filter=<query>', views.recipientfilter),
    path('own/', views.ownfilter),
    path('create/', views.EventCreate.as_view(template_name="event_create.html")),
    path('edit/<pk>', views.EventUpdate.as_view()),
    path('delete/<pk>', views.EventDelete.as_view()),
    path('login/', authviews.LoginView.as_view(template_name="login.html", next_page=f"{base_url}")),
    path('logout/', authviews.LogoutView.as_view(next_page=f"{base_url}")),
    path('pwchange/', authviews.PasswordChangeView.as_view(template_name="pwchange.html", success_url=f"{base_url}")),
    path('accounts/', include('django.contrib.auth.urls'))
]
