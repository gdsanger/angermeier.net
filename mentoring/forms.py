from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'name', 'email', 'role',
            'background', 'why', 'what_not_working', 'what_tried',
            'ready_to_change', 'time_confirm', 'budget_confirm',
        ]
        labels = {
            'name': 'Dein Name',
            'email': 'E-Mail-Adresse',
            'role': 'Deine Rolle',
            'background': 'Dein Hintergrund',
            'why': 'Warum willst du das Mentoring?',
            'what_not_working': 'Was funktioniert aktuell nicht?',
            'what_tried': 'Was hast du bereits versucht?',
            'ready_to_change': 'Ich bin bereit, bestehende Prozesse infrage zu stellen',
            'time_confirm': 'Ich habe Zeit für die Umsetzung',
            'budget_confirm': 'Ich bin bereit einen kleinen 4-stelligen Betrag pro Monat zu investieren',
        }
        help_texts = {
            'background': 'Kurz: Kontext, Tech-Stack, Verantwortungsbereich',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dein vollständiger Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'deine@email.com',
            }),
            'role': forms.Select(attrs={
                'class': 'form-select',
            }),
            'background': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Kurz: Kontext, Tech-Stack, Verantwortungsbereich',
            }),
            'why': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Was treibt dich an, dieses Mentoring zu suchen?',
            }),
            'what_not_working': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Was läuft aktuell nicht so, wie du es dir vorstellst?',
            }),
            'what_tried': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Was hast du bereits unternommen, um das Problem zu lösen?',
            }),
            'ready_to_change': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'time_confirm': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'budget_confirm': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
