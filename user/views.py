from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from fishing.models import PlayerProfile


def user_register(request):
    message = ""
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 保存新用戶並返回該用戶的實例
            user = form.save()  # 這裡會返回一個 User 實例
            # 創建對應的 PlayerProfile
            PlayerProfile.objects.create(
                name=user,  # 使用 User 實例
                health=10000,
                money=0,
            )
            message = "註冊成功!"
            return redirect("login")  # 註冊成功後跳轉到登入頁面
        else:
            message = "註冊失敗，請檢查輸入信息。"
    return render(request, "user/register.html", {"form": form, "message": message})


def user_login(request):
    message = ""
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("profile")  # 登入成功後跳轉到個人頁面
        else:
            message = "帳號或密碼錯誤!"

    form = AuthenticationForm()
    return render(request, "user/login.html", {"form": form, "message": message})


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect("login")  # 未登入的用戶無法訪問個人頁面
    session=PlayerProfile.objects.get(name=request.user)
    health=session.health
    money=session.money
    return render(request, "user/profile.html",{"health":health,"money":money})


def user_logout(request):
    logout(request)
    return redirect("login")

def user_story(request):
    return render(request, "user/story.html")

def user_text(request):
    return render(request, "user/text.html")


def BubbleSort(data):
    n = len(data)
    while n > 1:
        n-=1
        for i in range(n):        
            if data[i][1] < data[i+1][1]:  #比較money
                data[i], data[i+1] = data[i+1], data[i]
    return data

def user_rank(request):
    player_list=[]
    all_player=PlayerProfile.objects.all()
    for player in all_player:
        player_list.append([str(player.name),player.money])
    rank_list=BubbleSort(player_list)
    rank=[]
    for i in range(len(rank_list)):
        if i>30: #顯示前面幾位
            break
        rank.append([i+1,rank_list[i][0],rank_list[i][1]])
    return render(request, "user/rank.html", {"rank": rank})

