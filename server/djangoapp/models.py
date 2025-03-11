from email.policy import default
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

CAR_TYPE_CHOICES = (
    ("SEDAN", "Sedan"),
    ("SUV", "SUV"),
    ("WAGON", "WAGON"),
)


class CarMake(models.Model):
    name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Car Make Name"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Car Make Description"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    logo_url = models.URLField(
        max_length=200, null=True, blank=True, verbose_name="Brand Logo URL"
    )
    website = models.URLField(
        max_length=200, null=True, blank=True, verbose_name="Official Website"
    )
    founded_year = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Founded Year"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Car Make"
        verbose_name_plural = "Car Makes"


class CarModel(models.Model):
    name = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Car Model Name"
    )
    type_car = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Car Type",
        choices=CAR_TYPE_CHOICES,
        default='SUV'
    )
    year = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Car Year",
        validators=[MinValueValidator(2015), MaxValueValidator(2025)],
        default=2025
    )
    maker = models.ForeignKey(
        CarMake, on_delete=models.CASCADE, verbose_name="Car Make"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.maker.name} {self.name} ({self.year})"

    class Meta:
        ordering = ["-year", "maker__name", "name"]
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"
