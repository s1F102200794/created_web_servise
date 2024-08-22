from django.http import HttpResponse
from django.template import loader
from .forms import ChatForm
import openai
from django.shortcuts import render
from django.conf import settings

base_url = settings.OPEN_AI_URL
api_key = settings.OPEN_AI_API

def index(request):
    """
    チャット画面
    """

    # 応答結果
    chat_results = ""

    if request.method == "POST":
        

        form = ChatForm(request.POST)
        if form.is_valid():

            sentence = form.cleaned_data['sentence']

            client = openai.OpenAI(
              api_key = api_key,
              base_url = base_url,
            )

            # ChatGPT
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "日本語で応答してください ある生徒の読書感想文を見せます。その文章を具体的、中立的に評論してください。１００点満点中何点か教えてください。テンプレートとして、感想文を書いた人の名前  点数  改行してください 評価 改行してください こうしたらもっと良くなるなどのレコメンドをよろしくお願いします。改行 この感想文を読んでおすすめな本を紹介してください"
                    },
                    {
                        "role": "user",
                        "content": sentence
                    },
                ],
            )

            chat_results = response.choices[0].message.content

    else:
        form = ChatForm()

    template = loader.get_template('chat/index.html')
    context = {
        'form': form,
        'chat_results': chat_results
    }
    return HttpResponse(template.render(context, request))