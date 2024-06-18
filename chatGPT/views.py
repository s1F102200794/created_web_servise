import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import openai
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse

base_url = 'http://api.openweathermap.org/data/2.5/forecast'
base_url2 = 'http://api.openweathermap.org/data/2.5/weather'
base_url_gpt = settings.OPEN_AI_URL

api_key = settings.OPEN_WEATHER_API
api_key_gpt = settings.OPEN_AI_API

def rate_limit_exceeded(request, exception):
    return HttpResponse("トークンの上限に達してしまいました。日を改めてトライしてください。", status=429)


def get_weather_info(api_key, latitude, longitude):
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': api_key, 
        'units': 'metric', 
    }

    response = requests.get(base_url2, params=params)
    data = response.json()
    weather_description = data['weather'][0]['icon']
    
    if weather_description == '01d':
        weather_icon = 'bi bi-brightness-high'
    elif weather_description == '01n':
        weather_icon = 'bi bi-moon'
    elif weather_description == '02d':
        weather_icon = 'bi bi-cloud-sun'
    elif weather_description == '02n':
        weather_icon = 'bi bi-cloud-moon'  
    elif weather_description == '03d' or '03n':
        weather_icon = 'bi bi-cloud'   
    elif weather_description == '04d' or '04n':
        weather_icon = 'bi bi-clouds'
    elif weather_description == '09d' or '09n' or '10d' or '10n':
        weather_icon = 'bi bi-cloud-rain'
    elif weather_description == '11d' or '11n':
        weather_icon = 'bi bi-cloud-lightning'
    elif weather_description == '13d' or '13n':
        weather_icon = 'bi bi-cloud-snow'
    elif weather_description == '50d' or '50n':
        weather_icon = 'bi bi-cloud-haze2'
    else:  #iconが上記以外になった場合用
        weather_icon = 'bi bi-question'

    # 最高気温と最低気温はAPIの都合上、現時点での気温になってしまう為、正確性が低い
    weather_info = {
        'temperature_max': int(data['main']['temp_max']),
        'temperature_min': int(data['main']['temp_min']),
        'humidity': data['main']['humidity'],
        'weather_icon': weather_icon,
    }

    return weather_info

def get_weather_info_5days(api_key, latitude, longitude, index):
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': api_key,
        'units': 'metric',
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    weather_description = data['list'][index]['weather'][index]['icon']
    
    if weather_description == '01n':
        weather_icon = 'bi bi-brightness-high'
    elif weather_description == '01d':
        weather_icon = 'bi bi-moon'
    elif weather_description == '02n':
        weather_icon = 'bi bi-cloud-sun'
    elif weather_description == '02d':
        weather_icon = 'bi bi-cloud-moon'  
    elif weather_description == '03d' or '03n':
        weather_icon = 'bi bi-cloud'   
    elif weather_description == '04d' or '04n':
        weather_icon = 'bi bi-clouds'
    elif weather_description == '09d' or '09n' or '10d' or '10n':
        weather_icon = 'bi bi-cloud-rain'
    elif weather_description == '11d' or '11n':
        weather_icon = 'bi bi-cloud-lightning'
    elif weather_description == '13d' or '13n':
        weather_icon = 'bi bi-cloud-snow'
    elif weather_description == '50d' or '50n':
        weather_icon = 'bi bi-cloud-haze2'
    else:  #iconが?になった場合確認する用
        weather_icon = 'bi bi-question'

    # 最高気温と最低気温はAPIの都合上、現時点での気温になってしまう為、正確性が低い
    weather_info = {
        'temperature_max': int(data['list'][index]['main']['temp_max']),
        'temperature_min': int(data['list'][index]['main']['temp_min']),
        'humidity': data['list'][index]['main']['humidity'],
        'weather_icon': weather_icon,
        'day': int(data['list'][index]['sys']['dt_txt']),
    }

    return weather_info

def get_weather_info_gpt(api_key, latitude, longitude):
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': api_key,
        'units': 'metric',
    }

    response = requests.get(base_url2, params=params)
    data = response.json()
    return data

