from django.db import models


class Group(models.Model):
    group_id = models.CharField(verbose_name='组编号', max_length=12)
    group_name = models.CharField(verbose_name='组名称', max_length=12)

    def __str__(self):
        return self.group_id

    class Meta:
        db_table = "Group"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '分组'


class User(models.Model):
    USER_GENDER_CHOICE = (
        (True, '男'),
        (False, '女'),
    )
    USER_IDENTITY_CHOICE = (
        (0, '普通职员'),
        (1, '管理员'),
    )
    USER_QUESTION_CHOICE = (
        (0, '我最喜欢的颜色'),
        (1, '我的家乡'),
        (2, '我的出生年月（如2000.3.1）'),
        (3, '我的小学班主任是'),
        (4, '我的初中班主任是'),
        (5, '我的高中班主任是'),
        (6, '我配偶的姓名'),
        (7, '我的大学辅导员是'),
        (8, '我父亲的名字'),
        (9, '我母亲的名字'),
        (10, '我大学里最好的朋友是'),
        (11, '我最想去的地方'),
    )

    '''基础信息'''
    user_id = models.CharField(verbose_name='用户id', max_length=12)
    user_password = models.CharField(max_length=20, verbose_name='密码')
    user_group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='所属组')

    '''需要完善的信息'''
    user_name = models.CharField(max_length=12, default='保密', verbose_name='姓名')
    user_gender = models.BooleanField(
        default=True,
        choices=USER_GENDER_CHOICE,
        verbose_name='性别'
    )  # true 代表男性，false 代表女性
    user_identity = models.PositiveSmallIntegerField(
        default=0,
        choices=USER_IDENTITY_CHOICE,
        verbose_name='身份与权限'
    )  # 0:职员，2:管理员
    user_question = models.PositiveSmallIntegerField(
        choices=USER_QUESTION_CHOICE,
        blank=True,
        verbose_name='密保问题'
    )  # 密保问题
    user_question_answer = models.CharField(default='', max_length=20, blank=True, verbose_name='密保问题答案')  # 密保问题答案
    user_create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 用户的创建时间

    @classmethod
    def add_user(cls, user_id, user_password, user_group):
        """
        :param user_id: 用户id
        :param user_password: 用户密码
        :param user_group: 组对象
        :return: user
        """
        user = cls(user_id=user_id, user_password=user_password, user_group=user_group)
        return user

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "User"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '用户'


class Inventory(models.Model):
    """库存"""
    inventory_id = models.CharField(max_length=12, verbose_name='编号')
    inventory_name = models.CharField(max_length=20, verbose_name='名称')
    inventory_category = models.CharField(max_length=12, verbose_name='类别')
    inventory_num = models.PositiveIntegerField(verbose_name='数量')
    inventory_unit = models.CharField(max_length=12, default='个', verbose_name='单位')
    inventory_details = models.TextField(max_length=300, default='无', verbose_name='详细信息')
    inventory_create_user = models.CharField(max_length=12, verbose_name='创建人id')
    inventory_create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    inventory_recent_change_user = models.CharField(max_length=12, verbose_name='最近修改人id')
    inventory_recent_change_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    @classmethod
    def add_inventory(
            cls,
            inventory_id,
            inventory_category,
            inventory_num,
            inventory_unit,
            inventory_details,
            inventory_create_user,
    ):
        inventory = cls(
            inventory_id=inventory_id,
            inventory_category=inventory_category,
            inventory_num=inventory_num,
            inventory_unit=inventory_unit,
            inventory_details=inventory_details,
            inventory_create_user=inventory_create_user,
            inventory_recent_change_user=inventory_create_user,
        )
        return inventory

    def __str__(self):
        return self.inventory_id

    class Meta:
        db_table = "Inventory"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '库存'


class InventoryOperation(models.Model):
    """对库存的操作，注意在每次新建库存后都要增加一个此对象"""
    '''选项'''
    INVENTORY_OPERATION_CHOICE = (
        (0, '入库'),
        (1, '出库'),
        (2, '创建'),
    )

    '''属性'''
    inventory_operation_create_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    inventory_operation_user = models.CharField(max_length=12, verbose_name='操作者id')
    inventory_operation_category = models.PositiveSmallIntegerField(
        default=0,
        choices=INVENTORY_OPERATION_CHOICE,
        verbose_name='操作类别'
    )
    inventory_operation_num = models.PositiveIntegerField(verbose_name='操作数量')
    inventory_num = models.PositiveIntegerField(verbose_name='操作后数量')
    inventory_operation_object = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name='操作的库存对象')

    @classmethod
    def add_inventory_operation(
            cls,
            inventory_operation_user,
            inventory_operation_category,
            inventory_operation_num,
            inventory_num,
            inventory_operation_object,
    ):
        inventory_operation = cls(
            inventory_operation_user=inventory_operation_user,
            inventory_operation_category=inventory_operation_category,
            inventory_operation_num=inventory_operation_num,
            inventory_num=inventory_num,
            inventory_operation_object=inventory_operation_object,
        )
        return inventory_operation

    def __int__(self):
        return self.pk

    class Meta:
        db_table = "InventoryOperation"
        ordering = ['id']  # 以id为标准升序
        verbose_name_plural = '库存操作'
