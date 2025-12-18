from django.db import models


class AnalysisResult(models.Model):
    SEVERITY_CHOICES = [
        ('safe', 'Safe'),
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]
    
    text = models.TextField()
    is_offensive = models.BooleanField(default=False)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='safe')
    confidence_score = models.FloatField(default=0.0)
    categories = models.JSONField(default=list)
    flagged_terms = models.JSONField(default=list)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-analyzed_at']
    
    def __str__(self):
        return f"Analysis at {self.analyzed_at} - {'Offensive' if self.is_offensive else 'Safe'}"
