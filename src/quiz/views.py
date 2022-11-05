from django.shortcuts import render
from django.views.generic import TemplateView

class StartPage(TemplateView):
    template_name: str = "quiz/start_page.html"

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

    def get(self, request, *args, **kwargs):
        # getが飛んだ時の処理を書く
        return render(request, self.template_name, context=self.kwargs)

class ResultPage(TemplateView):
    template_name: str = "quiz/result.html"

    def get(self, request, *args, **kwargs):
        # getが飛んだ時の処理を書く
        return render(request, self.template_name, context=self.kwargs)