from django.db import models

NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='Created at')
    updated = models.DateTimeField(auto_now=True, editable=True, verbose_name='Updated at')
    deleted = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class DataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class News(BaseModel):
    objects = DataManager()

    title = models.CharField(max_length=256, verbose_name='Title')
    preambule = models.CharField(max_length=1024, verbose_name='Preambule')
    body = models.TextField(blank=True, null=True, verbose_name='Body')
    body_as_markdown = models.BooleanField(default=False, verbose_name='As markdown')

    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    class Meta:
        ordering = ('-created',)
        verbose_name = 'News'
        verbose_name_plural = 'Newses'


class Courses(BaseModel):
    objects = DataManager()

    name = models.CharField(max_length=256, verbose_name='Name')
    description = models.TextField(
        blank=True, null=True, verbose_name='Description'
    )
    description_as_markdown = models.BooleanField(
        default=False, verbose_name='As markdown'
    )
    cost = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name='Cost'
    )
    cover = models.CharField(
        max_length=25, default='no_image.svg', verbose_name='Cover'
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"


class Lesson(BaseModel):

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Title")
    description = models.TextField(
        blank=True, null=True, verbose_name="Description"
    )
    description_as_markdown = models.BooleanField(
        default=False, verbose_name="As markdown"
    )

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        ordering = ("course", "num")


class CourseTeachers(models.Model):

    course = models.ManyToManyField(Courses)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateField(verbose_name="Birth date")

    def __str__(self) -> str:
        return f"{self.pk} {self.name_first} {self.name_second}"

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

