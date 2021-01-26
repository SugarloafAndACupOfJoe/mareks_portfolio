from django.shortcuts import render
from django import forms
import openpyxl

from airpollution.models import Pollutant, Country, PollutantEntry
from airpollution.helpers import get_headers_and_units, XLHEADERS


class ExcelUploadForm(forms.Form):
    year = forms.CharField(max_length=4)
    file = forms.FileField()


def welcome(request):
    context = {
        'app_name': request.resolver_match.app_name
    }
    return render(request, 'airpollution/welcome.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            year = form.cleaned_data['year']
            file = form.cleaned_data['file']
            wb = openpyxl.load_workbook(filename=file, read_only=False)
            tab_names = wb.get_sheet_names()
            for tab_name in tab_names:
                ws = wb[tab_name]
                pollutant_name = tab_name.split('_')[0]
                pollutant = Pollutant.objects.get_or_create(name=pollutant_name)
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
        context = {
            'app_name': request.resolver_match.app_name,
            'message_success': 'This view only accepts POST methods'
        }

    return render(request, 'airpollution/welcome.html', context)


def temp_country_creator(request):
    countries = {
        'Albania': 'AL',
        'Andorra': 'AD',
        'Austria': 'AT',
        'Belgium': 'BE',
        'Bosnia and Herzegovina': 'BA',
        'Bulgaria': 'BG',
        'Croatia': 'HR',
        'Cyprus': 'CY',
        'Czech Republic': 'CZ',
        'Denmark': 'DK',
        'Estonia': 'EE',
        'Finland': 'FI',
        'France': 'FR',
        'Germany': 'DE',
        'Greece': 'GR',
        'Hungary': 'HU',
        'Iceland': 'IS',
        'Ireland': 'IE',
        'Italy': 'IT',
        'Kosovo under UNSCR 1244/99': 'XK',
        'Latvia': 'LV',
        'Lithuania': 'LT',
        'Luxembourg': 'LU',
        'Malta': 'MT',
        'Montenegro': 'ME',
        'Netherlands': 'NL',
        'Norway': 'NO',
        'Poland': 'PL',
        'Portugal': 'PT',
        'Romania': 'RO',
        'Serbia': 'RS',
        'Slovakia': 'SK',
        'Slovenia': 'SI',
        'Spain': 'ES',
        'Sweden': 'SE',
        'Switzerland': 'CH',
        'The former Yugoslav Republic of Macedonia': 'MK',
        'Turkey': 'TR',
        'United Kingdom': 'GB',
    }

    to_insert = []
    for country_name, iso_code in countries.items():
        to_insert.append(Country(iso_code=iso_code, name=country_name))
    Country.objects.bulk_create(to_insert)

    context = {
        'app_name': request.resolver_match.app_name,
        'message_success': 'Countries created successfully'
    }

    return render(request, 'airpollution/welcome.html', context)
