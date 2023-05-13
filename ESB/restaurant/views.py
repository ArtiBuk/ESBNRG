from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant, RestaurantCategory, Report, ReportType
from django.db.models import Q
from django.core.paginator import Paginator
import datetime
import plotly.graph_objs as go
from django.db.models import Sum
from django.db.models import F
from decimal import Decimal


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

    report_types = ReportType.objects.all()

    paginator = Paginator(restaurants, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update({
        'restaurant': page_obj,
        'report_types': report_types,  # Добавляем список видов отчетов в контекст
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
            report_types = ReportType.objects.all()
            context = {
                'results': results,
                'report_types': report_types,
            }
            return render(request, 'restaurant/search.html', context)
        else:
            return render(request, 'restaurant/search.html', {'results': []})


def generate_graph(report_data, selected_restaurants):
    # формируем данные для каждого месяца
    data = {}
    for r in report_data:
        month = r.data.month
        if month not in data:
            data[month] = {'dates': [], 'revenues': [], 'restaurant': []}
        data[month]['dates'].append(r.data)
        data[month]['revenues'].append(r.revenue)
        data[month]['restaurant'].append(
            (r.department.name, r.department.city))  # изменено

    # Создаем объект для построения графика
    fig = go.Figure()

    # Добавляем данные на график для каждого месяца и ресторана
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'pink', 'brown', 'gray', 'olive', 'teal',
              'navy', 'maroon', 'lime', 'aqua', 'silver', 'fuchsia', 'black', 'yellow', 'coral', 'indigo']
    i = 0
    for month, d in data.items():
        for restaurant in selected_restaurants:
            restaurant_data = [revenue for revenue, (name, city) in zip(
                d['revenues'], d['restaurant']) if name == restaurant.name and city == restaurant.city]  # изменено
            fig.add_trace(go.Scatter(x=d['dates'], y=restaurant_data,
                                     mode='lines+markers', name=f'Выручка за {d["dates"][0].strftime("%B")} ({restaurant.name} | {restaurant.city})',
                                     line=dict(color=colors[i % len(colors)]),
                                     marker=dict(color=colors[i % len(colors)], size=8)))
            i += 1

    # Настраиваем внешний вид графика
    fig.update_layout(
        title='Выручка за период',
        xaxis=dict(
            title='Дата',
            tickangle=-45,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Выручка, руб.',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        legend=dict(
            x=1.02,  # Adjust the x-coordinate to position the legend on the right side
            y=1.0,   # Adjust the y-coordinate if needed
            orientation='v',  # Set the orientation to vertical
            bgcolor='rgba(0,0,0,0)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig.to_html(full_html=False, config={'displayModeBar': False})


@login_required  # Requires user authentication
def consolidated_report(request, report_type_id):
    # Get the restaurants that the user has permission to access
    user = request.user
    restaurants = Restaurant.objects.filter(perm_grup_fo=user.access_rights)

    if report_type_id == 1:
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

        restaurant_ids = request.GET.getlist('restaurant_ids')
        selected_restaurants = restaurants.filter(id__in=restaurant_ids)

        # получаем данные из модели Report за выбранный период для выбранных ресторанов
        report_data = Report.objects.filter(
            department__in=selected_restaurants, data__range=[start_date, end_date])
        graph = generate_graph(report_data, selected_restaurants)

        # создаем контекст для передачи данных в шаблон
        context = {
            'title': 'Сводный отчет по ресторанам',
            'restaurants': restaurants,
            'selected_restaurants': selected_restaurants,
            'report_data': report_data,
            'start_date': start_date,
            'end_date': end_date - datetime.timedelta(days=1),
            'graph': graph,
            'report_type': report_type_id
        }

    return render(request, 'restaurant/consolidated_report.html', context)


def report_week_and_mounth(request, report_type_id):
    user = request.user
    report_type = ReportType.objects.get(pk=report_type_id)
    accessible_restaurants = Restaurant.objects.filter(perm_grup_fo=user.access_rights)

    print(report_type_id)
    if report_type_id == 2:
        report_name = report_type.name_report
        if 'month' in request.GET and 'year' in request.GET:
            # если переданы месяц и год, то фильтруем данные за этот месяц и год
            current_month = int(request.GET['month'])
            current_year = int(request.GET['year'])

            report_data = Report.objects.filter(
                department__in=accessible_restaurants,  # filter by accessible restaurants
                data__year=current_year,
                data__month=current_month,
                department__isnull=False
            ).select_related('department').values('department__name', 'department__city').annotate(
                revenue=Sum('revenue'),
                cost_price=Sum('cost_price'),
                number_of_checks=Sum('number_of_checks')
            ).order_by('department')

            for i, data in enumerate(report_data):
                revenue = data['revenue']
                fact_value = request.POST.get(f'fact_value_{i+1}', 1) or 1
                deviation = (revenue / Decimal(fact_value) -
                             1) if float(fact_value) else 0
                data['deviation'] = deviation
        else:
            report_data = None
            current_month = None
            current_year = None

        context = {
            'title': 'NRG',
            'report_name': report_name,
            'report_data': report_data,
            'current_month': current_month,
            'current_year': current_year,
            'report_type_id': report_type_id,
        }

        return render(request, 'restaurant/week_mounth_results.html', context)

    elif report_type_id == 3:
        report_name = report_type.name_report
        if 'week' in request.GET and 'year' in request.GET:
            # если переданы номер недели и год, то фильтруем данные за эту неделю
            year = int(request.GET['year'])
            week_number = int(request.GET['week'])
            start_date = datetime.datetime.strptime(
                f'{year}-W{week_number}-1', "%G-W%V-%u").date()
            end_date = start_date + datetime.timedelta(days=6)

            report_data = Report.objects.filter(
                department__in=accessible_restaurants,  # filter by accessible restaurants
                data__gte=start_date,
                data__lte=end_date,
                department__isnull=False
            ).select_related('department').values('department__name', 'department__city').annotate(
                revenue=Sum('revenue'),
                cost_price=Sum('cost_price'),
                number_of_checks=Sum('number_of_checks')
            ).order_by('department')
        else:
            report_data = None

        context = {
            'title': 'NRG',
            'report_name': report_name,
            'report_data': report_data,
            'current_month': None,
            'current_year': None,
            'report_type_id': report_type_id,
        }

        return render(request, 'restaurant/week_mounth_results.html', context)

    return render(request, 'restaurant/week_mounth_results.html', context)
