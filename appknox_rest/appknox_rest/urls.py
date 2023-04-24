from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"users", views.UserViewSet)
router.register(r"questions", views.QuestionViewSet)
router.register(r"answers", views.AnswerViewSet)
router.register(r"comments", views.CommentViewSet)
router.register(r"votes", views.VoteViewSet)
urlpatterns = [path("admin/", admin.site.urls), path("", include(router.urls))]
