from django.urls import path, include

from django.contrib import admin
from hello import views

admin.autodiscover()

# from .hello import views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("accountsettings/", views.accountsettings_view, name="accountsettings"),
    path("submit_job/", views.submit_job, name="submit_job"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/jobs", views.jobs, name="jobs"),
    path('dashboard/detail/<int:job_id>/', views.detail, name="job_detail"),
    path("admin/", admin.site.urls),
]
