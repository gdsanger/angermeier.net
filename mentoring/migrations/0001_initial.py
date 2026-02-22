from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.CharField(
                    choices=[('dev', 'Developer'), ('arch', 'Architect'), ('tl', 'Tech Lead'), ('other', 'Other')],
                    default='dev',
                    max_length=20,
                )),
                ('background', models.TextField(help_text='Kurz: Kontext, Tech-Stack, Verantwortungsbereich')),
                ('why', models.TextField()),
                ('what_not_working', models.TextField()),
                ('what_tried', models.TextField()),
                ('ready_to_change', models.BooleanField(default=False)),
                ('time_confirm', models.BooleanField(default=False, help_text='Zeit für Umsetzung vorhanden')),
                ('budget_confirm', models.BooleanField(default=False, help_text='4-stelliger Betrag/Monat ist ok')),
                ('status', models.CharField(
                    choices=[('new', 'New'), ('review', 'In review'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
                    default='new',
                    max_length=20,
                )),
                ('notes_internal', models.TextField(blank=True)),
                ('source', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
