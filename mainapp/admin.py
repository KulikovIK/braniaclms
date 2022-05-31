from django.contrib import admin
from django.utils.html import format_html
from mainapp.models import News, Courses, Lesson, CourseTeachers

admin.site.register(Courses)
admin.site.register(Lesson)
admin.site.register(CourseTeachers)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'deleted', 'slug')   # Список выводимых параметров
    ordering = ('pk',)      # Определение порядка вывода
    list_filter = ('deleted', 'created')    # Фильтрация списка (справа)
    list_per_page = 2   # Пагинатор по 2 записи на страницу
    search_fields = ('title', 'preambule', 'body') # фильтр на вывод
    actions = ('mark_as_delete',)  # добавление кастомного действия


    def slug(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.title.lower().replace(' ', '-'),
            obj.title
        )
        # return obj.title.lower().replace(' ', '-')

    slug.short_description = 'Слаг'

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'