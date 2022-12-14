# Generated by Django 4.1.1 on 2022-09-07 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_number', models.CharField(max_length=150, unique=True)),
                ('agent_name', models.CharField(max_length=200)),
                ('agent_position', models.CharField(max_length=200)),
                ('agent_contact', models.CharField(max_length=200, null=True)),
                ('agent_image', models.ImageField(upload_to='pic')),
            ],
        ),
    ]
