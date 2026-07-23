import os
import sys
import docx

# Add project root directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrod_backend.settings')
django.setup()


from apps.ai_engine.models import KnowledgeChunk

DOC_PATH = "Software Requirements Specification (SRS)-PMS_Retrod - Anushka (1).docx"

def ingest_srs_docx():
    """
    Parses the SRS .docx document, extracts headings and paragraphs,
    and stores them as KnowledgeChunk records in the database.
    """
    if not os.path.exists(DOC_PATH):
        print(f"Error: {DOC_PATH} not found.")
        return

    print(f"Reading document: {DOC_PATH}...")
    doc = docx.Document(DOC_PATH)

    current_title = "PMS Retrod Overview"
    current_chunk = []
    created_count = 0

    # Clear old SRS chunks before ingesting
    KnowledgeChunk.objects.filter(source_doc="SRS-PMS_Retrod").delete()

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        # Check if heading
        if paragraph.style.name.startswith("Heading") or len(text) < 60 and text.isupper():
            if current_chunk:
                full_text = "\n".join(current_chunk)
                if len(full_text) > 30:
                    KnowledgeChunk.objects.create(
                        title=current_title,
                        content=full_text,
                        category='staff_assistance' if 'staff' in current_title.lower() else 'pms_workflow',
                        source_doc="SRS-PMS_Retrod"
                    )
                    created_count += 1
                current_chunk = []
            current_title = text
        else:
            current_chunk.append(text)

    # Save remaining chunk
    if current_chunk:
        full_text = "\n".join(current_chunk)
        if len(full_text) > 30:
            KnowledgeChunk.objects.create(
                title=current_title,
                content=full_text,
                category='pms_workflow',
                source_doc="SRS-PMS_Retrod"
            )
            created_count += 1

    print(f"Successfully ingested {created_count} Knowledge Chunks into database!")

if __name__ == "__main__":
    ingest_srs_docx()
