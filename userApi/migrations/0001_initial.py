# Generated by Django 4.2.6 on 2023-11-03 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('language', models.CharField(blank=True, max_length=20, null=True)),
                ('proficiency', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SkillLevel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('skill_level', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('skill_name', models.CharField(blank=True, max_length=20, null=True)),
                ('skill_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userApi.skilllevel')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('short_intro', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, max_length=1000, null=True)),
                ('profile_picture', models.ImageField(default='profile/user-default.png', null=True, upload_to='profile/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employment_type', models.CharField(blank=True, max_length=50, null=True)),
                ('user_type', models.CharField(blank=True, max_length=20, null=True)),
                ('rate_total', models.FloatField(blank=True, default=0, null=True)),
                ('rate_ratio', models.FloatField(blank=True, default=0, null=True)),
                ('languages', models.ManyToManyField(blank=True, to='userApi.language')),
                ('skills', models.ManyToManyField(blank=True, to='userApi.skills')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('job_name', models.CharField(max_length=100)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('details', models.TextField(blank=True, max_length=600, null=True)),
                ('total_exp', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userApi.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ExpectedSalary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('currency', models.CharField(blank=True, max_length=3, null=True)),
                ('nominal', models.FloatField()),
                ('paid_period', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.OneToOneField(default='Personal', on_delete=django.db.models.deletion.CASCADE, to='userApi.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('major', models.CharField(blank=True, max_length=50, null=True)),
                ('degrees', models.CharField(blank=True, max_length=20, null=True)),
                ('school_name', models.CharField(blank=True, max_length=100, null=True)),
                ('start_year', models.DateField()),
                ('end_year', models.DateField()),
                ('user', models.ForeignKey(default='Personal', on_delete=django.db.models.deletion.CASCADE, to='userApi.profile')),
            ],
        ),
        migrations.CreateModel(
            name='UserRate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('comment', models.TextField(default='N/A', max_length=1000)),
                ('rate_value', models.IntegerField(default=5)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='given_rating', to='userApi.profile')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userApi.profile')),
            ],
            options={
                'unique_together': {('from_user', 'to_user')},
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('portfolio_link', models.CharField(max_length=100)),
                ('portfolio_name', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ForeignKey(default='Personal', on_delete=django.db.models.deletion.CASCADE, to='userApi.profile')),
            ],
            options={
                'unique_together': {('user', 'portfolio_name')},
            },
        ),
        migrations.CreateModel(
            name='Networking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('networking_link', models.CharField(max_length=100)),
                ('networking_name', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ForeignKey(default='Personal', on_delete=django.db.models.deletion.CASCADE, to='userApi.profile')),
            ],
            options={
                'unique_together': {('user', 'networking_name')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('subject', models.CharField(blank=True, max_length=200, null=True)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False, null=True)),
                ('date_read', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='userApi.profile')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userApi.profile')),
            ],
            options={
                'ordering': ['is_read', '-created'],
                'unique_together': {('sender', 'recipient')},
            },
        ),
    ]
