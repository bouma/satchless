import decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

class ProductPriceMixin(models.Model):
    QTY_MODE_CHOICES = (
        ('product', _("per product")),
        ('variant', _("per variant"))
    )
    qty_mode = models.CharField(_("Quantity pricing mode"), max_length=10,
                                choices=QTY_MODE_CHOICES, default='variant',
                                help_text=_("In 'per variant' mode the unit "
                                            "price will depend on quantity "
                                            "of single variant being sold. In "
                                            "'per product' mode, total "
                                            "quantity of all product's "
                                            "variants will be used."))
    price = models.DecimalField(_("base price"), max_digits=12, decimal_places=4)

    class Meta:
        abstract = True

    def get_qty_price_overrides(self):
        return self.qty_overrides.all()


class PriceQtyOverride(models.Model):
    """
    Overrides price of product unit, depending of total quantity being sold.
    """
    min_qty = models.DecimalField(_("minimal quantity"), max_digits=10, decimal_places=4)
    price = models.DecimalField(_("unit price"), max_digits=12, decimal_places=4)

    class Meta:
        abstract = True
        ordering = ('min_qty',)


class VariantPriceOffsetMixin(models.Model):
    """
    Holds optional price offset for a variant. Does not depend on quantity.
    """
    price_offset = models.DecimalField(_("unit price offset"), default=decimal.Decimal(0),
                                       max_digits=12, decimal_places=4)

    class Meta:
        abstract = True

