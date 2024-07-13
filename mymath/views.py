from django.shortcuts import render
from django.http import HttpResponse
from .forms import HeightQuizForm, IceCreamQuizForm, Fraction1Form, Fraction2Form
from django.template import loader
from .forms import ChatForm
import openai
from django.contrib.auth.decorators import login_required
from django.conf import settings


# OpenAI APIキーを設定
api_key = settings.OPEN_AI_API
api_base = settings.OPEN_AI_URL

api_key_my = settings.OPEN_AI_API_MY
api_base_my = settings.OPEN_AI_URL_MY

@login_required
def height_quiz_view(request):
    try:
        height_form = HeightQuizForm(prefix="height")
        ice_cream_form = IceCreamQuizForm(prefix="ice_cream")
        fraction1_form = Fraction1Form(prefix="fraction1")
        fraction2_form = Fraction2Form(prefix="fraction2")
        height_result = None
        ice_cream_result = None
        fraction1_result = None
        fraction2_result = None
        similar_question = ""
        chat_results = ""
        similar_question2 = ""
        chat_results2 = ""

        if request.method == 'POST':
            height_form = HeightQuizForm(request.POST, prefix="height")
            ice_cream_form = IceCreamQuizForm(request.POST, prefix="ice_cream")
            fraction1_form = Fraction1Form(request.POST, prefix="fraction1")
            fraction2_form = Fraction2Form(request.POST, prefix="fraction2")

            # 割合の問題の処理
            if height_form.is_valid() and ice_cream_form.is_valid():
                selected_height = height_form.cleaned_data['selected_height']
                selected_ice_cream = ice_cream_form.cleaned_data['selected_ice_cream']

                height_result = "正解" if selected_height == 175 else "不正解"
                ice_cream_result = "正解" if selected_ice_cream == 1.5 else "不正解"

                if height_result == "不正解" or ice_cream_result == "不正解":
                    incorrect_question = ""
                    if height_result == "不正解":
                        incorrect_question = "美紀ちゃんの身長は140cmです。美紀ちゃんのお父さんの身長は美紀ちゃんの1.25倍です。お父さんの身長は何センチになりますか？"
                    else:
                        incorrect_question = "1個100円のアイスAと1個150円のアイスBがあります。アイスBの値段は、アイスAの値段の何倍でしょうか？"

                    client = openai.OpenAI(api_key=api_key, base_url=api_base)
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        #問題を出題するのは、3.5で行う
                        #model='gpt-4',
                        messages=[
                            {
                                'role': 'system',
                                'content': f"次の問題を間違えました。次、間違えないように同じような例題を作ってください。なお「かしこまりました」などは答えず、問題のみを書いてください。{incorrect_question}",
                            }]
                        )
                    chat_results = completion.choices[0].message.content.strip()
                    similar_question_response = client.chat.completions.create(
                    #model="gpt-3.5-turbo",
                    model = "gpt-4o",
                    messages=[
                                {
                                    "role": "system",
                                    "content": "日本語でお願いします。" + chat_results
                                }
                            ]
                        )
                    similar_question = similar_question_response.choices[0].message.content

            # 分数の問題の処理
            if fraction1_form.is_valid() and fraction2_form.is_valid():
                selected_fraction1 = fraction1_form.cleaned_data['selected_fraction1']
                selected_fraction2 = fraction2_form.cleaned_data['selected_fraction2']

                fraction1_result = "正解" if selected_fraction1 == 2/3 else "不正解"
                fraction2_result = "正解" if selected_fraction2 == 7/12 else "不正解"

                if fraction1_result == "不正解" or fraction2_result == "不正解":
                    incorrect_question2 = ""
                    if fraction1_result == "不正解":
                        incorrect_question2 = "1/2 + 1/6 = ?"
                    elif fraction2_result == "不正解":
                        incorrect_question2 = "5/6 + 1/4 = ?"

                    if incorrect_question2:
                        client = openai.OpenAI(api_key=api_key, base_url=api_base)
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            #問題を出題するのは、3.5で行う
                            #model='gpt-4',
                            messages=[
                                {
                                    'role': 'system',
                                    'content': f"次の問題を間違えました。次、間違えないように同じような例題を作ってください。なお「かしこまりました」などは答えず、問題のみを書いてください。{incorrect_question2}",
                                }]
                        )
                        
                        chat_results2 = completion.choices[0].message.content.strip()
                        similar_question_response = client.chat.completions.create(
                            #model="gpt-3.5-turbo",
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "system",
                                    "content": "日本語でお願いします。" + chat_results2
                                }
                            ]
                        )
                        similar_question2 = similar_question_response.choices[0].message.content

        context = {
            'height_form': height_form,
            'ice_cream_form': ice_cream_form,
            'height_result': height_result,
            'ice_cream_result': ice_cream_result,
            'fraction1_form': fraction1_form,
            'fraction2_form': fraction2_form,
            'fraction1_result': fraction1_result,
            'fraction2_result': fraction2_result,
            'chat_results': chat_results,
            'chat_results2': chat_results2,
            'similar_question': similar_question,
            'similar_question2': similar_question2,  # コンテキストにもう一つの類題を追加
        }

        return render(request, 'mymath/quiz.html', context)
    
    except openai.RateLimitError as e:
        try:
            height_form = HeightQuizForm(prefix="height")
            ice_cream_form = IceCreamQuizForm(prefix="ice_cream")
            fraction1_form = Fraction1Form(prefix="fraction1")
            fraction2_form = Fraction2Form(prefix="fraction2")
            height_result = None
            ice_cream_result = None
            fraction1_result = None
            fraction2_result = None
            similar_question = ""
            chat_results = ""
            similar_question2 = ""
            chat_results2 = ""

            if request.method == 'POST':
                height_form = HeightQuizForm(request.POST, prefix="height")
                ice_cream_form = IceCreamQuizForm(request.POST, prefix="ice_cream")
                fraction1_form = Fraction1Form(request.POST, prefix="fraction1")
                fraction2_form = Fraction2Form(request.POST, prefix="fraction2")

                # 割合の問題の処理
                if height_form.is_valid() and ice_cream_form.is_valid():
                    selected_height = height_form.cleaned_data['selected_height']
                    selected_ice_cream = ice_cream_form.cleaned_data['selected_ice_cream']

                    height_result = "正解" if selected_height == 175 else "不正解"
                    ice_cream_result = "正解" if selected_ice_cream == 1.5 else "不正解"

                    if height_result == "不正解" or ice_cream_result == "不正解":
                        incorrect_question = ""
                        if height_result == "不正解":
                            incorrect_question = "美紀ちゃんの身長は140cmです。美紀ちゃんのお父さんの身長は美紀ちゃんの1.25倍です。お父さんの身長は何センチになりますか？"
                        else:
                            incorrect_question = "1個100円のアイスAと1個150円のアイスBがあります。アイスBの値段は、アイスAの値段の何倍でしょうか？"

                        client = openai.OpenAI(api_key=api_key_my, base_url=api_base_my)
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            #問題を出題するのは、3.5で行う
                            #model='gpt-4',
                            messages=[
                                {
                                    'role': 'system',
                                    'content': f"次の問題を間違えました。次、間違えないように同じような例題を作ってください。なお「かしこまりました」などは答えず、問題のみを書いてください。{incorrect_question}",
                                }]
                            )
                        chat_results = completion.choices[0].message.content.strip()
                        similar_question_response = client.chat.completions.create(
                        #model="gpt-3.5-turbo",
                        model = "gpt-4o",
                        messages=[
                                    {
                                        "role": "system",
                                        "content": "日本語でお願いします。" + chat_results
                                    }
                                ]
                            )
                        similar_question = similar_question_response.choices[0].message.content

                # 分数の問題の処理
                if fraction1_form.is_valid() and fraction2_form.is_valid():
                    selected_fraction1 = fraction1_form.cleaned_data['selected_fraction1']
                    selected_fraction2 = fraction2_form.cleaned_data['selected_fraction2']

                    fraction1_result = "正解" if selected_fraction1 == 2/3 else "不正解"
                    fraction2_result = "正解" if selected_fraction2 == 7/12 else "不正解"

                    if fraction1_result == "不正解" or fraction2_result == "不正解":
                        incorrect_question2 = ""
                        if fraction1_result == "不正解":
                            incorrect_question2 = "1/2 + 1/6 = ?"
                        elif fraction2_result == "不正解":
                            incorrect_question2 = "5/6 + 1/4 = ?"

                        if incorrect_question2:
                            client = openai.OpenAI(api_key=api_key_my, base_url=api_base_my)
                            completion = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                #問題を出題するのは、3.5で行う
                                #model='gpt-4',
                                messages=[
                                    {
                                        'role': 'system',
                                        'content': f"次の問題を間違えました。次、間違えないように同じような例題を作ってください。なお「かしこまりました」などは答えず、問題のみを書いてください。{incorrect_question2}",
                                    }]
                            )
                            
                            chat_results2 = completion.choices[0].message.content.strip()
                            similar_question_response = client.chat.completions.create(
                                #model="gpt-3.5-turbo",
                                model="gpt-4o",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": "日本語でお願いします。" + chat_results2
                                    }
                                ]
                            )
                            similar_question2 = similar_question_response.choices[0].message.content

            context = {
                'height_form': height_form,
                'ice_cream_form': ice_cream_form,
                'height_result': height_result,
                'ice_cream_result': ice_cream_result,
                'fraction1_form': fraction1_form,
                'fraction2_form': fraction2_form,
                'fraction1_result': fraction1_result,
                'fraction2_result': fraction2_result,
                'chat_results': chat_results,
                'chat_results2': chat_results2,
                'similar_question': similar_question,
                'similar_question2': similar_question2,  # コンテキストにもう一つの類題を追加
            }

            return render(request, 'mymath/quiz.html', context) 
        except openai.RateLimitError as e:
            return HttpResponse("ChatGPTのトークンの上限に達してしまいました。24時間後に回復しますので、そのあとに試してみてください。")

