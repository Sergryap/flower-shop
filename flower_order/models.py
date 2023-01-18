from django.db import models
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    title = models.CharField(
        verbose_name='Название',
        db_index=True,
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Bouquet(models.Model):
    title = models.CharField(
        verbose_name='Название',
        db_index=True,
        max_length=200,
        unique=True,
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории',
        related_name='bouquets',
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Цена',
        default=1600,
    )
    image = models.FileField(
        verbose_name='Изображение',
        blank=True,
        null=True,
        upload_to='images/bouquets',
        validators=[FileExtensionValidator(['png', 'jpeg', 'svg'])],
    )
    discription = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    structure = models.TextField(
        verbose_name='Состав',
        blank=True,
        null=True,
    )
    height = models.PositiveSmallIntegerField(
        verbose_name='Высота',
        default=30,
    )
    width = models.PositiveSmallIntegerField(
        verbose_name='Ширина',
        default=20,
    )

    class Meta:
        verbose_name = 'букет'
        verbose_name_plural = 'букеты'

    def __str__(self):
        return self.title


class Shop(models.Model):
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
        db_index=True,
        region='RU',
        unique=True,
    )
    address = models.CharField(
        verbose_name='Адрес',
        db_index=True,
        max_length=200,
        unique=True,
    )
    image = models.FileField(
        verbose_name='Изображение',
        blank=True,
        null=True,
        upload_to='images/shops',
        validators=[FileExtensionValidator(['png', 'jpeg', 'svg'])],
    )
    latitude = models.DecimalField(
        verbose_name='Широта',
        decimal_places=6,
        default=59.940722,
        max_digits=8,
    )
    longitude = models.DecimalField(
        verbose_name='Долгота',
        decimal_places=6,
        default=30.396429,
        max_digits=8,
    )

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'

    def __str__(self):
        return self.address


class Staff(models.Model):
    position_choices = [
        ('master', 'Мастер'),
        ('courier', 'Курьер'),
    ]

    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
        db_index=True,
        region='RU',
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=200,
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=200,
    )
    position = models.CharField(
        verbose_name='Должность',
        choices=position_choices,
        max_length=200,
    )

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

    def __str__(self):
        return f'{self.position}: {self.surname} {self.name}'


class Client(models.Model):
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
        db_index=True,
        # region='RU',
        # unique=True,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=200,
        blank=True,
        null=True,
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=200,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.surname} {self.name}'


class Order(models.Model):
    service_choices = [
        ('consultation', 'Консультация'),
        ('delivery', 'Доставка'),
    ]
    status_choices = [
        ('1 not processed', 'Необработан'),
        ('2 collect', 'Собирается'),
        ('3 on way', 'В пути'),
        ('4 completed', 'Выполнен'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Клиент',
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='сотрудник',
    )
    service = models.CharField(
        verbose_name='Статус',
        blank=True,
        choices=service_choices,
        max_length=15,
        null=True,
    )
    status = models.CharField(
        verbose_name='Статус',
        choices=status_choices,
        default='1 not processed',
        db_index=True,
        max_length=15,
    )
    address = models.CharField(
        verbose_name='Адрес доставки',
        blank=True,
        max_length=200,
        null=True,
    )
    bouquets = models.ManyToManyField(
        Bouquet,
        verbose_name='Букеты',
        related_name='orders',
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.service} {self.status} {self.client}'
