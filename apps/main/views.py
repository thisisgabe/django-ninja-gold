from django.shortcuts import render, redirect, HttpResponse
import datetime
import random


def build_data(session):
    data = {}
    # load the number of coins
    if 'number_coins' not in session:
        print('number_coins does not exist, creating...')
        session["number_coins"] = 0
        print(session["number_coins"])
    data["number_coins"] = session["number_coins"]
    # load the activity log
    if 'activity_log' not in session:
        print('activity_log does not exist, creating...')
        data["activity_log"] = []
        session["activity_log"] = []
    else:
        data["activity_log"] = reversed(session["activity_log"])
    # return the data
    return data


def add_to_log(session, string, color):
    d = datetime.datetime.today()
    value = string + ' ' + d.strftime("%B %d %Y %H:%M:%S")
    session["activity_log"].append({
        'color': color,
        'text': value
    })
    print('added to activity log')
    print(value)


def updateScore(request):
    if not request.POST["building_type"]:
        return
    switcher = {
        0: 'farm',
        1: 'cave',
        2: 'house',
        3: 'casino'
    }
    session = request.session
    building = switcher.get(int(request.POST["building_type"]), 'invalid')

    if building == 'farm':
        num = random.randrange(10, 21)
        session["number_coins"] += num
        add_to_log(
            session, f'visited the farm and acquired {num} coins. yay!!!', 'green')

    elif building == 'cave':
        num = random.randrange(5, 11)
        session["number_coins"] += num
        add_to_log(session, f'visited the cave and acquired {num} coins. yay!!!', 'green')
    elif building == 'house':
        num = random.randrange(2, 6)
        session["number_coins"] += num
        add_to_log(session, f'visited the house and acquired {num} coins. yay!!!', 'green')
    elif building == 'casino':
        num = random.randrange(-50, 51)
        session["number_coins"] += num
        if num > 0:
            add_to_log(session, f'visited the casino and acquired {num} coins. yay!!!', 'green')
        elif num < 0:
            add_to_log(session, f'visited the casino and got swindled for {num} coins. booo!!!', 'red')
        else:
            add_to_log(session, "we had water at the casino and came out even. ~~neutral-ness intensifies~~", '')
    else:
        add_to_log(session, 'what the heck just happened???', '')

# Create your views here.


def index(request):
    data = build_data(request.session)
    return render(request, "main/index.html", context=data)


def process_money(request):
    print('user submitted form')
    print(request.POST)
    updateScore(request)
    return redirect('/')


def destroy_session(request):
    print("destroying session")
    request.session.flush()
    return redirect('/')