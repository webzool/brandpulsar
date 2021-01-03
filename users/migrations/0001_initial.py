# Generated by Django 3.0.5 on 2021-01-03 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('name', models.CharField(blank=True, max_length=80, null=True, verbose_name='Name')),
                ('surname', models.CharField(blank=True, max_length=80, null=True, verbose_name='Surname')),
                ('stripe_id', models.CharField(blank=True, max_length=80, null=True, verbose_name='Stripe ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='pp', verbose_name='Profile Picture')),
                ('phone', models.CharField(blank=True, max_length=80, null=True, verbose_name='Phone Number')),
                ('user_type', models.PositiveIntegerField(choices=[(1, 'Buyer'), (2, 'Seller')], default=1, verbose_name='User Type')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('current_sign_in_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='Current IP')),
                ('last_signed_in_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='Latest IP')),
                ('sign_in_count', models.IntegerField(default=0, verbose_name='Sign in count')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Joined on')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', users.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='WirePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('account_number', models.CharField(max_length=200)),
                ('routing_number', models.CharField(max_length=200)),
                ('holder_first_name', models.CharField(max_length=200)),
                ('holder_last_name', models.CharField(max_length=200)),
                ('iban', models.CharField(max_length=200)),
                ('swift', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wire_payment_methods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wire Payment',
                'verbose_name_plural': 'Wire Payment Methods',
            },
        ),
        migrations.CreateModel(
            name='SkrillPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skrill_payment_methods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Skrill Payment',
                'verbose_name_plural': 'Skrill Payment Methods',
            },
        ),
        migrations.CreateModel(
            name='PayPalPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paypal_payment_methods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PayPal Payment',
                'verbose_name_plural': 'PayPal Payment Methods',
            },
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=20, null=True, verbose_name='Amount')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('method', models.CharField(choices=[('paypal', 'PayPal'), ('cashapp', 'CashAPP'), ('skrill', 'Skrill'), ('wire', 'Wire')], max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment History',
                'verbose_name_plural': 'Payment Histories',
            },
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domains', models.ManyToManyField(blank=True, related_name='favourites', to='main.Domain', verbose_name='Domain list')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Favourite',
                'verbose_name_plural': 'Favourites',
            },
        ),
        migrations.CreateModel(
            name='CashAppPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashapp_payment_methods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CashAPP Payment',
                'verbose_name_plural': 'CashAPP Payment Methods',
            },
        ),
    ]
