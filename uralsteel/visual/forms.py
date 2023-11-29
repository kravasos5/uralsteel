from django import forms
from visual.models import Employees


class CustomClearableFileInputCU(forms.ClearableFileInput):
    '''Виджет для добавления нового фото к форме'''
    initial_text = ''
    template_name = 'widgets/customImageFieldTemplate.html'

class ChangeEmployeeInfoForm(forms.ModelForm):
    '''форма для обновления пользовательских данных'''
    email = forms.EmailField(required=True,
                             label='Адресс электронной почты')
    photo = forms.ImageField(label='Фото (рекомендуемый размер 200x200 px)',
                              widget=CustomClearableFileInputCU(attrs={'id': 'id_photo'}))

    class Meta:
        model = Employees
        fields = ('photo', 'username', 'email',
                  'first_name', 'last_name', 'patronymic',
                  'send_messages')