from django.shortcuts import render, redirect
from django.utils import timezone
from .models import FishingSession,item,UserItem,PlayerProfile
from django.contrib.auth.models import User
from datetime import datetime
import random

def time_diff(dt1, dt2):
    # 計算兩個時間的差異
    diff = (dt2 - dt1).total_seconds()
    # 如果時間差異超過 1 小時，限制為 1 小時
    if diff > 3600:
        return 3600
    elif diff < 0:
        return 0  # 如果 dt2 比 dt1 還早，返回 0
    else:
        return int(diff)
    
def get_item(lake,secs):
    list=[]
    items=item.objects.filter(lake=lake)
    p=0.5 #調整機率
    rare_sum=0
    for i in items:
        rare_sum+=i.rarity
    for sec in range(secs):
        for i in items:
            item_p=p*(i.rarity/rare_sum)
            if random.random()<=item_p: #拿到此物品
                list.append(str(i.name))
    return list


def fishing_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')  # 從表單中取得動作
        if action == 'start_fishing':
            return start_fishing(request)
        elif action == 'stop_fishing':
            return stop_fishing(request)
    else:
        session=FishingSession.objects.filter(player=request.user, is_active=True).last()
        if session:
            return render(request, 'fishing/start_fishing.html')
        else:
            return render(request, 'fishing/index.html')

def start_fishing(request):
    lake_name = request.POST.get('lake')  # 從表單中取得湖的名稱
    session=FishingSession.objects.filter(player=request.user, is_active=True).last()
    if session:
        time_from=timezone.localtime(session.start_time)
        return render(request, 'fishing/start_fishing.html', {
            'message': f'{time_from.strftime("%Y/%m/%d %H:%M:%S")} 已在 {lake_name} 開始釣魚！'
        })
    elif lake_name:
        time_from = datetime.now()
        # 使用 Django ORM 插入一條新的 FishingSession 記錄
        FishingSession.objects.create(
            player=request.user,  # 保存當前用戶
            lake=lake_name,  # 保存湖泊名稱
            start_time=time_from,  # 保存開始時間
            is_active=True  # 設置釣魚會話為激活狀態
        )
        # 返回釣魚頁面，顯示成功信息
        return render(request, 'fishing/start_fishing.html', {
            'message': f'{time_from.strftime("%Y/%m/%d %H:%M:%S")} 已在 {lake_name} 開始釣魚！'
        })
    return redirect('fishing_view')

def stop_fishing(request):
    # 找到該玩家正在進行的釣魚會話，並將其標記為結束
    session = FishingSession.objects.filter(player=request.user, is_active=True).last()
    h=0
    if session:
        time_to = timezone.now()  # 使用 timezone 獲取當前時間
        time_from = session.start_time  # 直接使用 datetime 對象
        # 使用時間差計算
        duration = time_diff(time_from, time_to)
        session.stop_fishing()
        list=get_item(session.lake,duration)
        session.delete()
        #統計物品數量
        count_dict = {}
        for i in list:
            if i in count_dict:
                count_dict[i] += 1
            else:
                count_dict[i] = 1
        for key in count_dict:
            has_object=UserItem.objects.filter(user=request.user,item=key)
            if has_object:
                q=UserItem.objects.get(user=request.user,item=key).quantity
                UserItem.objects.filter(user=request.user,item=key).update(quantity=q+count_dict[key])
            else:
                UserItem.objects.create(
                    user=request.user,
                    item=key,
                    quantity=count_dict[key],
                )
            p=0.1 #扣體力的程度
            h=item.objects.get(name=key).weight*p
            PlayerProfile.objects.filter(name=request.user).update(health=PlayerProfile.objects.get(name=request.user).health-h)
            if PlayerProfile.objects.get(name=request.user).health<0:
                PlayerProfile.objects.get(name=request.user).delete()
                User.objects.get(username=request.user).delete()
                
                return render(request,'user/login.html',{"message":"你因筋疲力盡而死，請重新創建一個帳號!"})
        # 返回釣魚頁面，顯示結束信息
        return render(request, 'fishing/index.html', {'list':list,'duration':duration,'h':h,
            'message': f"{time_from.strftime('%Y/%m/%d %H:%M:%S')} 開始，{time_to.strftime('%Y/%m/%d %H:%M:%S')} 釣魚結束！",'message1':f'持續了{ duration }秒! 消耗了{h}體力!'
        })
    return redirect('fishing_view')