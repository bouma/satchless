# -*- coding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from satchless.category.models import CategorizedProductMixin
from satchless.contrib.pricing.simpleqty.models import ProductPriceMixin,\
    VariantPriceOffsetMixin
from satchless.contrib.tax.flatgroups.models import TaxedProductMixin
from satchless.util.models import construct
import satchless
import satchless.product.models

from ..categories.models import Category


class Product(ProductPriceMixin, TaxedProductMixin,
              construct(CategorizedProductMixin, category=Category)):

    name = models.CharField(_('name'), max_length=128)
    slug = models.SlugField(_('slug'), max_length=128)
    description = models.TextField(_('description'), blank=True)


class Variant(satchless.product.models.Variant, VariantPriceOffsetMixin):
    pass


class OnlineVariant(Variant):
    file = models.FileField()
    file_format = models.CharField(max_length=4)

    class Meta:
        abstract = True


class OfflineVariant(Variant):
    stock = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Book(Product):
    isbn = models.CharField(max_length=13)
    author = models.CharField(max_length=50)
    publication_date = models.DateField(blank=True)


class BookVariant(Variant):
    book = models.ForeignKey(Book)

    class Meta:
        abstract = True


class EBookVariant(BookVariant, OnlineVariant):
    pass


class TraditionalBookVariant(BookVariant, OfflineVariant):
    hard_cover = models.BooleanField(default=False)


class Movie(Product):
    director = models.CharField(max_length=50)
    premiere_date = models.DateField(blank=True)


class MovieVariant(Variant):
    movie = models.ForeignKey(Movie)

    class Meta:
        abstract = True


class OnlineMovieVariant(MovieVariant, OnlineVariant):
    with_adverts = models.BooleanField(default=False)


class TraditionalMovie(MovieVariant, OfflineVariant):
    CARRIERS = (
        ('vhs', 'VHS'),
        ('dvd', 'DVD'),
        ('br', 'BlueRay'),
    )
    carrier = models.CharField(choices=CARRIERS)


class Music(Product):
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)


class MusicVariant(Variant):
    music = models.ForeignKey(Music)

    class Meta:
        abstract = True


class MusicFileVariant(MusicVariant, OnlineVariant):
    duration = models.IntegerField()


class MusicAlbumVariant(MusicVariant, OfflineVariant):
    CARRIERS = (
        ('dvd', 'DVD'),
        ('br', 'BlueRay'),
        ('cd', 'Audio CD'))
    carrier = models.CharField(choices=CARRIERS)
