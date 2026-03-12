from django.db import models

from apps.common.models import TimeStampedModel


class Restaurant(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        SUSPENDED = 'suspended', 'Suspended'
        TRIAL_EXPIRED = 'trial_expired', 'Trial expired'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    def suspend(self) -> None:
        self.is_active = False
        self.status = self.Status.SUSPENDED
        self.save(update_fields=['is_active', 'status', 'updated_at'])

    def activate(self) -> None:
        self.is_active = True
        self.status = self.Status.ACTIVE
        self.save(update_fields=['is_active', 'status', 'updated_at'])

    def __str__(self) -> str:
        return self.name
