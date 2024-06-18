python3 -m venv venv

source venv/bin/activate
(powershellの場合 --> .\venv\script\activate)

pip install -r requirements.txt
python manage.py runserver

デフォルトではchatGPTを使用する部分はiniadアカウントでのログインが必須になっています。
ログインしたくない場合は@login_requiredの部分を削除してください。

また、ChatGPTのAPIは制限があるため、上限に達してしまった場合はRateLimitErrorのエラーが出ます。丸1日開けるかAPIキーを別のもので使用してください。

ログイン機能でiniadアカウントをクリックしてもロードが終わらないバグが発生しています。Ctrl + Cでターミナルを止めていただきもう一度ログインボタンを押すとログインできます。