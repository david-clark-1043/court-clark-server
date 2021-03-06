# Generated by Django 4.0.5 on 2022-06-22 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courtzapi', '0003_alter_docket_case_name_alter_docket_case_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docketparty',
            name='docket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docket_parties', to='courtzapi.docket'),
        ),
        migrations.AlterField(
            model_name='docketparty',
            name='rep_firm_party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docket_parties', to='courtzapi.repfirmparty'),
        ),
    ]
