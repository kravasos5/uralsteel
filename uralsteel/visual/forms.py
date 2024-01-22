from django import forms
from visual.models import Employees, LadlesAccident, CranesAccident, AggregateAccident


class CustomClearableFileInputCU(forms.ClearableFileInput):
    """Виджет для добавления нового фото к форме"""
    initial_text = ''
    template_name = 'widgets/customImageFieldTemplate.html'


class ChangeEmployeeInfoForm(forms.ModelForm):
    """Форма для обновления пользовательских данных"""
    email = forms.EmailField(required=True,
                             label='Адресс электронной почты')
    photo = forms.ImageField(label='Фото (рекомендуемый размер 200x200 px)',
                             widget=CustomClearableFileInputCU(attrs={'id': 'id_photo'}))

    class Meta:
        model = Employees
        fields = ('photo', 'username', 'email',
                  'first_name', 'last_name', 'patronymic',
                  'send_messages')


class AccidentStartingForm(forms.Form):
    """
    Форма начальной стадии написания отчёта о поломке или аварии
    содержит в себе список доступных для выбора элементов
    """
    CHOICES = (
        ('cr', 'Кран'),
        ('la', 'Ковш'),
        ('ag', 'Агрегат')
    )
    accident_type = forms.ChoiceField(choices=CHOICES, label='Что сломалось?')


class AccidentForm(forms.ModelForm):
    """Форма для проишествий"""

    class Meta:
        fields = ('object',)
        exclude = ['created_at', 'author', 'report']


class AccidentDetailForm(forms.ModelForm):
    """Форма для проишествий (подробная)"""
    report = forms.CharField(label='Подробное описание проблемы',
                             help_text='минимум 10 слов, до 800 символов',
                             widget=forms.Textarea)

    class Meta:
        fields = ('object', 'report')
        exclude = ['created_at', 'author']


class LadlesAccidentForm(AccidentForm):
    """Форма проишествий с ковшами"""

    class Meta(AccidentForm.Meta):
        model = LadlesAccident


class LadlesAccidentDetailForm(AccidentDetailForm):
    """Форма проишествий с ковшами (подробная)"""

    class Meta(AccidentDetailForm.Meta):
        model = LadlesAccident


class CranesAccidentForm(AccidentForm):
    """Форма проишествий с кранами"""

    class Meta(AccidentForm.Meta):
        model = CranesAccident


class CranesAccidentDetailForm(AccidentDetailForm):
    """Форма проишествий с кранами (подробная)"""

    class Meta(AccidentDetailForm.Meta):
        model = CranesAccident


class AggregateAccidentForm(AccidentForm):
    """Форма проишествий с агрегатами"""

    class Meta(AccidentForm.Meta):
        model = AggregateAccident


class AggregateAccidentDetailForm(AccidentDetailForm):
    """Форма проишествий с агрегатами (подробная)"""

    class Meta(AccidentDetailForm.Meta):
        model = AggregateAccident
