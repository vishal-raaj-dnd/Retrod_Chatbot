import os
import docx
from django.core.management.base import BaseCommand
from apps.ai_engine.models import KnowledgeChunk
from apps.ai_engine.ingest_routes import ROUTES_DATA, BASE_URL

class Command(BaseCommand):
    help = 'Ingests both SRS Specification document and Website Navigation Routes into the Knowledge base.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting Knowledge Base Ingestion..."))

        # 1. Ingest SRS Document
        doc_path = "Software Requirements Specification (SRS)-PMS_Retrod - Anushka (1).docx"
        if os.path.exists(doc_path):
            doc = docx.Document(doc_path)
            KnowledgeChunk.objects.filter(source_doc="SRS-PMS_Retrod").delete()
            
            current_title = "PMS Retrod Overview"
            current_chunk = []
            srs_count = 0

            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if not text:
                    continue

                if paragraph.style.name.startswith("Heading") or (len(text) < 60 and text.isupper()):
                    if current_chunk:
                        full_text = "\n".join(current_chunk)
                        if len(full_text) > 30:
                            KnowledgeChunk.objects.create(
                                title=current_title,
                                content=full_text,
                                category='staff_assistance' if 'staff' in current_title.lower() else 'pms_workflow',
                                source_doc="SRS-PMS_Retrod"
                            )
                            srs_count += 1
                        current_chunk = []
                    current_title = text
                else:
                    current_chunk.append(text)

            if current_chunk:
                full_text = "\n".join(current_chunk)
                if len(full_text) > 30:
                    KnowledgeChunk.objects.create(
                        title=current_title,
                        content=full_text,
                        category='pms_workflow',
                        source_doc="SRS-PMS_Retrod"
                    )
                    srs_count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully ingested {srs_count} SRS Document chunks."))
        else:
            self.stdout.write(self.style.WARNING(f"SRS Document '{doc_path}' not found."))

        # 2. Ingest Website Routes
        KnowledgeChunk.objects.filter(source_doc="Website_Routes").delete()
        route_count = 0

        for item in ROUTES_DATA:
            full_url = f"{BASE_URL}{item['route']}"
            title = f"Route: {item['feature']} ({item['route']})"
            content = (
                f"Page Name: {item['feature']}\n"
                f"Direct Page URL: {full_url}\n"
                f"Relative Route: {item['route']}\n"
                f"Required Permission: {item['perm']}\n"
                f"Description: {item['desc']}"
            )

            KnowledgeChunk.objects.create(
                title=title,
                content=content,
                category="website_navigation",
                source_doc="Website_Routes"
            )
            route_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully ingested {route_count} Website Navigation Routes."))
        self.stdout.write(self.style.SUCCESS("All Knowledge Base Ingestion Completed!"))