# Chat_GPT_APIを使用
def chat_GPT_response(api_key, latitude, longitude):
    try:
        client = openai.OpenAI(api_key=api_key_gpt, base_url=base_url_gpt)
        weather_data = get_weather_info_gpt(api_key, latitude, longitude)

        response = client.chat.completions.create(
            #model="gpt-3.5-turbo",
            #model = "gpt-4-turbo",
            model = "gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "日本語で応答してください。 あなたは天気予報士です。openweatherから取得したJSON形式のデータをお渡しする為、そのデータをもとにポイント解説をしてください。また、傘や日焼け止めが必要かどうかを自分で判断して教えてください。なお「わかりました」などの言葉は使わずに、解説だけを話してください。次がデータです。" + str(weather_data)
                    #デバッグ用
                    #'content': 'テストメッセージです。と返してください。'
                },
            ],
        )
        return response.choices[0].message.content
    
    except openai.RateLimitError as e:
        return ("トークンの上限に達してしまいました。24時間後に回復しますので、そのあとに試してみてください。")

def chat_GPT_response_jap(api_key, latitude1, longitude1, latitude2, longitude2, latitude3, longitude3):
    try:
        client = openai.OpenAI(api_key=api_key_gpt, base_url=base_url_gpt)
        weather_data_Sap = get_weather_info_gpt(api_key, latitude = latitude1, longitude = longitude1)
        weather_data_Tokyo = get_weather_info_gpt(api_key, latitude = latitude2, longitude = longitude2)
        weather_data_Kago = get_weather_info_gpt(api_key, latitude = latitude3, longitude = longitude3)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            #model = "gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "日本語で応答してください。 あなたは天気予報士です。openweatherから取得したJSON形式のデータをお渡しする為、そのデータをもとにポイント解説をしてください。鹿児島のデータと東京のデータと札幌のデータを渡すので日本全体の天気予報を予測して話してください。特段、札幌や鹿児島、東京の天気の解説はいりません。また、傘や日焼け止めが必要かどうかを自分で判断して教えてください。なお「わかりました」などの言葉は使わずに、解説だけをしてください。次が鹿児島のデータです。" + str(weather_data_Sap) + "次が東京のデータです。" + str(weather_data_Tokyo) + "次が鹿児島のデータです。" + str(weather_data_Kago),
                    #デバッグ用
                    #'content': 'テストメッセージです。と返してください。',
                },
            ],
        )
        return response.choices[0].message.content
    except openai.RateLimitError as e:
        return ("トークンの上限に達してしまいました。24時間後に回復しますので、そのあとに試してみてください。")


