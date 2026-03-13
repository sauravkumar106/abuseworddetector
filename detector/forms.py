from django import forms


class TextAnalysisForm(forms.Form):
    MODE_CHOICES = [
        ('kid', '🧒 Kid Mode'),
        ('adult', '🔞 Adult Mode'),
    ]

    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter text or paste content to analyze…',
        }),
        max_length=5000,
        required=True,
        label='Text to Analyze'
    )

    mode = forms.ChoiceField(
        choices=MODE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'mode-radio'}),
        initial='adult',
        required=True,
        label='Detection Mode',
    )
