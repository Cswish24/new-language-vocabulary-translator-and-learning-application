from django.db import connection
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from .models import Words
from .forms import EnWordForm,EsWordForm, ManualWordForm
from .translator_api import translate_en, translate_es
from django.db.models import Avg, Max, Min, Count, Sum


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
        if category == "None":
            words = Words.objects.all().order_by("percentage")[:15]
            hard_quiz = True
        else:            
            words = Words.objects.filter(category=category).order_by("id")
            hard_quiz = False
        counter = iterations
        iterations += 1
        print(words)
        lwords = [word for word in words]
        try:
            lwords[counter]
        except IndexError:
            return HttpResponseRedirect(reverse("success"))
        context = {
            "words": lwords[counter],
            "iterations": iterations,
            "hard_quiz": hard_quiz,
        }
        
        return render(request, "application/quiz-game.html", context)


class SuccessView(TemplateView):
    template_name = 'success.html'