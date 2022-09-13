from django.db import connection
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from .models import Words
from .forms import EnWordForm,EsWordForm, ManualWordForm
from .translator_api import translate_en, translate_es


# Create your views here.


class HomeView(TemplateView):
    template_name = "application/home.html"

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
            word.spanish_word = translate_en(word.english_word)
            word.save()
            return HttpResponseRedirect(reverse("en-translator"))

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
            word.english_word = translate_es(word.spanish_word)
            word.save()
            return HttpResponseRedirect(reverse("es-translator"))


class ManualTranslateView(View):
    def get(self, request):
        context = {
            "word_form": ManualWordForm()
        }
        return render(request, "application/manual-translator.html", context)

    def post(self, request):
        word_form = ManualWordForm(request.POST)
        if word_form.is_valid():
            word_form.save()
            return HttpResponseRedirect(reverse("manual-translator"))



class DatabaseSelectionView(View):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('SELECT DISTINCT category FROM application_words')
            rows = cursor.fetchall()
        categories = [category[0] for category in rows]
        context = {
            'categories': categories
        }
        return render(request, 'application/databases.html', context)


class DatabaseView(View):
    def get(self, request, category):
        context = {
            "words": Words.objects.filter(category=category),
            "category": category
        }
        print(category)
        return render(request, "application/database.html", context)


class ManualUpdateView(View):
    def get(self, request, id):
        context = {
            "update_word": Words.objects.filter(pk=id),
            "word_form": ManualWordForm(),
            "id": id
        }
        return render(request, "application/update.html", context)
    
    def post(self, request, id):
        word_form = ManualWordForm(request.POST)
        if word_form.is_valid():
            Words.objects.filter(pk=id).delete()
            category = str(word_form).split('category')[2].split('"')[2]
            print(category)
            word_form.save()
            return HttpResponseRedirect(reverse("database", args=[category]))


def delete_word(request, id, category):
    Words.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse("database", args=[category]))





class QuizHomeView(View):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('SELECT DISTINCT category FROM application_words')
            category_rows = cursor.fetchall()
        categories = [category[0] for category in category_rows]
        context = {
            "categories": categories
        }
        print(categories)
        return render(request, "application/quiz-home.html", context)

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


class StatView(View):
    def get(self, request, category):
        if category == "worst":
            context = {
                "words": Words.objects.all().order_by("percentage")[:15],
                "category": category
            }
        elif category == "least":
            context = {
                "words": Words.objects.all().order_by("tries")[:15],
                "category": category
            }
        elif category == "least-category":
            with connection.cursor() as cursor:
                cursor.execute('SELECT DISTINCT category FROM application_words')
                category_rows = cursor.fetchall()
            categories = [category[0] for category in category_rows]
            context = {
                "words": Words.objects.all().order_by("tries")[:15],
                "category": category
            }
        elif category == "worst-category":
            context = {
                "words": Words.objects.all().order_by("tries")[:15],
                "category": category
            }
        else:
            context = {
                "words": Words.objects.filter(category=category).order_by("percentage"),
                "category": category
            }
        print(category)
        return render(request, "application/quiz-stat-view.html", context)


class QuizHardView(View):
    def get(self, request, iterations, id=0, correct=0):
        if id:
            last_word = Words.objects.get(pk=id)
            last_word.tries += 1
            if correct:
                last_word.correct_guesses += 1
            else:
                last_word.wrong_guesses +=1
            last_word.percentage = 100*(last_word.correct_guesses/last_word.tries)
            last_word.save()
        with connection.cursor() as cursor:
            cursor.execute('SELECT spanish_word, english_word, id FROM application_words WHERE ((100 * (correct_guesses/tries)) < 50)')
            category_rows = cursor.fetchall()
        words = [[category[0], category[1], category[2]] for category in category_rows]
        print(words)
        counter = iterations
        iterations += 1
        try:
            words[counter]
        except IndexError:
            return HttpResponseRedirect(reverse("success"))
        context = {
            "spanish_word": words[counter][0],
            "english_word": words[counter][1],
            "id": words[counter][2],
            "iterations": iterations
        }
        
        return render(request, "application/quiz-game-hard.html", context)


class QuizView(View):
    def get(self, request, iterations, category, id=0, correct=0):
        if id:
            last_word = Words.objects.get(pk=id)
            last_word.tries += 1
            if correct:
                last_word.correct_guesses += 1
            else:
                last_word.wrong_guesses +=1
            last_word.percentage = 100*(last_word.correct_guesses/last_word.tries)
            last_word.save()
        words = Words.objects.filter(category=category)
        counter = iterations
        iterations += 1
        print(words)
        words = [word for word in words]
        try:
            words[counter]
        except IndexError:
            return HttpResponseRedirect(reverse("success"))
        context = {
            "words": words[counter],
            "iterations": iterations
        }
        
        return render(request, "application/quiz-game.html", context)


class SuccessView(TemplateView):
    template_name = 'success.html'