# Chat_GPT_APIを使用
@login_required
def Japan_weather_gpt(request):
    
    Sap_lat = 43.062
    Sap_lon = 141.3543
    Kushi_lat = 42.9848
    Kushi_lon = 144.3813
    Tokyo_lat = 35.6894
    Tokyo_lon = 139.6917
    Osaka_lat = 34.6937
    Osaka_lon =135.5021
    Nagoya_lat = 35.1814
    Nagoya_lon = 136.9063
    Kago_lat = 31.5965
    Kago_lon = 130.5571
    Naha_lat = 26.2123
    Naha_lon = 127.6791
    Toku_lat = 34.0702
    Toku_lon = 134.5548
    Hiro_lat = 34.3852
    Hiro_lon = 132.4552
    Hukuo_lat = 33.5903
    Hukuo_lon = 130.4017
    Kanaz_lat = 36.5613
    Kanaz_lon = 136.6562
    Niiga_lat = 37.9161
    Niiga_lon = 139.0364
    Senda_lat = 38.2682
    Senda_lon = 140.8693
    Aomo_lat = 40.822
    Aomo_lon = 140.7473
    # 都市名、郵便番号、都市 IDによる API リクエストは廃止されたことに注意してください。
    # 上記のように記載があるため、使用しない

    Sap_weather_info = get_weather_info(api_key, Sap_lat, Sap_lon)
    Kushi_weather_info = get_weather_info(api_key, Kushi_lat, Kushi_lon)
    Tokyo_weather_info = get_weather_info(api_key, Tokyo_lat, Tokyo_lon)
    Osaka_weather_info = get_weather_info(api_key, Osaka_lat, Osaka_lon)
    Nagoya_weather_info = get_weather_info(api_key, Nagoya_lat, Nagoya_lon)
    Kago_weather_info = get_weather_info(api_key, Kago_lat, Kago_lon)
    Naha_weather_info = get_weather_info(api_key, Naha_lat, Naha_lon)
    Toku_weather_info = get_weather_info(api_key, Toku_lat, Toku_lon)
    Hiro_weather_info = get_weather_info(api_key, Hiro_lat, Hiro_lon)
    Hukuo_weather_info = get_weather_info(api_key, Hukuo_lat, Hukuo_lon)
    Kanaz_weather_info = get_weather_info(api_key, Kanaz_lat, Kanaz_lon)
    Niiga_weather_info = get_weather_info(api_key, Niiga_lat, Niiga_lon)
    Senda_weather_info = get_weather_info(api_key, Senda_lat, Senda_lon)
    Aomo_weather_info = get_weather_info(api_key, Aomo_lat, Aomo_lon)

    chat_results = chat_GPT_response_jap(api_key, Sap_lat, Sap_lon, Tokyo_lat, Tokyo_lon, Kago_lat, Kago_lon)

    context = {
        'Sap_weather_info': Sap_weather_info,
        'Kushi_weather_info': Kushi_weather_info,
        'Tokyo_weather_info': Tokyo_weather_info,
        'Osaka_weather_info': Osaka_weather_info,
        'Nagoya_weather_info': Nagoya_weather_info,
        'Kago_weather_info': Kago_weather_info,
        'Naha_weather_info': Naha_weather_info,
        'Toku_weather_info': Toku_weather_info,
        'Hiro_weather_info': Hiro_weather_info,
        'Hukuo_weather_info': Hukuo_weather_info,
        'Kanaz_weather_info': Kanaz_weather_info,
        'Niiga_weather_info': Niiga_weather_info,
        'Senda_weather_info': Senda_weather_info,
        'Aomo_weather_info': Aomo_weather_info,
        'chat_results': chat_results
    }

    return render(request, 'chatGPT/index.html', context)


@login_required
def Hokkaido_weather_gpt(request):

    Sap_lat = 43.062
    Sap_lon = 141.3543
    Hako_lat = 41.7687
    Hako_lon = 140.7288
    Kushi_lat = 42.9848
    Kushi_lon = 144.3813
    Asahi_lat = 43.7706
    Asahi_lon = 142.3648
    Wakka_lat = 45.4156
    Wakka_lon = 141.673
    Abashi_lat = 44.0206
    Abashi_lon = 144.2733

    Sap_weather_info = get_weather_info(api_key, Sap_lat, Sap_lon)
    Hako_weather_info = get_weather_info(api_key, Hako_lat, Hako_lon)
    Asahi_weather_info = get_weather_info(api_key, Asahi_lat, Asahi_lon)
    Kushi_weather_info = get_weather_info(api_key, Kushi_lat, Kushi_lon)
    Wakka_weather_info = get_weather_info(api_key, Wakka_lat, Wakka_lon)
    Abashi_weather_info = get_weather_info(api_key, Abashi_lat, Abashi_lon)
    
    chat_results = chat_GPT_response(api_key, Sap_lat, Sap_lon)

    context = {
        'Sap_weather_info': Sap_weather_info,
        'Hako_weather_info': Hako_weather_info,
        'Asahi_weather_info': Asahi_weather_info,
        'Kushi_weather_info': Kushi_weather_info,
        'Wakka_weather_info': Wakka_weather_info,
        'Abashi_weather_info': Abashi_weather_info,
        'chat_results': chat_results,
        }
    return render(request, 'chatGPT/Hokkaido.html', context)

