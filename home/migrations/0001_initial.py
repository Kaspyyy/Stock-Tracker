# Generated by Django 5.0 on 2023-12-20 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='stock_icons/')),
                ('last_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('market_cap', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('pe_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]
