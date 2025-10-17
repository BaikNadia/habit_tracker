from django.urls import path
from .views import MyHabitsList, PublicHabitsList, HabitDetail

urlpatterns = [
    path("my/", MyHabitsList.as_view(), name="my-habits"),
    path("public/", PublicHabitsList.as_view(), name="public-habits"),
    path("<int:pk>/", HabitDetail.as_view(), name="habit-detail"),
]
