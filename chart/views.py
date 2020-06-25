# chart/views.py
from django.shortcuts import render
from .models import Passenger
from django.db.models import Count, Q
import json



def home(request):
    return render(request, 'home.html')

def ticket_class_view_3(request):
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    dataset_2 = Passenger.objects \
        .values('ticket_class') \
        .annotate(
        survived_count=Count('ticket_class', filter=Q(survived=True)),
        not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    survival_rate_series_data = list()

    for d in dataset_2:
        ticket_class = d['ticket_class']
        rate = d['survived_count'] \
            / (d['survived_count'] + d['not_survived_count']) * 100.0
        f_rate = float(f'{rate:.1f}')
        survival_rate_series_data.append(f_rate)

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()                 # for xAxis
    survived_series_data = list()       # for series named 'Survived'
    not_survived_series_data = list()   # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s 등석' % entry['ticket_class'])         # for xAxis
        survived_series_data.append(entry['survived_count'])          # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'

    survived_series = {
        'name': '생존',
        'type': 'column',
        'data': survived_series_data,
        'tooltip': {'valueSuffix': '명'},
        'color': 'green'
    }
    not_survived_series = {
        'name': '비생존',
        'type': 'column',
        'data': not_survived_series_data,
        'tooltip': {'valueSuffix': '명'},
        'color': 'red'
    }
    survival_rate_series = {
        'name': '생존율',
        'type': 'spline',
        'yAxis': 1,
        'data': survival_rate_series_data,
        'tooltip': {'valueSuffix': '%'},
        'color': 'blue'
    }

    chart = {
        'chart': {'zoomType': 'xy'},
        'title': {'text': '좌석 등급에 따른 타이타닉 생존/비생존 인원 및 생존율'},
        'xAxis': {'categories': categories},
        'yAxis': [{'labels': {'format': '{value}명'}, 'title': {'text': '인원'}},
                  {'title': {'text': '생존율'}, 'labels': {'format': '{value}%'}, 'tickInterval': 10, 'opposite': 'true'}],
        'tooltip': {'shared': 'true'},
        'series': [survived_series, not_survived_series, survival_rate_series]
    }
    dump = json.dumps(chart)

    return render(request, 'ticket_class_3.html', {'chart': dump})