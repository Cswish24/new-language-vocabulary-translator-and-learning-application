from django.db import connection
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from .models import UsersWords, Words
from .forms import EnWordForm,EsWordForm, ManualWordForm, RegisterForm
from .translator_api import translate_en, translate_es
from django.db.models import Avg, Max, Min, Count, Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user
from django.db.utils import ProgrammingError



# Create your views here.
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class HomeView(TemplateView):
    template_name = "application/home.html"



def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home-page'))
    else: 
        form = RegisterForm()
    
    return render(request, 'registration/sign-up.html', {"form": form})

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EnTranslateView(View):
    def get(self, request):
        context = {
            "word_form": EnWordForm()
        }
        return render(request, "application/en-translator.html", context)

    def post(self, request):
        word_form = EnWordForm(request.POST)
        if word_form.is_valid():
            word = word_form.save(commit=False)
            with connection.cursor() as cursor:
                cursor.execute('SELECT DISTINCT category FROM application_words')
                rows = cursor.fetchall()
            categories = [category[0] for category in rows]

            for category in categories:
                if word.category == category:
                    existing_words = Words.objects.filter(category=category)
                    for existing_word in existing_words:
                        if existing_word.english_word == word.english_word:
                            existing_word.user.add(request.user)
                            return HttpResponseRedirect(reverse("en-translator"))
            word.spanish_word = translate_en(word.english_word)
            word.save()
            word.user.add(request.user)
            return HttpResponseRedirect(reverse("en-translator"))

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EsTranslateView(View):
    def get(self, request):
        context = {
            "word_form": EsWordForm()
        }
        return render(request, "application/es-translator.html", context)

    def post(self, request):
        word_form = EsWordForm(request.POST)
        if word_form.is_valid():
            word = word_form.save(commit=False)
            with connection.cursor() as cursor:
                cursor.execute('SELECT DISTINCT category FROM application_words')
                rows = cursor.fetchall()
            categories = [category[0] for category in rows]
            print(categories)
            for category in categories:
                if word.category == category:
                    existing_words = Words.objects.filter(category=category)
                    for existing_word in existing_words:
                        if existing_word.spanish_word == word.spanish_word:
                            existing_word.user.add(request.user)
                            return HttpResponseRedirect(reverse("es-translator"))

            word.english_word = translate_es(word.spanish_word)
            word.save()
            word.user.add(request.user)
            return HttpResponseRedirect(reverse("es-translator"))


            
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ManualTranslateView(View):
    def get(self, request):
        context = {
            "word_form": ManualWordForm()
        }
        return render(request, "application/manual-translator.html", context)

    def post(self, request):
        word_form = ManualWordForm(request.POST)
        if word_form.is_valid():
            word = word_form.save(commit=False)
            with connection.cursor() as cursor:
                cursor.execute('SELECT DISTINCT category FROM application_words')
                rows = cursor.fetchall()
            categories = [category[0] for category in rows]
            print(categories)
            for category in categories:
                if word.category == category:
                    existing_words = Words.objects.filter(category=category)
                    for existing_word in existing_words:
                        if existing_word.spanish_word == word.spanish_word and existing_word.english_word == word.english_word:
                            existing_word.user.add(request.user)
                            return HttpResponseRedirect(reverse("manual-translator"))
            word.save()
            word.user.add(request.user)
            return HttpResponseRedirect(reverse("manual-translator"))



@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PersonalOrTotalDatabaseSelectionView(View):
    def get(self, request):
        return render(request, 'application/personal_or_total_database.html')

            
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DatabaseSelectionView(View):
    def get(self, request, personal):
        if personal == "true":
            categories = Words.objects.filter(user__id=request.user.id).distinct('category').values('category')
            categories = [category['category'] for category in categories]
            print(categories)
        else:
            with connection.cursor() as cursor:
                cursor.execute('SELECT DISTINCT category FROM application_words')
                rows = cursor.fetchall()
            categories = [category[0] for category in rows]
        context = {
            'categories': categories,
            'personal' : personal
        }
        return render(request, 'application/databases.html', context)

            
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DatabaseView(View):
    def get(self, request, category, personal):
        if personal == "true":
            words = Words.objects.filter(user__id=request.user.id).filter(category=category)
        else:
            words = Words.objects.filter(category=category)
        context = {
            "words": words,
            "category": category,
            "personal": personal
        }
        return render(request, "application/database.html", context)
        

            
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ManualUpdateView(View):
    def get(self, request, id, personal):
        context = {
            "update_word": Words.objects.filter(pk=id),
            "word_form": ManualWordForm(),
            "id": id,
            "personal": personal
        }
        return render(request, "application/update.html", context)
    
    def post(self, request, id, personal):
        word_form = ManualWordForm(request.POST)
        if word_form.is_valid():
            Words.objects.filter(pk=id).delete()
            category = str(word_form).split('category')[2].split('"')[2]
            print(category)
            word_form.save()
            return HttpResponseRedirect(reverse("database", args=[category, personal]))