@login_required
def Tohoku_weather_gpt(request):

    Aomo_lat = 40.822
    Aomo_lon = 140.7473
    Iwate_lat = 39.702
    Iwate_lon = 141.1544
    Akita_lat = 39.7199
    Akita_lon = 140.1035
    Yamaga_lat = 38.2554
    Yamaga_lon = 140.3396
    Miya_lat = 38.2682
    Miya_lon = 140.8693
    Hukushi_lat = 37.4005
    Hukushi_lon = 140.3597

    Aomo_weather_info = get_weather_info(api_key, Aomo_lat, Aomo_lon)
    Iwate_weather_info = get_weather_info(api_key, Iwate_lat, Iwate_lon)
    Akita_weather_info = get_weather_info(api_key, Akita_lat, Akita_lon)
    Yamaga_weather_info = get_weather_info(api_key, Yamaga_lat, Yamaga_lon)
    Miya_weather_info = get_weather_info(api_key, Miya_lat, Miya_lon)
    Hukushi_weather_info = get_weather_info(api_key, Hukushi_lat, Hukushi_lon)
    
    chat_results = chat_GPT_response(api_key, Iwate_lat, Iwate_lon)

    context = {
        'Aomo_weather_info': Aomo_weather_info,
        'Iwate_weather_info': Iwate_weather_info,
        'Akita_weather_info': Akita_weather_info,
        'Yamaga_weather_info': Yamaga_weather_info,
        'Miya_weather_info': Miya_weather_info,
        'Hukushi_weather_info': Hukushi_weather_info,
        'chat_results': chat_results,
        }
    return render(request, 'chatGPT/Tohoku.html', context)

@login_required
def Kanto_weather_gpt(request):

    Iba_lat = 36.0834
    Iba_lon = 140.0766
    Tochi_lat = 36.5657
    Tochi_lon = 139.8835
    Chiba_lat = 35.605
    Chiba_lon = 140.1233
    Gunma_lat = 36.3894
    Gunma_lon = 139.0634
    Saita_lat = 35.9064
    Saita_lon = 139.6287
    Tokyo_lat = 35.6894
    Tokyo_lon = 139.6917
    Kanag_lat = 35.4437
    Kanag_lon = 139.638

    Iba_weather_info = get_weather_info(api_key, Iba_lat, Iba_lon)
    Tochi_weather_info = get_weather_info(api_key, Tochi_lat, Tochi_lon)
    Chiba_weather_info = get_weather_info(api_key, Chiba_lat, Chiba_lon)
    Gunma_weather_info = get_weather_info(api_key, Gunma_lat, Gunma_lon)
    Saita_weather_info = get_weather_info(api_key, Saita_lat, Saita_lon)
    Tokyo_weather_info = get_weather_info(api_key, Tokyo_lat, Tokyo_lon)
    Kanag_weather_info = get_weather_info(api_key, Kanag_lat, Kanag_lon)
    
    chat_results = chat_GPT_response(api_key, Tokyo_lat, Tokyo_lon)
    
    context = {
        'Iba_weather_info': Iba_weather_info,
        'Tochi_weather_info': Tochi_weather_info,
        'Chiba_weather_info': Chiba_weather_info,
        'Gunma_weather_info': Gunma_weather_info,
        'Saita_weather_info': Saita_weather_info,
        'Tokyo_weather_info': Tokyo_weather_info,
        'Kanag_weather_info': Kanag_weather_info,
        'chat_results': chat_results,
        }
    return render(request, 'chatGPT/Kanto.html', context)

