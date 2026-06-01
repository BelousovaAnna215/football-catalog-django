from django import forms
from .models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'position', 'number',
                  'is_captain', 'club']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'club': forms.Select(attrs={'class': 'form-control'}),
            'awards': forms.SelectMultiple(attrs={'size': 4}),
        }

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if not name:
            raise forms.ValidationError('Имя обязательно для заполнения')

        if len(name) < 2:
            raise forms.ValidationError('Имя должно содержать минимум 2 символа')

        if len(name) > 50:
            raise forms.ValidationError('Имя не может быть длиннее 50 символов')

        if not all(c.isalpha() or c in ' -' for c in name):
            raise forms.ValidationError('Имя может содержать только буквы, дефис и пробел')

        return name.strip().title()

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name')

        if not name:
            raise forms.ValidationError('Фамилия обязательна для заполнения')

        if len(name) < 2:
            raise forms.ValidationError('Фамилия должна содержать минимум 2 символа')

        if len(name) > 50:
            raise forms.ValidationError('Фамилия не может быть длиннее 50 символов')

        if not all(c.isalpha() or c in ' -' for c in name):
            raise forms.ValidationError('Фамилия может содержать только буквы, дефис и пробел')

        return name.strip().title()

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None:
            raise forms.ValidationError('Возраст обязателен для заполнения')

        if age < 16 or age > 50:
            raise forms.ValidationError('Возраст должен быть от 16 до 50 лет')
        return age

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if number is None:
            raise forms.ValidationError('Игровой номер обязателен')

        if number < 1 or number > 99:
            raise forms.ValidationError('Номер должен быть больше 0 и меньше 100')

        club = self.cleaned_data.get('club')
        if club and number:
            existing_player = Player.objects.filter(club=club, number=number).exclude(id=self.instance.id)
            if existing_player.exists():
                raise forms.ValidationError('Игрок с таким номером уже есть в клубе. Выберите другой номер.')
        return number

    def clean_club(self):
        club = self.cleaned_data.get('club')

        if not club:
            raise forms.ValidationError('Выберите клуб из списка')

        return club

    def clean_is_captain(self):
        is_captain = self.cleaned_data.get('is_captain')
        club = self.cleaned_data.get('club')

        if is_captain and club:
            existing_captain = Player.objects.filter(club=club, is_captain=True).exclude(id=self.instance.id)
            if existing_captain.exists():
                raise forms.ValidationError('В клубе уже есть капитан.')
        return is_captain
