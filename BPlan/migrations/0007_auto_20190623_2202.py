# Generated by Django 2.2.2 on 2019-06-23 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BPlan', '0006_auto_20190623_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_identity',
            field=models.PositiveSmallIntegerField(choices=[(0, '普通职员'), (1, '管理员')], default=0, verbose_name='身份与权限'),
        ),
        migrations.CreateModel(
            name='InventoryOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_operation_create_time', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
                ('inventory_operation_user', models.CharField(max_length=12, verbose_name='操作者id')),
                ('inventory_operation_category', models.PositiveSmallIntegerField(choices=[(0, '入库'), (1, '出库'), (2, '创建')], default=0, verbose_name='操作类别')),
                ('inventory_operation_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BPlan.Inventory', verbose_name='操作的库存对象')),
            ],
            options={
                'verbose_name_plural': '库存操作',
                'db_table': 'InventoryOperation',
                'ordering': ['id'],
            },
        ),
    ]
