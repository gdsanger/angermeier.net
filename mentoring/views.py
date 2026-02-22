import logging
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail

from .forms import ApplicationForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'mentoring/index.html')


def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            _send_emails(application)
            return redirect('apply_success')
    else:
        form = ApplicationForm()
    return render(request, 'mentoring/apply.html', {'form': form})


def apply_success(request):
    return render(request, 'mentoring/apply_success.html')


def impressum(request):
    return render(request, 'mentoring/impressum.html')


def datenschutz(request):
    return render(request, 'mentoring/datenschutz.html')


def _send_emails(application):
    # Confirmation to applicant
    try:
        send_mail(
            subject='Deine Bewerbung bei Angermeier.net',
            message=(
                f'Hallo {application.name},\n\n'
                'vielen Dank für deine Bewerbung. Wir haben sie erhalten und melden uns in Kürze bei dir.\n\n'
                'Beste Grüße\nChristian Angermeier\nangermeier.net'
            ),
            from_email=settings.EMAIL_HOST_USER or 'noreply@angermeier.net',
            recipient_list=[application.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception('Failed to send confirmation email to applicant %s', application.email)

    # Notification to admin
    try:
        detail_lines = [
            f'Neue Bewerbung eingegangen:\n',
            f'Name:    {application.name}',
            f'E-Mail:  {application.email}',
            f'Rolle:   {application.get_role_display()}',
            f'\nHintergrund:\n{application.background}',
            f'\nWarum:\n{application.why}',
            f'\nWas funktioniert nicht:\n{application.what_not_working}',
            f'\nWas wurde versucht:\n{application.what_tried}',
            f'\nBereit zur Veränderung: {"Ja" if application.ready_to_change else "Nein"}',
            f'Zeit bestätigt:         {"Ja" if application.time_confirm else "Nein"}',
            f'Budget bestätigt:       {"Ja" if application.budget_confirm else "Nein"}',
        ]
        send_mail(
            subject=f'[Mentoring] Neue Bewerbung von {application.name}',
            message='\n'.join(detail_lines),
            from_email=settings.EMAIL_HOST_USER or 'noreply@angermeier.net',
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception('Failed to send admin notification email')
