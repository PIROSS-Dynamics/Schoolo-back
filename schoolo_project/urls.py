from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    #Page admin
    path('admin/', admin.site.urls),
    #Page principal
    path('', home, name='home'),
    #Pages principales des apps
    path('lessons/', include('apps.lessons.urls')),
    path('quizz/', include('apps.quizz.urls')),
    path('users/', include('apps.users.urls')),
    path('stats/', include('apps.stats.urls')),
    path('activity/', include('apps.activity.urls')),
    #Challenges
    path('guessword/', include('apps.guessword.urls')),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
