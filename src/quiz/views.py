from django.shortcuts import render
from django.views.generic import TemplateView

class TopPage(TemplateView):
    template_name: str = "quiz/top_page.html"

    def get(self, request, *args, **kwargs):
        # getが飛んだ時の処理を書く
        return render(request, self.template_name, context=self.kwargs)

