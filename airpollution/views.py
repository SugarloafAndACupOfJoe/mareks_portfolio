from django.db.models import Max, Min, Sum, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
import openpyxl
import json

from airpollution.models import Pollutant, Country, PollutantEntry
from airpollution.helpers import get_headers_and_units, XLHEADERS


class ExcelUploadForm(forms.Form):
    year = forms.CharField(max_length=4)
    file = forms.FileField()


def airpollution(request):
    if request.method == 'GET':
        table_data = {}
        visuals_data = {}
        pollutant_list = [pollutant for pollutant in Pollutant.objects.all()]
        country_list = [country for country in Country.objects.all()]

        for pollutant in pollutant_list:
            table_data[pollutant.name] = {}
            visuals_data[pollutant.name] = {'labels': [], 'data': [], 'border': []}
            for country in country_list:
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
                    table_data[pollutant.name][country.iso_code] = {'avg': total / count, 'min': minimum, 'max': maximum,
                                                           'limit': pollutant.limit_value, 'units': units}
                    visuals_data[pollutant.name]['labels'].append(country.iso_code)
                    visuals_data[pollutant.name]['data'].append(total / count)
                    visuals_data[pollutant.name]['border'].append(country.color)

        # Post process visual data
        for pollutant_data in visuals_data.values():
            background_colors = [color + '50' for color in pollutant_data['border']]
            pollutant_data['labels'] = json.dumps(pollutant_data['labels'])
            pollutant_data['data'] = json.dumps(pollutant_data['data'])
            pollutant_data['background'] = json.dumps(background_colors)
            pollutant_data['border'] = json.dumps(pollutant_data['border'])

        context = {
            'app_name': request.resolver_match.app_name,
            'data': table_data,
            'visuals_data': visuals_data
        }

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
        context = {
            'app_name': request.resolver_match.app_name,
            'message_success': 'File uploaded successfully!'
        }

    else:  # Request method not POST
        return HttpResponse('This view only handles GET and POST requests')

    return render(request, 'airpollution/welcome.html', context)


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

    return redirect('airpollution:airpollution')


def temp_add_colors_to_pollutants(request):
    pollutants = ['PM2.5', 'PM10', 'NO2', 'O3', 'BaP', 'SO2']
    colors = ['#dc5c5c', '#dc5cdb', '#5c63dc', '#5cdadc', '#66dc5c', '#dcdb5c']
    to_insert = [Pollutant(name=pollutant, color=colors[i]) for i, pollutant in enumerate(pollutants)]
    Pollutant.objects.bulk_update(to_insert, ['color'])

    return redirect('airpollution:airpollution')
