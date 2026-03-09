import logging
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse

from .forms import ApplicationForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'mentoring/index.html')

def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: https://angermeier.net/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


def sitemap_xml(request):
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://angermeier.net/</loc>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://angermeier.net/bewerben/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://angermeier.net/impressum/</loc>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://angermeier.net/datenschutz/</loc>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
"""
    return HttpResponse(content, content_type="application/xml")

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
    email_context_base = {
        'impressum_url': f'{settings.SITE_BASE_URL}/impressum',
        'datenschutz_url': f'{settings.SITE_BASE_URL}/datenschutz',
    }
    from_email = settings.EMAIL_HOST_USER or 'noreply@angermeier.net'

    # Confirmation to applicant
    try:
        plain_text = (
            f'Hallo {application.name},\n\n'
            'vielen Dank für deine Bewerbung. Wir haben sie erhalten und melden uns in Kürze bei dir.\n\n'
            'Beste Grüße\nChristian Angermeier\nangermeier.net'
        )
        html_body = render_to_string(
            'mentoring/email/application_confirmation.html',
            {**email_context_base, 'name': application.name},
        )
        msg = EmailMultiAlternatives(
            subject='Deine Bewerbung bei Angermeier.net',
            body=plain_text,
            from_email=from_email,
            to=[application.email],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send(fail_silently=False)
    except Exception:
        logger.exception('Failed to send confirmation email to applicant %s', application.email)

    # Notification to admin
    try:
        plain_text = '\n'.join([
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
        ])
        html_body = render_to_string(
            'mentoring/email/application_admin.html',
            {
                **email_context_base,
                'name': application.name,
                'email': application.email,
                'role': application.get_role_display(),
                'background': application.background,
                'why': application.why,
                'what_not_working': application.what_not_working,
                'what_tried': application.what_tried,
                'ready_to_change': 'Ja' if application.ready_to_change else 'Nein',
                'time_confirm': 'Ja' if application.time_confirm else 'Nein',
                'budget_confirm': 'Ja' if application.budget_confirm else 'Nein',
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'[Mentoring] Neue Bewerbung von {application.name}',
            body=plain_text,
            from_email=from_email,
            to=[settings.ADMIN_EMAIL],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send(fail_silently=False)
    except Exception:
        logger.exception('Failed to send admin notification email')
