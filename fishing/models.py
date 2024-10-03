from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class item(models.Model):
    name=models.CharField(max_length=20)
    lake=models.CharField(max_length=20)
    rarity=models.IntegerField()
    weight=models.IntegerField()
    describe=models.CharField(max_length=255)
    category=models.CharField(max_length=20,blank=True) #health,durability,lucky,efficiency
    value=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return f"{self.lake}-{self.name}"
    
class PlayerProfile(models.Model):
    name=models.OneToOneField(User, on_delete=models.CASCADE)
    health=models.IntegerField(default=10000) #體力
    money=models.IntegerField(default=10000) #金錢
    def __str__(self):
        return f"{self.name} {self.health} {self.money}"
    
class UserItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # 關聯用戶
    item = models.CharField(max_length=20)
    quantity = models.IntegerField()  # 物品數量

    def sell_item(self, quantity_to_sell, item_value):
        if self.quantity >= quantity_to_sell:
            # 移除用戶的物品
            self.quantity -= quantity_to_sell
            if self.quantity==0:
                self.delete()
            else:
                self.save()
            # 更新用戶的金錢
            obj=PlayerProfile.objects.get(name=self.user)
            obj.money += quantity_to_sell * item_value
            obj.save()
        return self.quantity
    
    def __str__(self):
        return f"{self.user} - {self.item} x {self.quantity}"
    
class FishingSession(models.Model):
    player = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lake = models.CharField(max_length=50, blank=True, null=True)  # 保存玩家在哪個湖釣魚
    start_time = models.DateTimeField()  # 釣魚開始時間
    is_active = models.BooleanField(default=True)  # 紀錄釣魚是否還在進行
    def stop_fishing(self):
        self.is_active = False
        self.save()