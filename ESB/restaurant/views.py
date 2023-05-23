from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant, RestaurantCategory, Report, ReportType
from django.core.paginator import Paginator
import datetime
import plotly.graph_objs as go
from django.db.models import Sum
from dateutil.relativedelta import relativedelta


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
            'end_date': end_date,
            'graph': graph,
            'report_type': report_type_id
        }

    return render(request, 'restaurant/consolidated_report.html', context)

def week_report(request, report_type_id):
    user = request.user
    report_type = ReportType.objects.get(pk=report_type_id)
    accessible_restaurants = Restaurant.objects.filter(perm_grup_fo=user.access_rights)

    if report_type_id == 3:
        report_name = report_type.name_report
        if 'week' in request.GET and 'year' in request.GET and 'compare_week' in request.GET and 'compare_year' in request.GET:
            year = int(request.GET['year'])
            week_number = int(request.GET['week'])
            compare_year = int(request.GET['compare_year'])
            compare_week_number = int(request.GET['compare_week'])
            previous_year = year - 1
            #все переменные даты
            start_date = datetime.datetime.strptime(f'{year}-W{week_number}-1', "%G-W%V-%u").date()
            end_date = start_date + datetime.timedelta(days=6)
            previous_start_date = start_date.replace(year=previous_year)
            previous_end_date = end_date.replace(year=previous_year)
            compare_start_date = datetime.datetime.strptime(f'{compare_year}-W{compare_week_number}-1', "%G-W%V-%u").date()
            compare_end_date = compare_start_date + datetime.timedelta(days=6)
            start_date_from = datetime.date(start_date.year, start_date.month, 1)
            end_date_from = start_date_from + relativedelta(months=1, days=-1)
            end_date_from = min(end_date_from, end_date)
            previous_start_date_from = datetime.date(previous_start_date.year, previous_start_date.month, 1)
            previous_end_date_from = previous_start_date_from + relativedelta(months=1, days=-1)
            previous_end_date_from = min(previous_end_date_from, previous_end_date)
            days_from_start = (end_date_from - start_date_from).days+1
            print(days_from_start)
            #вытаскивания данных по датам
            report_data = Report.objects.filter(
                department__in=accessible_restaurants,
                data__range=(start_date, end_date),
                department__isnull=False
            ).values('department__category__name', 'department__name', 'department__city').annotate(
                revenue_selected_week=Sum('revenue')
            ).order_by('department__category', 'department')

            compare_report_data = Report.objects.filter(
                department__in=accessible_restaurants,
                data__range=(compare_start_date, compare_end_date),
                department__isnull=False
            ).values('department__category__name', 'department__name', 'department__city').annotate(
                compare_revenue_selected_week=Sum('revenue')
            ).order_by('department__category', 'department')
            previous_year_data = Report.objects.filter(
                department__in=accessible_restaurants,
                data__range=(previous_start_date, previous_end_date),
                department__isnull=False
            ).values('department__category__name', 'department__name', 'department__city').annotate(
                revenue_for_last_year=Sum('revenue')
            ).order_by('department__category', 'department')
            departments_with_revenue = {(item['department__name'], item['department__city']) for item in previous_year_data}
            # Преобразование Decimal во float
            previous_year_data = [
                {
                    'department__category__name': item['department__category__name'],
                    'department__name': item['department__name'],
                    'department__city': item['department__city'],
                    'revenue_for_last_year': float(item['revenue_for_last_year'] or 0),
                }
                for item in previous_year_data
            ]
            # Добавление нулевых значений для ресторанов без данных о доходах за прошлый год
            departments_without_revenue = {(item['department__name'], item['department__city']) for item in report_data} - departments_with_revenue
            for department in departments_without_revenue:
                previous_year_data.append({
                    'department__category__name': '',
                    'department__name': department[0],
                    'department__city': department[1],
                    'revenue_for_last_year': 0.0,
                })
            report_data_from = Report.objects.filter(
                department__in=accessible_restaurants,
                data__range=(start_date_from,end_date_from),
                department__isnull=False
            ).values('department__category__name', 'department__name', 'department__city').annotate(
                revenue_from=Sum('revenue')
            ).order_by('department__category', 'department')
            previous_report_data_from = Report.objects.filter(
                department__in=accessible_restaurants,
                data__range=(previous_start_date_from, previous_end_date_from),
                department__isnull=False
            ).values('department__category__name', 'department__name', 'department__city').annotate(
                previous_revenue_from=Sum('revenue')
            ).order_by('department__category', 'department')

            departments_with_revenue_from = {(item['department__name'], item['department__city']) for item in previous_report_data_from}

            previous_report_data_from = [
                {
                    'department__category__name': item['department__category__name'],
                    'department__name': item['department__name'],
                    'department__city': item['department__city'],
                    'previous_revenue_from': float(item['previous_revenue_from'] or 0),
                }
                for item in previous_report_data_from
            ]

            departments_without_revenue_from = {(item['department__name'], item['department__city']) for item in report_data} - departments_with_revenue_from
            for department in departments_without_revenue_from:
                previous_report_data_from.append({
                    'department__category__name': '',
                    'department__name': department[0],
                    'department__city': department[1],
                    'previous_revenue_from': 0.0,
                })
            context = {
                'report_name': report_name,
                'report_data': report_data,
                'compare_report_data': compare_report_data,
                'previous_year_data': previous_year_data,
                'current_year': year,
                'current_week': week_number,
                'compare_year': compare_year,
                'compare_week': compare_week_number,
                'report_type_id': report_type_id,
                'report_data_from':report_data_from,
                'previous_report_data_from':previous_report_data_from,
                'first_day_number':start_date_from,
                'end_day_number':days_from_start,
            }

            return render(request, 'restaurant/week_results.html', context)

    # Handle case when parameters are missing or invalid
    report_data = None
    compare_report_data = None
    previous_year_data = None
    context = {
        'title': 'NRG',
        'report_name': report_name,
        'report_data': report_data,
        'compare_report_data': compare_report_data,
        'previous_year_data': previous_year_data,
        'current_year': None,
        'current_week': None,
        'compare_year': None,
        'compare_week': None,
        'report_type_id': report_type_id,
        'report_data_from':None,
        'previous_report_data_from':None,
        'first_day_number':None,
        'end_day_number':None,
    }

    return render(request, 'restaurant/week_results.html', context)


