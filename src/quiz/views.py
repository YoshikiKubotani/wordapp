from django.shortcuts import render
from django.views.generic import TemplateView

from .models import MasterWordTable
from .pyfiles import make_random_test

class StartPage(TemplateView):
    template_name: str = "quiz/start_page.html"

    def get(self, request, *args, **kwargs):
        # getが飛んだ時の処理を書く
        return render(request, self.template_name, context=self.kwargs)

class ModePage(TemplateView):
    template_name: str = "quiz/mode.html"

    def get(self, request, *args, **kwargs):
        # getが飛んだ時の処理を書く
        return render(request, self.template_name, context=self.kwargs)

class GenraPage(TemplateView):
    template_name: str = "quiz/genra.html"

    def get(self, request, *args, **kwargs):
        # getが飛んだ時の処理を書く
        return render(request, self.template_name, context=self.kwargs)

class WordLevelPage(TemplateView):
    template_name: str = "quiz/wordlevel.html"

    def get(self, request, *args, **kwargs):
        # getが飛んだ時の処理を書く
        return render(request, self.template_name, context=self.kwargs)

class SolvePage(TemplateView):
    template_name: str = "quiz/solve.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_items = MasterWordTable.objects.order_by("-id")
        test_set = make_random_test(all_items, num_question=20, num_options=4)
        context["test_set"] = test_set
        context["num_question"] = 20
        return context

class ResultPage(TemplateView):
    template_name: str = "quiz/result.html"

    def get(self, request, *args, **kwargs):
        # getが飛んだ時の処理を書く
        return render(request, self.template_name, context=self.kwargs)