from django.contrib import admin
from .models import AnalysisResult


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('analyzed_at', 'severity', 'is_offensive', 'confidence_score')
    list_filter = ('severity', 'is_offensive', 'analyzed_at')
    search_fields = ('text',)
    readonly_fields = ('analyzed_at', 'text', 'is_offensive', 'severity', 'confidence_score', 'categories', 'flagged_terms')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
