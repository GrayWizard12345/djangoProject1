from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice


# Create your views here.
def detail(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    context = {'question': question}
    return render(request, 'poll/detail.html', context)


def index(request):
    question_list = Question.objects.all().order_by('-creation_date')
    question_list = question_list[:5]
    context = {'latest_question_list': question_list}
    return render(request, 'poll/index.html', context)


def vote(request, question_id):
    question = Question.objects.get(id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))


def results(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'poll/results.html', context)

