from django.urls import path , include
from . import views
urlpatterns = [
	path('', views.index , name = 'index'),
	path('delete/<city_id>/', views.delete , name = 'delete'),
    # path('admin/', admin.site.urls),
]
