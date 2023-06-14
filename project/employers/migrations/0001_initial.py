# Generated by Django 4.1.5 on 2023-06-14 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecruitersProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, upload_to='')),
                ('recruiter_bio', models.TextField(blank=True, max_length=255)),
                ('location', models.CharField(max_length=40)),
                ('company_name', models.CharField(max_length=40)),
                ('company_website', models.URLField(default=None, null=True)),
                ('company_email', models.EmailField(max_length=30)),
                ('company_mobile', models.CharField(max_length=30)),
                ('company_address_line1', models.CharField(max_length=50)),
                ('company_address_line2', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('post_balance', models.IntegerField(default=0, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.account')),
            ],
        ),
    ]
