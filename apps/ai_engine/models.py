from django.db import models

class KnowledgeChunk(models.Model):
    CATEGORY_CHOICES = [
        ('staff_assistance', 'Staff Assistance'),
        ('website_navigation', 'Website Navigation'),
        ('pms_workflow', 'PMS Workflow'),
        ('general_faq', 'General FAQ'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='pms_workflow')
    source_doc = models.CharField(max_length=255, default='SRS-PMS_Retrod')
    embedding_json = models.JSONField(null=True, blank=True, help_text="Stored vector embedding list")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} [{self.category}]"
