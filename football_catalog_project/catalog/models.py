from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название страны')
    continent = models.CharField(max_length=50, verbose_name='Континент')

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название клуба')
    city = models.CharField(max_length=100, verbose_name='Город')
    stadium = models.CharField(max_length=100, verbose_name='Стадион')

    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='Страна')

    def __str__(self):
        return self.name


class Coach(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    age = models.IntegerField(verbose_name='Возраст')

    club = models.OneToOneField(Club, on_delete=models.PROTECT, verbose_name='Клуб')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Player(models.Model):
    POSITIONS = [
        ('GK', 'Вратарь'),
        ('DEF', 'Защитник'),
        ('MID', 'Полузащитник'),
        ('FWD', 'Нападающий'),
    ]

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    position = models.CharField(max_length=3, choices=POSITIONS, verbose_name='Позиция')
    number = models.IntegerField(verbose_name='Игровой номер')
    is_captain = models.BooleanField(default=False, verbose_name='Капитан')

    club = models.ForeignKey(Club, on_delete=models.PROTECT, verbose_name='Клуб', related_name='players')

    def __str__(self):
        return f"{self.first_name} {self.last_name} (#{self.number})"


class Award(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название награды')

    players = models.ManyToManyField(Player, related_name='awards', blank=True, verbose_name='Игроки')

    def __str__(self):
        return f"{self.name}"
