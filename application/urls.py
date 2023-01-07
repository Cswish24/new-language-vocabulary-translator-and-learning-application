from django.urls import path
from application.translator_api import translate_en
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name=("home-page")),
    path("sign-up", views.sign_up, name="sign-up"),
    path("en-es", views.EnTranslateView.as_view(), name=("en-translator")),
    path("es-en", views.EsTranslateView.as_view(), name=("es-translator")),
    path("manual", views.ManualTranslateView.as_view(), name=("manual-translator")),
    path("personal_or_total_database", views.PersonalOrTotalDatabaseSelectionView.as_view(), name=("personal_or_total_database")),
    path("databases/<str:personal>", views.DatabaseSelectionView.as_view(), name=("databases")),
    path("database/<str:category>/<str:personal>", views.DatabaseView.as_view(), name=("database")),
    path("database_update/<int:id>/<str:personal>", views.ManualUpdateView.as_view(), name=("update")),
    path("database_delete/<int:id>/<str:category>/<str:personal>", views.delete_word, name=("delete")),
    path("which-quizzes", views.WhichQuizzesView.as_view(), name=("which-quizzes")),
    path("quiz-home/<str:personal>", views.QuizHomeView.as_view(), name=("quiz-home")),
    path("quiz-stat-home", views.QuizStatHomeView.as_view(), name=("quiz-stat-home")),
    path("quiz-game/<str:category>/<int:iterations>/<str:personal>/<int:id>/<int:correct>", views.QuizView.as_view(), name=("quiz")),
    path("quiz-stat-view/<str:category>", views.StatView.as_view(), name=("stat-view")),
    path("success", views.SuccessView.as_view(), name=("success")),
    path("exceeded", views.ExceededView.as_view(), name=("exceeded")),
]