@login_required
def Chubu_weather_gpt(request):

    Niiga_lat = 37.9161
    Niiga_lon = 139.0364
    Toyama_lat = 36.6959
    Toyama_lon = 137.2136
    Nagan_lat = 37.9161
    Nagan_lon = 139.0364
    Yaman_lat = 35.6622
    Yaman_lon = 138.5682
    Shiz_lat = 34.9771
    Shiz_lon = 138.383
    Gihu_lat = 35.4232
    Gihu_lon = 136.7606
    Ishi_lat = 36.5613
    Ishi_lon = 136.6562
    Hukui_lat = 36.064
    Hukui_lon = 136.2194
    Aichi_lat = 35.1814
    Aichi_lon = 136.9063

    Niiga_weather_info = get_weather_info(api_key, Niiga_lat, Niiga_lon)
    Toyama_weather_info = get_weather_info(api_key, Toyama_lat, Toyama_lon)
    Nagan_weather_info = get_weather_info(api_key, Nagan_lat, Nagan_lon)
    Yaman_weather_info = get_weather_info(api_key, Yaman_lat, Yaman_lon)
    Shiz_weather_info = get_weather_info(api_key, Shiz_lat, Shiz_lon)
    Gihu_weather_info = get_weather_info(api_key, Gihu_lat, Gihu_lon)
    Ishi_weather_info = get_weather_info(api_key, Ishi_lat, Ishi_lon)
    Hukui_weather_info = get_weather_info(api_key, Hukui_lat, Hukui_lon)
    Aichi_weather_info = get_weather_info(api_key, Aichi_lat, Aichi_lon)

    chat_results = chat_GPT_response(api_key, Aichi_lat, Aichi_lon)

    context = {
        'Niiga_weather_info': Niiga_weather_info,
        'Toyama_weather_info': Toyama_weather_info,
        'Nagan_weather_info': Nagan_weather_info,
        'Yaman_weather_info': Yaman_weather_info,
        'Shiz_weather_info': Shiz_weather_info,
        'Gihu_weather_info': Gihu_weather_info,
        'Ishi_weather_info': Ishi_weather_info,
        'Hukui_weather_info': Hukui_weather_info,
        'Aichi_weather_info': Aichi_weather_info,
        'chat_results': chat_results,
        }
    return render(request, 'chatGPT/Chubu.html', context)

@login_required
def Kinki_weather_gpt(request):

    Shiga_lat = 35.0045
    Shiga_lon = 135.8685
    Mie_lat = 34.7185
    Mie_lon = 136.5056
    Kyoto_lat = 35.0116
    Kyoto_lon = 135.768
    Nara_lat = 34.685
    Nara_lon = 135.805
    Hyogo_lat = 34.69
    Hyogo_lon = 135.1955
    Osaka_lat = 34.6937
    Osaka_lon = 135.5021
    Wakay_lat = 34.2305
    Wakay_lon = 135.1708

    Shiga_weather_info = get_weather_info(api_key, Shiga_lat, Shiga_lon)
    Mie_weather_info = get_weather_info(api_key, Mie_lat, Mie_lon)
    Kyoto_weather_info = get_weather_info(api_key, Kyoto_lat, Kyoto_lon)
    Nara_weather_info = get_weather_info(api_key, Nara_lat, Nara_lon)
    Hyogo_weather_info = get_weather_info(api_key, Hyogo_lat, Hyogo_lon)
    Osaka_weather_info = get_weather_info(api_key, Osaka_lat, Osaka_lon)
    Wakay_weather_info = get_weather_info(api_key, Wakay_lat, Wakay_lon)

    chat_results = chat_GPT_response(api_key, Osaka_lat, Osaka_lon)

    context = {
        'Shiga_weather_info': Shiga_weather_info,
        'Mie_weather_info': Mie_weather_info,
        'Kyoto_weather_info': Kyoto_weather_info,
        'Nara_weather_info': Nara_weather_info,
        'Hyogo_weather_info': Hyogo_weather_info,
        'Osaka_weather_info': Osaka_weather_info,
        'Wakay_weather_info': Wakay_weather_info,
        'chat_results': chat_results,
        }
    return render(request, 'chatGPT/Kinki.html', context)

