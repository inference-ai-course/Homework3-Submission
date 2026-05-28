# Week 3 Project Update: Pretraining Data & Voice Agents

## Project Description

I just started a capstone project where I'm building a semiconductor focus application that helps engineers quickly find relevant information from technical documents, research papers, and web sources. The goal is to create a tool that can extract key insights, summarize findings, and provide voice-based interactions for users who are on the go.

## Data Pipeline Strategy

# Data Pipeline Strategy: Semiconductor Intelligence Tool

## Executive Summary

You're building a **Retrieval-Augmented Generation (RAG) system** specialized for semiconductor engineering. Your pipeline needs to handle highly technical content with precise terminology, equations, and structured data (tables, figures, specs). Here's a concrete, buildable strategy.

---

## 1. Data Sources

### Primary Sources (High Priority)

```
Semiconductor Knowledge Base
¢u¢w¢w Technical PDFs
¢x   ¢u¢w¢w Datasheets (Texas Instruments, Infineon, STMicro portals)
¢x   ¢u¢w¢w Application Notes (vendor websites)
¢x   ¢u¢w¢w IEEE Xplore papers (if licensed) or arXiv EE section
¢x   ¢|¢w¢w JEDEC/IEC standards documents
¢x
¢u¢w¢w Web Sources
¢x   ¢u¢w¢w Electronics Stack Exchange (Q&A gold mine)
¢x   ¢u¢w¢w SemiWiki.com (industry blog/forum)
¢x   ¢u¢w¢w EETimes.com (news + technical articles)
¢x   ¢u¢w¢w Vendor documentation sites (TI.com/docs, Microchip docs)
¢x   ¢|¢w¢w Wikipedia semiconductor category (baseline concepts)
¢x
¢|¢w¢w Audio/Video (Optional Phase 2)
    ¢u¢w¢w Conference talks (ISSCC, Hot Chips on YouTube)
    ¢|¢w¢w Vendor webinars
```

### Why These Sources Specifically
- **Datasheets** = dense, structured, domain-specific ground truth
- **App Notes** = practical engineering context, real use cases
- **Stack Exchange** = natural language Q&A pairs (perfect for RAG training data)
- **arXiv cs.AR + eess.SP** = free, current research without paywalls

---

## 2. Extraction Tools by Content Type

### Decision Matrix

```
Content Type          Tool              Why This Choice
¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w¢w
Clean web articles    trafilatura       Fast, removes boilerplate well
JavaScript-heavy      Crawl4AI          Handles dynamic vendor portals
Simple PDFs           PyMuPDF (fitz)    Fastest, preserves structure
Complex PDFs          Docling           Best for tables + equations
Scanned datasheets    Marker            Better than Tesseract for tech docs
Audio transcription   faster-whisper    Local, accurate on technical terms
```

### Concrete Tool Configuration

```python
# PDF extraction pipeline - use tiered approach
import fitz  # PyMuPDF
from docling.document_converter import DocumentConverter

def extract_pdf(filepath: str) -> dict:
    """
    Tier 1: Try PyMuPDF first (fast)
    Tier 2: Fall back to Docling if tables/figures detected
    """
    doc = fitz.open(filepath)
    
    # Heuristic: check if document has complex layout
    has_tables = any(
        len(page.find_tables().tables) > 0 
        for page in doc

## Mini Pipeline Results

- Documents collected: 5
- Documents after cleaning: 5

## Reflections

### Data Strategy
[YOUR REFLECTION HERE]

- Which data sources are most relevant for your project?
- I think the most useful extraction tools for my domain will be web scraping for technical documents and research papers like IEEE, and OCR for any scanned PDFs. ASR might be less critical unless I want to include audio sources.
- Which tools from this week will you actually use in your capstone?
- I think I'll primarily use trafilatura for web scraping, Tesseract for OCR, and MinHash for deduplication. I might experiment with faster-whisper for ASR if I find relevant audio content.
- What's the most challenging data quality issue you expect to face?
- I anticipate that a major data quality issue will be dealing with noisy and unstructured data from web sources. Ensuring that I can extract clean, relevant information without too much irrelevant content will be a challenge.

### Pipeline Execution
[YOUR REFLECTION HERE]

- What data did you collect and how did you clean it?
- I collected abstracts of research papers related to semiconductor manufacturing from arXiv. I then ran a cleaning pipeline that included language detection, deduplication using MinHash, and quality filtering to remove any low-quality or irrelevant abstracts.
- Were any documents removed by the pipeline? Why?
- No documents were removed during the quality filtering step due to low relevance or poor text quality.
- How would you scale this to a full dataset for your project?
- To scale this to a full dataset, I would set up an automated pipeline that continuously scrapes new papers from relevant sources like arXiv, IEEE, and other research databases. I would also implement more robust error handling and monitoring to ensure the pipeline runs smoothly. Additionally, I might consider parallelizing the scraping and cleaning processes to handle larger volumes of data more efficiently.

## Tools I Plan to Use

Trafilatura, Tesseract, MinHash, and possibly faster-whisper for ASR.

## Next Steps

I will continue refining my data pipeline, potentially adding more sources and improving the cleaning steps. I also want to start exploring how to integrate voice capabilities into my project, perhaps by prototyping a simple voice agent using Pipecat.
