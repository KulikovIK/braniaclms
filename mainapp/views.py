from django.views.generic import TemplateView
from datetime import datetime
from django.shortcuts import redirect


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["news_title"] = "Громкий заголовок"

        context["news_preview"] = "Не очень громкое содержание"

        context["datetime_obj"] = datetime.now()

        context["range"] = range(5)

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
    print(request.GET['param1'])
    return redirect(f"https://yandex.ru/search/?text={request.GET['param1']}")
