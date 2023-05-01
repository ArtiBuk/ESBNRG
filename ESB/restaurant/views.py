from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant, RestaurantCategory, Report, ReportType
from django.db.models import Q
from django.core.paginator import Paginator
import datetime
import plotly.graph_objs as go
from django.db.models import Sum
from django.db.models import F


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


def report(request, restaurant_id, report_type_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    report_type = ReportType.objects.get(pk=report_type_id)

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
            'report_type': report_type_id
        }
    if report_type_id == 2:
        return ()
    return render(request, 'restaurant/report.html', context)

def report_week_and_mounth(request, report_type_id):
    report_type = ReportType.objects.get(pk=report_type_id)
    print(report_type_id)
    if report_type_id == 2:
        report_name = report_type.name_report
        if 'month' in request.GET and 'year' in request.GET:
            # если переданы месяц и год, то фильтруем данные за этот месяц и год
            current_month = int(request.GET['month'])
            current_year = int(request.GET['year'])
            
            report_data = Report.objects.filter(
                data__year=current_year,
                data__month=current_month,
                department__isnull=False
            ).select_related('department').values('department__name','department__city').annotate(
                revenue=Sum('revenue'),
                cost_price=Sum('cost_price'),
                number_of_checks=Sum('number_of_checks')
            ).order_by('department')
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
            'report_type_id':report_type_id
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
                data__gte=start_date,
                data__lte=end_date,
                department__isnull=False
            ).select_related('department').values('department__name','department__city').annotate(
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
            'report_type_id':report_type_id
        }

        return render(request, 'restaurant/week_mounth_results.html', context)
    else:
        report_name = None
        report_data = None
        context = {
            'title': 'NRG',
            'report_name': report_name,
            'report_data': report_data,
            'current_month': None,
            'current_year': None
        }
        
    return render(request, 'restaurant/week_mounth_results.html', context)

# def report_week_and_mounth(request, report_type_id):
#     report_type = ReportType.objects.get(pk=report_type_id)
#     if report_type_id == 2:
#         report_name = report_type.name_report
#         if 'month' in request.GET and 'year' in request.GET:
#             # если переданы месяц и год, то фильтруем данные за этот месяц и год
#             current_month = int(request.GET['month'])
#             current_year = int(request.GET['year'])
            
#             if 'week' in request.GET and 'year' in request.GET:
#                 # если переданы номер недели и год, то фильтруем данные за эту неделю
#                 year = int(request.GET['year'])
#                 week_number = int(request.GET['week'])
#                 start_date = datetime.datetime.strptime(
#                     f'{year}-W{week_number}-1', "%G-W%V-%u").date()
#                 end_date = start_date + datetime.timedelta(days=6)
                
#                 report_data = Report.objects.filter(
#                     data__year=current_year,
#                     data__month=current_month
#                 ).select_related('department').values('department').annotate(
#                     revenue=Sum('revenue'),
#                     cost_price=Sum('cost_price'),
#                     number_of_checks=Sum('number_of_checks')
#                 ).order_by('department')
#             else:
#                 report_data = Report.objects.filter(
#                     data__year=current_year,
#                     data__month=current_month,
#                     department__isnull=False
#                 ).select_related('department').values('department').annotate(
#                     revenue=Sum('revenue'),
#                     cost_price=Sum('cost_price'),
#                     number_of_checks=Sum('number_of_checks')
#                 ).order_by('department')
#         else:
#             report_data = None
#             current_month = None
#             current_year = None
            
#         context = {
#             'title': 'NRG',
#             'report_name': report_name,
#             'report_data': report_data,
#             'current_month': current_month,
#             'current_year': current_year
#         }

#         return render(request, 'restaurant/week_mounth_results.html', context)
#     elif report_type_id == 3:
#         report_name = report_type.name_report
#         # Add logic for report_type_id == 3
#         report_data = None
        
#         context = {
#             'title': 'NRG',
#             'report_name': report_name,
#             'report_data': report_data,
#             'current_month': None,
#             'current_year': None
#         }

#         return render(request, 'restaurant/week_mounth_results.html', context)
#     else:
#         report_name = None
#         report_data = None
#     return render(request, 'restaurant/week_mounth_results.html', context)
