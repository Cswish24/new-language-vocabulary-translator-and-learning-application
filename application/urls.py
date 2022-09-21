from django.urls import path
from application.translator_api import translate_en
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name=("home-page")),
    path("sign-up", views.sign_up, name="sign-up"),
    path("en-es", views.EnTranslateView.as_view(), name=("en-translator")),
    path("es-en", views.EsTranslateView.as_view(), name=("es-translator")),
    path("manual", views.ManualTranslateView.as_view(), name=("manual-translator")),
    path("databases", views.DatabaseSelectionView.as_view(), name=("databases")),
    path("database/<str:category>", views.DatabaseView.as_view(), name=("database")),
    path("database_update/<int:id>", views.ManualUpdateView.as_view(), name=("update")),
    path("database_delete/<int:id>/<str:category>", views.delete_word, name=("delete")),
    path("quiz-home", views.QuizHomeView.as_view(), name=("quiz-home")),
    path("quiz-stat-home", views.QuizStatHomeView.as_view(), name=("quiz-stat-home")),
    path("quiz-game/<str:category>/<int:iterations>/<int:id>/<int:correct>", views.QuizView.as_view(), name=("quiz")),
    path("quiz-stat-view/<str:category>", views.StatView.as_view(), name=("stat-view")),
    path("success", views.SuccessView.as_view(), name=("success"))
]