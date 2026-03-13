from django.shortcuts import render
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
            mode = form.cleaned_data['mode']
            analysis = analyze_text(text, mode=mode)

            result_obj = AnalysisResult.objects.create(
                text=text,
                is_offensive=analysis['is_offensive'],
                severity=analysis['severity'],
                confidence_score=analysis['confidence_score'],
                categories=analysis['categories'],
                flagged_terms=analysis['flagged_terms'],
                emoji_detections=analysis['emoji_detections'],
                mode=analysis['mode'],
            )

            # Build sorted ML scores list for the template bar chart
            ml_scores_list = []
            label_map = {
                'toxicity': 'Toxic',
                'severe_toxicity': 'Severe',
                'obscene': 'Obscene',
                'threat': 'Threat',
                'insult': 'Insult',
                'identity_attack': 'Hate Speech',
            }
            for key, label in label_map.items():
                score = analysis.get('ml_scores', {}).get(key, None)
                if score is not None:
                    ml_scores_list.append({
                        'key': key,
                        'label': label,
                        'score': score,
                        'pct': int(score * 100),
                    })

            result = {
                'id': result_obj.id,
                'text': text[:200] + '...' if len(text) > 200 else text,
                'is_offensive': analysis['is_offensive'],
                'severity': analysis['severity'],
                'confidence_score': int(analysis['confidence_score'] * 100),
                'categories': analysis['categories'],
                'flagged_terms': analysis['flagged_terms'],
                'emoji_detections': analysis['emoji_detections'],
                'ml_scores': ml_scores_list,
                'mode': analysis['mode'],
                'engine': analysis['analysis_details'].get('engine', 'unknown'),
                'details': analysis.get('analysis_details', {}),
            }

    return render(request, 'detector/home.html', {
        'form': form,
        'result': result,
    })


def history(request):
    results_queryset = AnalysisResult.objects.all()[:50]
    results = []
    for r in results_queryset:
        results.append({
            'text': r.text,
            'is_offensive': r.is_offensive,
            'severity': r.severity,
            'confidence_score': int(r.confidence_score * 100),
            'categories': r.categories,
            'flagged_terms': r.flagged_terms,
            'emoji_detections': r.emoji_detections,
            'mode': r.mode,
            'analyzed_at': r.analyzed_at,
        })
    return render(request, 'detector/history.html', {
        'results': results,
    })


def api_analyze(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    text = request.POST.get('text', '')
    mode = request.POST.get('mode', 'adult')

    if not text:
        return JsonResponse({'error': 'Text is required'}, status=400)

    analysis = analyze_text(text, mode=mode)

    AnalysisResult.objects.create(
        text=text,
        is_offensive=analysis['is_offensive'],
        severity=analysis['severity'],
        confidence_score=analysis['confidence_score'],
        categories=analysis['categories'],
        flagged_terms=analysis['flagged_terms'],
        emoji_detections=analysis['emoji_detections'],
        mode=analysis['mode'],
    )

    return JsonResponse(analysis)
