from django import forms

from mainapp.models import CourseFeedback


class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = (
            'course',
            'user',
            'rating',
            'feedback',
        )
        # Для сокрытия каких-либо полей делай так:
        widgets = {
            'course': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            # Для радоикнопки так:
            'rating': forms.RadioSelect()
        }

        # Так как некоторые поля сокрыты, то ин надо предустановить:

    def __init__(self, *args, course=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if course and user:
            # Процесс задания переменных для инициализации формы
            self.fields['course'].initial = course.pk
            self.fields['user'].initial = user.pk
