from django import forms


class TextAnalysisForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter text to analyze for offensive or abusive content...',
        }),
        max_length=5000,
        required=True,
        label='Text to Analyze'
    )
