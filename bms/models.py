from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50) #创建字符串类型字
    email=models.EmailField(default=None)
    bussinesslines=models.ManyToManyField("BussinessLine")
    def __str__(self):
        return self.username

class Env(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class BussinessLine(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(null=True,max_length=64)
    def __str__(self):
        return self.name

class Asset(models.Model):

    hostname=models.CharField(max_length=32)
    ip=models.CharField(max_length=32)
    port=models.IntegerField()
    model=models.CharField(max_length=32)
    env=models.ForeignKey("Env") #外键关联Env
    hardware=models.CharField(max_length=32)
    bussiness=models.ForeignKey("BussinessLine")

class AssetDetail(models.Model):
    asset = models.OneToOneField(Asset) #可以把一对一理解为一种特殊的一对多（多的一方外键为Unique）
    hostname = models.CharField(max_length=32,null=True)
    memory = models.CharField(max_length=32,null=True)
    cpu_model = models.CharField(max_length=32,null=True)
    vender = models.CharField(max_length=32,null=True)
    product = models.CharField(max_length=32,null=True)
    sn = models.CharField(max_length=64,null=True)
    osver = models.CharField(max_length=32,null=True)
    cpu_num = models.CharField(max_length=10,null=True)
    ip = models.CharField(max_length=32) 