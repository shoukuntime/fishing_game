from django.shortcuts import render
from fishing.models import UserItem,item,PlayerProfile
# Create your views here.
def items_index(request):
    items = []
    objects = UserItem.objects.filter(user=request.user)
    for obj in objects:
        i=item.objects.get(name=obj.item)
        describe=i.describe
        items.append([obj.item,obj.quantity,describe])
    return render(request, "items/index.html", {"items": items})

def sell_item_view(request):
    # 取得用戶擁有的物品，並且只列出 category 為 'money' 的物品
    user_items = UserItem.objects.filter(user=request.user)
    sellable_items = []

    # 只列出 category 為 'money' 的物品
    for user_item in user_items:
        item_data = item.objects.filter(name=user_item.item).first()
        if item_data and item_data.category == 'money':
            sellable_items.append(user_item)
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        quantity_to_sell = int(request.POST.get('quantity_to_sell'))

        # 查找用戶擁有的物品以及該物品的詳細數據
        user_item = UserItem.objects.filter(user=request.user, item=item_name).first()
        item_data = item.objects.filter(name=item_name).first()

        if user_item and item_data:
            if user_item.quantity >= quantity_to_sell:
                user_item.sell_item(quantity_to_sell, item_data.value)
                message = f"你賣掉了 {quantity_to_sell} 個 {item_name}，賺取了 {quantity_to_sell * item_data.value} 金幣。"
            else:
                message = "你沒有足夠的物品來賣。"
        else:
            message = "物品不存在。"
        return render(request, 'items/sell.html', {'message': message, 'sellable_items': sellable_items})
    return render(request, 'items/sell.html', {'sellable_items': sellable_items})

def eat_food_view(request):
    if request.method == 'POST':
        item_name = request.POST.get('item')
        quantity_to_eat = int(request.POST.get('quantity', 1))  # 玩家選擇吃的數量，預設為1

        # 找到該玩家的物品和玩家配置檔
        user_item = UserItem.objects.get(user=request.user, item=item_name)
        food_item = item.objects.get(name=item_name)
        player_profile = PlayerProfile.objects.get(name=request.user)

        if food_item.category == 'health' and user_item.quantity >= quantity_to_eat:
            # 計算增加後的體力，並考慮最大值 10000
            health_increase = food_item.value * quantity_to_eat
            new_health = player_profile.health + health_increase
            if new_health > 10000:
                health_increase = 10000 - player_profile.health
                new_health = 10000  # 設定體力為最大值

            # 更新玩家體力
            player_profile.health = new_health
            player_profile.save()

            # 減少玩家的物品數量
            user_item.quantity -= quantity_to_eat
            if user_item.quantity == 0:
                user_item.delete()  # 如果物品數量變為0，則刪除該物品
            else:
                user_item.save()
                user_items = UserItem.objects.filter(user=request.user)
                food_items = [user_item for user_item in user_items if item.objects.get(name=user_item.item).category == 'health']
            return render(request, 'items/eat_food.html', {
                'message': f'已吃掉 {quantity_to_eat} 個 {item_name}，恢復了 {health_increase} 體力，當前體力為 {new_health}！','food_items': food_items
            })
        else:
            user_items = UserItem.objects.filter(user=request.user)
            food_items = [user_item for user_item in user_items if item.objects.get(name=user_item.item).category == 'health']
            return render(request, 'items/eat_food.html', {'message': '你沒有足夠的食物或這不是食物類別！','food_items': food_items})

    # 顯示玩家擁有的食物
    user_items = UserItem.objects.filter(user=request.user)
    food_items = [user_item for user_item in user_items if item.objects.get(name=user_item.item).category == 'health']
    return render(request, 'items/eat_food.html', {'food_items': food_items})