@login_required(login_url='/login/')
def delete_word(request, id, category, personal):
    Words.objects.get(pk=id).user.remove(request.user)
    return HttpResponseRedirect(reverse("database", args=[category, personal]))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class WhichQuizzesView(View):
    def get(self, request):
        return render(request, 'application/which_quizzes.html')
            
            
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class QuizHomeView(View):
    def get(self, request, personal):
        if personal =="true":
            categories = Words.objects.filter(user__id=request.user.id).distinct('category').values('category')
            categories = [category['category'] for category in categories]
        else:
            with connection.cursor() as cursor:
                cursor.execute('SELECT DISTINCT category FROM application_words')
                category_rows = cursor.fetchall()
            categories = [category[0] for category in category_rows]
        context = {
            "categories": categories,
            "personal": personal
        }
        return render(request, "application/quiz-home.html", context)
            
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class QuizStatHomeView(View):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('SELECT DISTINCT category FROM application_words')
            category_rows = cursor.fetchall()
        categories = [category[0] for category in category_rows]
        context = {
            "categories": categories
        }
        print(categories)
        return render(request, "application/quiz-stat-home.html", context)

            
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class StatView(View):
    def get(self, request, category):
        if category == "worst":
            categories= Words.objects.all().distinct('category')
            print(categories)
            context = {
                "words": Words.objects.all().order_by("percentage")[:15],
                "category": category,
                "categories": False
            }
        elif category == "least":
            context = {
                "words": Words.objects.all().order_by("tries")[:15],
                "category": category,
                "categories": False
            }
        elif category == "least-category":
            words = Words.objects.values('category').annotate(sum_tries=Sum('tries'), sum_correct_guesses=Sum('correct_guesses'), sum_wrong_guesses=Sum('wrong_guesses'), avg_percentage=100*(Sum('correct_guesses')/Sum('tries'))).order_by('sum_tries')[:15]
            print(words)
            context = {
                "words": words,
                "category": category,
                "categories": True
            }
        elif category == "worst-categories":
            # with connection.cursor() as cursor:
            #     cursor.execute('SELECT category, SUM(tries), SUM(correct_guesses), SUM(wrong_guesses), SUM(correct_guesses)/SUM(tries) FROM application_words GROUP BY category ORDER BY SUM(correct_guesses)/SUM(tries)')
            #     category_rows = cursor.fetchall()
            # print(category_rows)
            words = Words.objects.values('category').annotate(sum_tries=Sum('tries'), sum_correct_guesses=Sum('correct_guesses'), sum_wrong_guesses=Sum('wrong_guesses'), avg_percentage=100*(Sum('correct_guesses')/Sum('tries'))).order_by('avg_percentage')[:15]
            print(words)
            context = {
                "words": words,
                "category": category,
                "categories": True
            }
        else:
            context = {
                "words": Words.objects.filter(category=category).order_by("percentage"),
                "category": category,
                "categories": False
            }
        print(category)
        return render(request, "application/quiz-stat-view.html", context)

            
# @method_decorator(login_required(login_url='/login/'), name='dispatch')
# class QuizView(View):
#     def get(self, request, iterations, category, id=0, correct=0):
#         if id:
#             last_word = Words.objects.get(pk=id)
#             last_word.tries += 1
#             if correct:
#                 last_word.correct_guesses += 1
#             else:
#                 last_word.wrong_guesses +=1
#             last_word.percentage = 100*(last_word.correct_guesses/last_word.tries)
#             last_word.save()
#         if category == "None":
#             words = Words.objects.all().order_by("percentage")[:15]
#             hard_quiz = True
#         else:            
#             words = Words.objects.filter(category=category).order_by("id")
#             hard_quiz = False
#         counter = iterations
#         iterations += 1
#         print(words)
#         lwords = [word for word in words]
#         try:
#             lwords[counter]
#         except IndexError:
#             return HttpResponseRedirect(reverse("success"))
#         context = {
#             "words": lwords[counter],
#             "iterations": iterations,
#             "hard_quiz": hard_quiz,
#         }
        
#         return render(request, "application/quiz-game.html", context)

def score_calculator(request, id, correct):
    last_word = Words.objects.get(pk=id)
    try:
        last_word_user = UsersWords.objects.filter(user_id_id=request.user.id).get(words_id_id=id)
    except UsersWords.DoesNotExist:
        last_word_user = None
    print(last_word_user)
    if last_word_user:
        last_word_user.tries += 1
    last_word.tries += 1
    if correct:
        last_word.correct_guesses += 1
        if last_word_user:
            last_word_user.correct_guesses += 1
    else:
        last_word.wrong_guesses +=1
        if last_word_user:
            last_word_user.wrong_guesses += 1
    last_word.percentage = 100*(last_word.correct_guesses/last_word.tries)
    last_word.save()
    if last_word_user:
        last_word_user.percentage = 100*(last_word_user.correct_guesses/last_word_user.tries)
        last_word_user.save()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class QuizView(View):
    def get(self, request, iterations, category, personal, id=0, correct=0):
        if id:
            score_calculator(request, id, correct)
        if personal == "true":
            if category == "None":
                words= Words.objects.filter(user__id=request.user.id).order_by("percentage")[:15]
                hard_quiz = True
            else:
                words = Words.objects.filter(user__id=request.user.id).filter(category=category).order_by("id")
                hard_quiz = False
        else:
            if category == "None":
                words = Words.objects.all().order_by("percentage")[:15]
                hard_quiz = True
            else:            
                words = Words.objects.filter(category=category).order_by("id")
                hard_quiz = False
        counter = iterations
        iterations += 1
        lwords = [word for word in words]
        try:
            lwords[counter]
        except IndexError:
            return HttpResponseRedirect(reverse("success"))
        context = {
            "words": lwords[counter],
            "iterations": iterations,
            "hard_quiz": hard_quiz,
            "personal": personal
        }
        
        return render(request, "application/quiz-game.html", context)

            
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SuccessView(TemplateView):
    template_name = 'success.html'