def mounth_report(request, report_type_id):
    user = request.user
    report_type = ReportType.objects.get(pk=report_type_id)
    accessible_restaurants = Restaurant.objects.filter(
        perm_grup_fo=user.access_rights)
    if report_type_id == 2:
        report_name = report_type.name_report
        if 'month' in request.GET and 'year' in request.GET and 'compare_month' in request.GET and 'compare_year' in request.GET:
            # если переданы месяц и год, то фильтруем данные за этот месяц и год
            current_month = int(request.GET['month'])
            current_year = int(request.GET['year'])
            compare_month = int(request.GET['compare_month'])
            compare_year = int(request.GET['compare_year'])

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

            compare_report_data = Report.objects.filter(
                department__in=accessible_restaurants,  # filter by accessible restaurants
                data__year=compare_year,
                data__month=compare_month,
                department__isnull=False
            ).select_related('department').values('department__name', 'department__city').annotate(
                compare_revenue=Sum('revenue'),
                compare_cost_price=Sum('cost_price'),
                compare_number_of_checks=Sum('number_of_checks')
            ).order_by('department')
        else:
            report_data = None
            compare_report_data = None
            current_month = None
            current_year = None
            compare_month = None
            compare_year = None

        context = {
            'title': 'NRG',
            'report_name': report_name,
            'report_data': report_data,
            'compare_report_data': compare_report_data,
            'current_month': current_month,
            'current_year': current_year,
            'compare_month': compare_month,
            'compare_year': compare_year,
            'report_type_id': report_type_id,
        }

        return render(request, 'restaurant/mounth_results.html', context)
