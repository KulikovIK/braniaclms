from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.core.cache import cache
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mainapp import tasks
from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Courses, Lesson, CourseTeachers, CourseFeedback


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsListView(ListView):
    model = News
    paginate_by = 2     # Число выводимых "строк" на страницу

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News
    # Тут нужно описать вывод ошибки 404, если происходит попытка
    # просмотра удаленных новостей пользователями


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'  # вывести все поля у модели
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'  # вывести все поля у модели
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


class CourseDetailView(TemplateView):
    template_name = 'mainapp/course_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Блок "как в методичке"
        # get_object_or_404 возвращает либо объект, либо "404", если ничего не нашлось. Полезная штука!
        context_data['course_object'] = get_object_or_404(Courses, pk=self.kwargs.get('pk'))
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        context_data['teachers'] = CourseTeachers.objects.filter(course=context_data['course_object'])

        # Кэширование на уровне контроллера
        feedback_list_key = f'course_feedback_{context_data["course_object"].pk}'
        cached_feedback_list = cache.get(feedback_list_key)
        if cached_feedback_list is None:
            context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])
            cache.set(feedback_list_key, context_data['feedback_list'], timeout=300)
        else:
            context_data['feedback_list'] = feedback_list_key

        # Если пользователь авторизован, то вызывается форма для заполнения отзыва
        if self.request.user.is_authenticated:
            context_data['feedback_form'] = CourseFeedbackForm(
                user=self.request.user,
                course=context_data['course_object'],
            )
        # свой пагинатор
        # from django.core.paginator import Paginator
        # paginator = Paginator(context_data['feedback_list'], 2) # данные и количество записей на страницу
        # paginator.page(2)   # номер страницы

        return context_data


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    # В этом случае не будет создаваться success_url, так как метод
    # form_valid будет генерировать ответ
    def form_valid(self, form):
        # сохраняем форму
        self.object = form.save()
        # рендерим часть страницы с отзывами из шаблона и контекста
        rendered_template = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        # Этот контент отображается JS кодом, что в блоке <script> в конце файла шаблона
        return JsonResponse({'card': rendered_template})


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"

    def post(self, *args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_from = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_to_email.delay(message_body, message_from)

        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))



class CoursesListPageView(ListView):
    template_name = "mainapp/courses_list.html"
    model = Courses


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


class LogView(UserPassesTestMixin, TemplateView):
    # UserPassesTestMixin позволяет добавить возможность проверки уровня доступа
    template_name = 'mainapp/logs.html'

    # Цункция проверки того, что запрос делает админ
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log_lines = []
        with open(settings.BASE_DIR / 'log/myapp_log.log') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                log_lines.insert(0, line)
            context_data['logs'] = log_lines
        return context_data


class LogDownloadView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))