@login_required
def Chugoku_weather_gpt(request):

    Totto_lat = 35.5011
    Totto_lon = 134.235
    Okaya_lat = 34.6551
    Okaya_lon = 133.9195
    Shimane_lat = 35.468
    Shimane_lon = 133.0483
    Hiro_lat = 34.3852
    Hiro_lon = 132.4552
    Yamag_lat = 33.9515
    Yamag_lon = 131.2467

    Totto_weather_info = get_weather_info(api_key, Totto_lat, Totto_lon)
    Okaya_weather_info = get_weather_info(api_key, Okaya_lat, Okaya_lon)
    Shimane_weather_info = get_weather_info(api_key, Shimane_lat, Shimane_lon)
    Hiro_weather_info = get_weather_info(api_key, Hiro_lat, Hiro_lon)
    Yamag_weather_info = get_weather_info(api_key, Yamag_lat, Yamag_lon)
    
    chat_results = chat_GPT_response(api_key, Hiro_lat, Hiro_lon)

    context = {
        'Totto_weather_info': Totto_weather_info,
        'Okaya_weather_info': Okaya_weather_info,
        'Shimane_weather_info': Shimane_weather_info,
        'Hiro_weather_info': Hiro_weather_info,
        'Yamag_weather_info': Yamag_weather_info,
        'chat_results': chat_results,
        }
    return render(request, 'chatGPT/Chugoku.html', context)

@login_required
def Shikoku_weather_gpt(request):

    Kaga_lat = 34.3427
    Kaga_lon = 134.0465
    Toku_lat = 34.1725
    Toku_lon = 134.6087
    Ehime_lat = 33.8391
    Ehime_lon = 132.7655
    Kochi_lat = 33.5595
    Kochi_lon = 133.5292

    Kaga_weather_info = get_weather_info(api_key, Kaga_lat, Kaga_lon)
    Toku_weather_info = get_weather_info(api_key, Toku_lat, Toku_lon)
    Ehime_weather_info = get_weather_info(api_key, Ehime_lat, Ehime_lon)
    Kochi_weather_info = get_weather_info(api_key, Kochi_lat, Kochi_lon)
    
    chat_results = chat_GPT_response(api_key, Ehime_lat, Ehime_lon)

    context = {
        'Kaga_weather_info': Kaga_weather_info,
        'Toku_weather_info': Toku_weather_info,
        'Ehime_weather_info': Ehime_weather_info,
        'Kochi_weather_info': Kochi_weather_info,
        'chat_results': chat_results,
        }
    return render(request, 'chatGPT/Shikoku.html', context)

@login_required
def Kyusyu_weather_gpt(request):

    Ooi_lat = 33.2395
    Ooi_lon = 131.6092
    Miyaz_lat = 31.9076
    Miyaz_lon = 131.4202
    Hukuo_lat = 33.5903
    Hukuo_lon = 130.4017
    Kuma_lat = 32.8031
    Kuma_lon = 130.7078
    Kagoshi_lat = 31.5965
    Kagoshi_lon = 130.5571
    Saga_lat = 33.2634
    Saga_lon = 130.3008
    Nagasa_lat = 32.7502
    Nagasa_lon = 129.8776

    Ooi_weather_info = get_weather_info(api_key, Ooi_lat, Ooi_lon)
    Miyaz_weather_info = get_weather_info(api_key, Miyaz_lat, Miyaz_lon)
    Hukuo_weather_info = get_weather_info(api_key, Hukuo_lat, Hukuo_lon)
    Kuma_weather_info = get_weather_info(api_key, Kuma_lat, Kuma_lon)
    Kagoshi_weather_info = get_weather_info(api_key, Kagoshi_lat, Kagoshi_lon)
    Saga_weather_info = get_weather_info(api_key, Saga_lat, Saga_lon)
    Nagasa_weather_info = get_weather_info(api_key, Nagasa_lat, Nagasa_lon)
    
    chat_results = chat_GPT_response(api_key, Miyaz_lat, Miyaz_lon)

    context = {
        'Ooi_weather_info': Ooi_weather_info,
        'Miyaz_weather_info': Miyaz_weather_info,
        'Hukuo_weather_info': Hukuo_weather_info,
        'Kuma_weather_info': Kuma_weather_info,
        'Kagoshi_weather_info': Kagoshi_weather_info,
        'Saga_weather_info': Saga_weather_info,
        'Nagasa_weather_info': Nagasa_weather_info,
        'chat_results': chat_results
        }
    return render(request, 'chatGPT/Kyusyu.html', context)
