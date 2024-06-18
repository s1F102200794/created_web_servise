# forms.py
from django import forms

class ChatForm(forms.Form):
    sentence = forms.CharField(label='チャット', widget=forms.Textarea(), required=True)

class HeightQuizForm(forms.Form):
    height_choices = [
        (140, "140cm"),
        (155, "155cm"),
        (175, "175cm"),
        (190, "190cm"),
    ]
    selected_height = forms.TypedChoiceField(
        choices=height_choices,
        widget=forms.RadioSelect,
        coerce=int,
        label="美紀ちゃんの身長は140cmです。美紀ちゃんのお父さんの身長は美紀ちゃんの1.25倍です。お父さんの身長は何センチになりますか？",
        label_suffix=''
    )

class IceCreamQuizForm(forms.Form):
    ice_cream_choices = [
        (0.5, "0.5倍"),
        (1.0, "1.0倍"),
        (1.5, "1.5倍"),
        (2.0, "2.0倍"),
    ]
    selected_ice_cream = forms.TypedChoiceField(
        choices=ice_cream_choices,
        widget=forms.RadioSelect,
        coerce=float,
        label="1個100円のアイスAと1個150円のアイスBがあります。アイスBの値段は、アイスAの値段の何倍でしょうか？",
        label_suffix=''
    )


class Fraction1Form(forms.Form):
    fraction1_choices = [
        (2/3, '2/3'),
        (2/41, '2/41'),
        (3/8, '3/8'),
        (1/4, '1/4'),
    ]
    selected_fraction1 = forms.TypedChoiceField(
        choices=fraction1_choices,
        widget=forms.RadioSelect,
        coerce=float,
        label='1/2 + 1/6 =',
        label_suffix=''
    )

class Fraction2Form(forms.Form):
    fraction2_choices = [
        (6/10, '6/10'),
        (13/24, '13/24'),
        (7/12, '7/12'),
        (8/31, '8/31'),
    ]
    selected_fraction2 = forms.TypedChoiceField(
        choices=fraction2_choices,
        widget=forms.RadioSelect,
        coerce=float,
        label='5/6 - 1/4 =',
        label_suffix=''
    )


