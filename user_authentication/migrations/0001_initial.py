# Generated by Django 4.2.2 on 2023-11-23 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user_authentication.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.CharField(default=user_authentication.utils.generate_id, max_length=128, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=18, unique=True)),
                ('gender', models.CharField(max_length=6)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date_created')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(related_name='user_auth_group', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='user_auth_permission', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.CharField(default=user_authentication.utils.generate_id, max_length=64, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('age', models.IntegerField(blank=True, null=True)),
                ('bloog_group', models.CharField(blank=True, max_length=5, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('genotype', models.CharField(blank=True, max_length=7, null=True)),
                ('Medical_records', models.CharField(blank=True, max_length=150, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date_created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_rel', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.CharField(default=user_authentication.utils.generate_id, max_length=64, primary_key=True, serialize=False)),
                ('token', models.IntegerField(default=user_authentication.utils.generate_token)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('expired', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
