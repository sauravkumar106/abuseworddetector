from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import TextAnalysisForm
from .models import AnalysisResult
from .services import analyze_text


def home(request):
    form = TextAnalysisForm()
    result = None
    
    if request.method == 'POST':
        form = TextAnalysisForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            analysis = analyze_text(text)
            
            result_obj = AnalysisResult.objects.create(
                text=text,
                is_offensive=analysis['is_offensive'],
                severity=analysis['severity'],
                confidence_score=analysis['confidence_score'],
                categories=analysis['categories'],
                flagged_terms=analysis['flagged_terms'],
            )
            
            result = {
                'id': result_obj.id,
                'text': text[:200] + '...' if len(text) > 200 else text,
                'is_offensive': analysis['is_offensive'],
                'severity': analysis['severity'],
                'confidence_score': analysis['confidence_score'],
                'categories': analysis['categories'],
                'flagged_terms': analysis['flagged_terms'],
                'details': analysis.get('analysis_details', {}),
            }
    
    return render(request, 'detector/home.html', {
        'form': form,
        'result': result,
    })


def history(request):
    results = AnalysisResult.objects.all()[:50]
    return render(request, 'detector/history.html', {
        'results': results,
    })


def api_analyze(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    text = request.POST.get('text', '')
    if not text:
        return JsonResponse({'error': 'Text is required'}, status=400)
    
    analysis = analyze_text(text)
    
    AnalysisResult.objects.create(
        text=text,
        is_offensive=analysis['is_offensive'],
        severity=analysis['severity'],
        confidence_score=analysis['confidence_score'],
        categories=analysis['categories'],
        flagged_terms=analysis['flagged_terms'],
    )
    
    return JsonResponse(analysis)
