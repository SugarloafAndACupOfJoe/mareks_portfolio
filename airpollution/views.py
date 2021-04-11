from django.contrib import messages
from django.db.models import Max, Min, Sum, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django import forms
import openpyxl
import json

from airpollution.models import Pollutant, Country, PollutantEntry
from airpollution.helpers import get_headers_and_units, XLHEADERS


class ExcelUploadForm(forms.Form):
    year = forms.CharField(max_length=4)
    file = forms.FileField()


def upload(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            year = form.cleaned_data['year']
            file = form.cleaned_data['file']
            wb = openpyxl.load_workbook(filename=file, read_only=False)
            tab_names = wb.get_sheet_names()
            for tab_name in tab_names:
                ws = wb[tab_name]
                pollutant_name = tab_name.split('_')[0].strip()
                pollutant = Pollutant.objects.get_or_create(name=pollutant_name)
                if pollutant[0].limit_value is None:
                    limit_value = int(ws['A'][2].value.split()[-2])
                    pollutant[0].limit_value = limit_value
                    pollutant[0].save()
                headers_row, headers, units = get_headers_and_units(ws)

                # Save all entries to database
                to_insert = []
                for i, row in enumerate(ws.rows):
                    if i <= headers_row:  # Skip to actual entries
                        continue

                    country = row[headers[XLHEADERS.COUNTRY]].value
                    if country is None:
                        break
                    if len(country) > 2:
                        country_object = Country.objects.filter(name=country).first()
                    else:
                        country_object = Country.objects.get(pk=country)

                    city = row[headers[XLHEADERS.CITY]].value
                    station_name = row[headers[XLHEADERS.STATION_NAME]].value
                    station_area = row[headers[XLHEADERS.AREA]].value

                    data = {
                        'pollutant': pollutant[0],
                        'country': country_object,
                        'year': year,
                        'city': city if city else '',
                        'station_code': row[headers[XLHEADERS.STATION_EOI_CODE]].value,
                        'station_name': station_name if station_name else '',
                        'pollution_level': row[headers[XLHEADERS.AIR_POLLUTION_LEVEL]].value,
                        'units': units,
                        'station_type': row[headers[XLHEADERS.TYPE]].value,
                        'station_area': station_area if station_area else '',
                        'longitude': row[headers[XLHEADERS.LONGITUDE]].value,
                        'latitude': row[headers[XLHEADERS.LATITUDE]].value,
                        'altitude': row[headers[XLHEADERS.ALTITUDE]].value,
                    }
                    to_insert.append(PollutantEntry(**data))

                PollutantEntry.objects.filter(year=year, pollutant=pollutant[0]).delete()
                PollutantEntry.objects.bulk_create(to_insert)
        messages.success(request, 'File uploaded successfully!')
    else:
        return HttpResponse('This view only handles GET and POST requests')

    return render(request, 'airpollution/upload.html')


def table(request):
    return render(request, 'airpollution/table.html')


def charts(request):
    context = {
        'pollutant_list': [p.name for p in Pollutant.objects.all()]
    }
    return render(request, 'airpollution/charts.html', context)


def airpollution_table_data(request):
    table_data = {}
    pollutant_list = [pollutant for pollutant in Pollutant.objects.all()]
    country_list = [country for country in Country.objects.all()]
    for pollutant in pollutant_list:
        table_data[pollutant.name] = {}

        for i, country in enumerate(country_list):
            total = PollutantEntry.objects \
                .aggregate(total=Sum('pollution_level', filter=Q(pollutant=pollutant,
                                                                 country=country)))['total']
            minimum = PollutantEntry.objects \
                .aggregate(min=Min('pollution_level', filter=Q(pollutant=pollutant,
                                                               country=country)))['min']
            maximum = PollutantEntry.objects \
                .aggregate(max=Max('pollution_level', filter=Q(pollutant=pollutant,
                                                               country=country)))['max']
            count = PollutantEntry.objects.filter(pollutant=pollutant, country=country).count()
            units = PollutantEntry.objects.filter(pollutant=pollutant, country=country).first()
            units = units.units if units else ''
            if total is not None and count:
                table_data[pollutant.name][country.iso_code] = {'avg': total / count, 'min': minimum,
                                                                'max': maximum,
                                                                'limit': pollutant.limit_value, 'units': units}
    return JsonResponse(table_data)


def airpollution_visual_data1(request):
    visuals_data = {
        'Pollution Levels by Pollutant by Country': {
            'chart_type': 'chart1',
            'labels': [],
            'datasets': [
                {'label': 'Limit',
                 'backgroundColor': '#3C9C85',
                 'stack': 'limit',
                 'data': []}
            ]
        },

    }
    pollutant_list = [pollutant for pollutant in Pollutant.objects.all()]
    country_list = [country for country in Country.objects.all()]
    visuals_data['Pollution Levels by Pollutant by Country']['datasets'] += \
        [{'label': c.name, 'backgroundColor': c.color, 'hidden': 'true', 'data': []} for c in country_list]

    for pollutant in pollutant_list:
        visuals_data['Pollution Levels by Pollutant by Country']['labels'].append(pollutant.name)
        visuals_data['Pollution Levels by Pollutant by Country']['datasets'][0]['data'] \
            .append(pollutant.limit_value)
        for i, country in enumerate(country_list):
            total = PollutantEntry.objects \
                .aggregate(total=Sum('pollution_level', filter=Q(pollutant=pollutant,
                                                                 country=country)))['total']

            count = PollutantEntry.objects.filter(pollutant=pollutant, country=country).count()
            if total is not None and count:
                visuals_data['Pollution Levels by Pollutant by Country']['datasets'][i + 1]['data'] \
                    .append(round(total / count, 2))
            else:
                visuals_data['Pollution Levels by Pollutant by Country']['datasets'][i + 1]['data'].append(-1)
    return JsonResponse(visuals_data)


def airpollution_visual_data2(request):
    pollutant_name = request.GET.get('pollutant', 'PM10')
    pollutant = Pollutant.objects.get(name=pollutant_name)
    summary_type = request.GET.get('summary_type', 'max')
    if summary_type == 'avg':
        name_prefix = 'Average'
    elif summary_type == 'min':
        name_prefix = 'Minimum'
    else:  # by default -> max
        name_prefix = 'Maximum'
    all_years = [pe['year'] for pe in PollutantEntry.objects.order_by('year').values('year').distinct()]
    all_countries = list(Country.objects.all())
    all_pollutants = [p.name for p in Pollutant.objects.all()]
    visuals_data = {
        'name': f'{name_prefix} pollution level by country over time',
        'labels': all_years,
        'datasets': [
            {'label': 'Limit',
             'backgroundColor': '#3C9C85',
             'borderColor': '#3C9C85',
             'data': [pollutant.limit_value] * len(all_years),
             'fill': False,
             },
        ]
    }

    for country in all_countries:
        country_data = {'label': country.name,
                        'backgroundColor': country.color,
                        'borderColor': country.color,
                        'data': [],
                        'fill': False,
                        'hidden': True}
        visuals_data['datasets'].append(country_data)
        for year in all_years:
            f = Q(pollutant=pollutant, year=year, country=country)
            if summary_type == 'avg':
                country_tot = PollutantEntry.objects.aggregate(s=Sum('pollution_level', filter=f))['s']
                country_count = PollutantEntry.objects.filter(f).count()
                country_data['data'].append(country_tot / country_count if country_count else 0)
            elif summary_type == 'min':
                country_min = PollutantEntry.objects.aggregate(s=Min('pollution_level', filter=f))['s']
                country_data['data'].append(country_min if country_min else 0)
            else:  # by default -> max
                country_max = PollutantEntry.objects.aggregate(s=Max('pollution_level', filter=f))['s']
                country_data['data'].append(country_max if country_max else 0)

    return JsonResponse(visuals_data)


def temp_country_creator(request):
    countries = {
        'Albania': ['AL', '#f60a0a'],
        'Andorra': ['AD', '#2019c0'],
        'Austria': ['AT', '#a81b1b'],
        'Belgium': ['BE', '#000000'],
        'Bosnia and Herzegovina': ['BA', '#ffd200'],
        'Bulgaria': ['BG', '#468650'],
        'Croatia': ['HR', '#21248a'],
        'Cyprus': ['CY', '#ff7a00'],
        'Czech Republic': ['CZ', '#dfdfdf'],
        'Denmark': ['DK', '#b60000'],
        'Estonia': ['EE', '#2f8ebc'],
        'Finland': ['FI', '#011d92'],
        'France': ['FR', '#dfdfdf'],
        'Germany': ['DE', '#e0be1d'],
        'Greece': ['GR', '#0b66aa'],
        'Hungary': ['HU', '#295934'],
        'Iceland': ['IS', '#2933d9'],
        'Ireland': ['IE', '#00d614'],
        'Italy': ['IT', '#c30000'],
        'Kosovo under UNSCR 1244/99': ['XK', '#354dcb'],
        'Latvia': ['LV', '#762424'],
        'Lithuania': ['LT', '#ffc000'],
        'Luxembourg': ['LU', '#6dc0f6'],
        'Malta': ['MT', '#dfdfdf'],
        'Montenegro': ['ME', '#a07900'],
        'Netherlands': ['NL', '#ff6000'],
        'Norway': ['NO', '#ff0000'],
        'Poland': ['PL', '#ffbcbc'],
        'Portugal': ['PT', '#064a00'],
        'Romania': ['RO', '#201b82'],
        'Serbia': ['RS', '#3d2269'],
        'Slovakia': ['SK', '#294bff'],
        'Slovenia': ['SI', '#ff3333'],
        'Spain': ['ES', '#f6a900'],
        'Sweden': ['SE', '#3c73d3'],
        'Switzerland': ['CH', '#cf3535'],
        'The former Yugoslav Republic of Macedonia': ['MK', '#ecc615'],
        'Turkey': ['TR', '#c82727'],
        'United Kingdom': ['GB', '#071260'],
    }

    to_insert = []
    for country_name, data in countries.items():
        to_insert.append(Country(iso_code=data[0], name=country_name, color=data[1]))

    if request.GET.get('update', '') == 'true':
        Country.objects.bulk_update(to_insert, ['color'])
    else:
        Country.objects.bulk_create(to_insert)

    return redirect('airpollution:upload')


def temp_add_colors_to_pollutants(request):
    try:
        pollutants = ['PM2.5', 'PM10', 'NO2', 'O3', 'BaP', 'SO2']
        colors = ['#dc5c5c', '#dc5cdb', '#5c63dc', '#5cdadc', '#66dc5c', '#dcdb5c']
        to_insert = [Pollutant(name=pollutant, color=colors[i]) for i, pollutant in enumerate(pollutants)]
        Pollutant.objects.bulk_update(to_insert, ['color'])
        messages.success(request, 'Colors added successfully!')
    except Exception as e:
        messages.error(request, e)
    return redirect('airpollution:upload')
