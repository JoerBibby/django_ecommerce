# Generated by Django 3.2.5 on 2021-09-05 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_order_billing_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingadress',
            old_name='same_billing_address',
            new_name='same_shipping_address',
        ),
        migrations.RemoveField(
            model_name='billingadress',
            name='save_info',
        ),
    ]
