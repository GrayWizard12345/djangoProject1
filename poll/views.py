from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Question


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

