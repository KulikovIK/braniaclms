from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Courses, Lesson, CourseTeachers, CourseFeedback


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsListView(ListView):
    model = News
    paginate_by = 5

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
        context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])

        # Если пользователь авторизован, то вызывается форма для заполнения отзыва
        if self.request.user.is_authenticated:
            context_data['feedback_form'] = CourseFeedbackForm(
                user=self.request.user,
                course=context_data['course_object'],
            )

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
