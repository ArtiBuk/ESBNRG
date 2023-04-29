from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant, RestaurantCategory, Report, ReportType
from django.db.models import Q
from django.core.paginator import Paginator
import datetime
import plotly.graph_objs as go


def index(request):
    context = {
        'title': 'NRG'
    }
    return render(request, 'restaurant/index.html', context)


@login_required
def restaurant(request, category_id=None):
    user = request.user
    # Получаем доступные для пользователя категории ресторанов
    categories = RestaurantCategory.objects.filter(
        perm_grup_for_category=user.access_rights)
    context = {
        'title': 'restaurant',
        'categories': categories,
    }
    # Фильтруем рестораны, принадлежащие выбранной категории и доступные для пользователя
    if category_id:
        restaurants = Restaurant.objects.filter(
            category_id=category_id, perm_grup_fo=user.access_rights)
    # Если категория не выбрана, выводим все доступные рестораны для пользователя
    else:
        restaurants = Restaurant.objects.filter(
            perm_grup_fo=user.access_rights)

    paginator = Paginator(restaurants, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update({
        'restaurant': page_obj,
    })
    return render(request, 'restaurant/restaurant.html', context)


@login_required
def search_restaurant(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            results = Restaurant.objects.filter(
                name__icontains=query,
                perm_grup_fo=request.user.access_rights
            )
        else:
            results = []
        return render(request, 'restaurant/search.html', {'results': results})


def generate_graph(report_data):
    # формируем данные для каждого месяца
    data = {}
    for r in report_data:
        month = r.data.month
        if month not in data:
            data[month] = {'dates': [], 'revenues': []}
        data[month]['dates'].append(r.data)
        data[month]['revenues'].append(r.revenue)

    # Создаем объект для построения графика
    fig = go.Figure()

    # Добавляем данные на график для каждого месяца
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'pink']
    i = 0
    for month, d in data.items():
        fig.add_trace(go.Scatter(x=d['dates'], y=d['revenues'],
                                 mode='lines+markers', name=f'Выручка за {d["dates"][0].strftime("%B")}',
                                 line=dict(color=colors[i % len(colors)])))
        i += 1

    # Настраиваем внешний вид графика
    fig.update_layout(
        title='Выручка за период',
        xaxis_title='Дата',
        yaxis_title='Выручка, руб.',
        xaxis_tickangle=-45,
        showlegend=True
    )

    return fig.to_html(full_html=False)

def report(request, restaurant_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)

    # по умолчанию отчет за последнюю неделю
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)

    if request.GET.get('start_date') and request.GET.get('end_date') and not request.GET.get('week') and not request.GET.get('year'):
        # если переданы start_date и end_date, то фильтруем данные по этим датам
        start_date = datetime.datetime.strptime(
            request.GET['start_date'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(
            request.GET['end_date'], '%Y-%m-%d').date()
    elif request.GET.get('week') and request.GET.get('year'):
        # если передан год и номер недели, то фильтруем данные за эту неделю
        year = int(request.GET['year'])
        week_number = int(request.GET['week'])
        start_date = datetime.datetime.strptime(
            f'{year}-W{week_number}-1', "%G-W%V-%u").date()
        end_date = start_date + datetime.timedelta(days=6)

    # получаем данные из модели Report за выбранный период для выбранного ресторана
    report_data = Report.objects.filter(
        department=restaurant, data__range=[start_date, end_date])
    graph = generate_graph(report_data)

    # создаем контекст для передачи данных в шаблон
    context = {
        'title': restaurant.name,
        'category': restaurant.category,
        'city': restaurant.city,
        'address': restaurant.adress,
        'report_data': report_data,
        'start_date': start_date,
        # вычитаем 1 день, чтобы отобразить правильную конечную дату
        'end_date': end_date - datetime.timedelta(days=1),
        'graph': graph,
    }
    return render(request, 'restaurant/report.html', context)