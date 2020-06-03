from django.db import models
from utils.models import BaseModel

# Create your models here.
class UserProfile(BaseModel):
    username=models.CharField(max_length=11,verbose_name='用户名',unique=True)
    password=models.CharField(max_length=32,verbose_name='密码')
    email=models.CharField(max_length=50,verbose_name='邮箱')
    phone=models.CharField(max_length=11,verbose_name='手机')
    isActive=models.BooleanField(default=False,verbose_name='激活状态')

    class Meta:
        db_table='user_profile'

    def __str__(self):
        return str(self.id)

class Address(BaseModel):
    uid=models.ForeignKey('UserProfile',verbose_name=u'用户id',related_name='address')
    receiver=models.CharField(max_length=20,verbose_name=u'收件人')
    address=models.CharField(max_length=100,verbose_name=u'收货地址')
    default_address=models.BooleanField(default=False,verbose_name='默认收货地址')
    isActive=models.BooleanField(default=True,verbose_name=u'是否删除')
    postcode=models.CharField(max_length=20,verbose_name=u'邮政编码')
    receiver_mobile=models.CharField(max_length=11,verbose_name=u'手机号')
    tag=models.CharField(default=None,max_length=10,verbose_name=u'标签')

    class Meta:
        db_table='address'
        verbose_name='用户地址'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (
            str(self.id), self.receiver, self.address, self.default_address, self.postcode, self.receiver_mobile)



