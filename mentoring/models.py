from django.db import models


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        REVIEW = "review", "In review"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    class Role(models.TextChoices):
        DEV = "dev", "Developer"
        ARCH = "arch", "Architect"
        TL = "tl", "Tech Lead"
        OTHER = "other", "Other"

    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=120)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DEV)

    background = models.TextField(help_text="Kurz: Kontext, Tech-Stack, Verantwortungsbereich")
    why = models.TextField()
    what_not_working = models.TextField()
    what_tried = models.TextField()

    ready_to_change = models.BooleanField(default=False)
    time_confirm = models.BooleanField(default=False, help_text="Zeit für Umsetzung vorhanden")
    budget_confirm = models.BooleanField(default=False, help_text="4-stelliger Betrag/Monat ist ok")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    notes_internal = models.TextField(blank=True)

    source = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return f"{self.created_at:%Y-%m-%d} - {self.name} ({self.email})"
