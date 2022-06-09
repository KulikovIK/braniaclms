from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from mainapp import models as mainapp_models


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_qs"] = mainapp_models.News.objects.all()[:5]
        return context


class NewsPageDetailView(TemplateView):
    template_name = "mainapp/news_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context["news_object"] = get_object_or_404(mainapp_models.News, pk=pk)
        return context


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class CoursesListPageView(TemplateView):
    template_name = "mainapp/courses_list.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class NewsWithPaginatorView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)

        context["page_num"] = page

        return context


def search(request):
    query = request.GET.get('param1')
    if query:
        return redirect(f"https://yandex.ru/search/?text={query}")
