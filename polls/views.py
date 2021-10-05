from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Question, Choice

#---------------------------QUESTION--------------------------#
def index(response):
    if response.method == "POST":
        if response.POST.get("newQuestion"):
            txt = response.POST.get("question")
            if len(txt) > 2:
                q = Question(question_text=txt, pub_date=timezone.now())
                q.save()
                return HttpResponseRedirect(reverse('polls:index'))
            else:
                print("invalid")

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(response, 'polls/index.html', context)


#---------------------------ALL ???--------------------------#
def all(response):
    if response.method == "POST":
        if response.POST.get("newQuestion"):
            txt = response.POST.get("question")
            if len(txt) > 2:
                q = Question(question_text=txt, pub_date=timezone.now())
                q.save()
                return render(response, 'polls/detail.html', {'question': q})
            else:
                print("invalid")

    all_questions = Question.objects.order_by('-pub_date').all()
    context = {'all_questions': all_questions}
    return render(response, 'polls/index.html', context)


#---------------------------DETAIL--------------------------#
def detail(response, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(response, 'polls/detail.html', {'question': question})


#---------------------------RESULTS--------------------------#
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


#---------------------------VOTE--------------------------#
def vote(response, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if response.method == "POST":
        if response.POST.get("addChoice"):
            txt = response.POST.get("newChoice")
            if len(txt) > 2:
                c = Choice(question=question, choice_text=txt, votes=0)
                c.save()
                return HttpResponseRedirect(reverse('polls:index'))
        else:
            try:
                selected_choice = question.choice_set.get(pk=response.POST['choice'])
            except (KeyError, Choice.DoesNotExist):
                context = { 'alert_flag': True }
                return render(response, 'polls/index.html', context)
            else:
                selected_choice.votes += 1
                selected_choice.save()
                redirect('/polls')
                return HttpResponseRedirect(reverse('polls:index'))




#---------------------------DELETE--------------------------#
def delete(response, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if response.method == "POST":
        question.delete()
        return redirect('/polls')

    return render(response, 'index.html', {})
