from django.shortcuts import render
from django.http import HttpResponse


def index(request):
  return render(request, "index.html")
    #return HttpResponse("Hello, world. You're at the polls index.")


    #def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #context = {'latest_question_list': latest_question_list}
    #return render(request, 'polls/index.html', context)