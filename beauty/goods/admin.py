from django.contrib import admin
from .models import *

# Register your models here.
from django_redis import get_redis_connection

redis_conn=get_redis_connection('goods')

class BaseModel(admin.ModelAdmin):
    def save_model(self,request,obj,form,change):
        super().save_model(request,obj,form,change)
        redis_conn.delete('index_cache')
        print('保存数据时，首页缓存删除')

    def delete_model(self,request,obj):
        super().delete_model(request,obj)
        redis_conn.delete('index_cache')
        print('删除数据时，首页缓存删除')

@admin.register(Brand)
class BrandAdmin(BaseModel):
    list_display=['id','name']
    list_per_page=20
    ordering=('create_time',)

@admin.register(Catalog)
class CatalogAdmin(BaseModel):
    list_display=['id','name']
    list_per_page=20
    ordering=('create_time',)