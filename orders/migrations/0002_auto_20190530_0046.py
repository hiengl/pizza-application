# Generated by Django 2.0.3 on 2019-05-30 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item_id',
            field=models.CharField(default='bdbvhgfffhuerbci', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderinfor',
            name='order_id',
            field=models.CharField(max_length=15),
        ),
    ]
