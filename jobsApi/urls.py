from django.urls import path
from . import views 

urlpatterns = [
    path('add-job/', views.add_job, name='add_job'),
    path('all-jobs/<str:id>/', views.get_all_posted_jobs, name='get_all_posted_jobs'),
    path('all-jobs-auth/', views.get_authenticated_all_posted_jobs, name='get_authenticated_all_posted_jobs'),
    path('get_job_detail/<str:id>/', views.get_job_detail, name='get_job_detail'),
    path('update_job/<str:id>/', views.update_job, name='update_job'),
    path('delete_job/<str:id>/', views.delete_job, name='delete_job'),
]