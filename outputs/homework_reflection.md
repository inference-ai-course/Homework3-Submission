
## Notebook 01: Environment Setup

**Completed:** 2026-05-26 10:55:05

### Path Selection

[YOUR REFLECTION HERE]

- Why did you choose Path A/B/C?
- What trade-offs did you consider (cost vs. speed vs. flexibility)?
- Have you used Ollama before? If so, how does it compare to cloud APIs?

---

## Notebook 01: Environment Setup

**Completed:** 2026-05-26 11:05:08

### Path Selection

[YOUR REFLECTION HERE]

- Why did you choose Path A/B/C?
- What trade-offs did you consider (cost vs. speed vs. flexibility)?
- Have you used Ollama before? If so, how does it compare to cloud APIs?

---

## Notebook 01: Environment Setup

**Completed:** 2026-05-26 22:25:35

### Path Selection

[YOUR REFLECTION HERE]

- Why did you choose Path A/B/C?
- I chose Path A becuase I want to try out online API and I think it's more convenient to use cloud API than local model. And I also want to compare the quality and speed of cloud API and local model.
- What trade-offs did you consider (cost vs. speed vs. flexibility)?
- Sometimes, Claude can get a more consistent result than local model, especially when it comes to tool calling. But local model can be more flexible and cost-effective if you have the right hardware and you don't need to call tools. So I think it's a trade-off between quality and cost/speed.
- Have you used Ollama before? If so, how does it compare to cloud APIs?
- Yes, I have used Ollama for other application before. And I think the main differnece is the quality and time. Somethimes, local model cann't get a consistent result and when it comes to tool calling it's a big problem unless I upgrade my hardware to aford 27B model.

---

## Notebook 02: Web Scraping & Text Extraction

**Completed:** 2026-05-26 23:09:09

### Part 1 - trafilatura Extraction

[YOUR REFLECTION HERE]

- What URL did you choose and why?
- I choose wikipedia page about large language models, because it is a topic of interest to me and I wanted to see how well trafilatura can extract information from a structured page with multiple sections.
- How well did trafilatura extract the main content?
- Because it's extracted from wiki and I think the quality is pretty good. And the main reason I think is that wiki is always extracted as training data for LLM so trafilatura is likely optimized for it.
- Were there any missing or incorrect parts in the extraction?
- I think the extraction is pretty good, but there are some missing parts such as the references and the infobox on the right side of the page. However, the main content of the article is well preserved.

---

### Part 2 - Crawl4AI vs trafilatura

[YOUR REFLECTION HERE]

- Which extractor produced better output for your test URLs?
- I think Crawl4AI produced better output for the arXiv page because it preserved the structure and formatting of the original page, which is important for understanding the content. However, for the blog post, trafilatura did a decent job of extracting the main text, but it lost some of the formatting and structure that could be useful for downstream tasks.
- For what types of pages would you prefer Crawl4AI over trafilatura?
- I would prefer Crawl4AI for pages that have a lot of structure, such as research papers, documentation, or any page where the formatting (headings, lists, code blocks) is important for understanding the content. For simpler pages or when I just need the main text without formatting, trafilatura might be sufficient.
- How does output format (plain text vs Markdown) affect downstream LLM usage?
- The output format can significantly affect downstream LLM usage. Plain text is simpler and may be sufficient for tasks that only require the main content, but it loses important structural information that can help the LLM understand the context and relationships between different parts of the text. Markdown, on the other hand, preserves this structure, which can improve the performance of the LLM on tasks like summarization, question answering, or any task that benefits from understanding the hierarchy and formatting of the content.

---

### Part 3 - arXiv Paper Dataset

[YOUR REFLECTION HERE]

- What topic did you choose and why?
- I chose Electrical Engineering because it is a broad field with many subtopics, and I wanted to see what kind of papers are being published recently in this area. I am particularly interested in how electrical engineering intersects with AI and machine learning, so I wanted to find papers that might touch on those themes.
- Were you surprised by any of the papers found?
- I was surprised to find some papers that applied machine learning techniques to traditional electrical engineering problems, such as signal processing and circuit design. It shows how interdisciplinary the field is becoming, and how AI is influencing even areas that are not traditionally associated with it.
- How could this scraping approach scale to build a real pretraining dataset?
- This scraping approach could be scaled by automating the process to scrape a large number of papers across multiple topics and categories on arXiv. We could set up a pipeline that regularly scrapes new papers, extracts the relevant text (abstracts, introductions), and formats it for LLM pretraining. Additionally, we could use metadata (authors, publication date, categories) to organize the dataset and potentially filter for higher-quality or more relevant papers.

---

## Notebook 03: Document OCR & PDF Extraction

**Completed:** 2026-05-27 00:11:50

### Part 1 - Tesseract OCR Quality

[YOUR REFLECTION HERE]

- What text did Tesseract extract correctly?
- Most of the main text was extracted correctly, including the steps and the general layout. The line breaks were preserved, which helps maintain the structure of the content.
- Were there any errors, missing text, or ordering issues?
- Lift top part of image is dark so the text is not extracted correctly. Also, some of the smaller text at the bottom is not extracted well, likely due to the font size and contrast.
- For what types of documents would Tesseract be sufficient?
- Tesseract would be sufficient for documents that have clear, high-contrast text and a simple layout. It works well for scanned documents, printed materials, and images with minimal noise. However, it may struggle with complex layouts, low-quality images, or documents with a lot of formatting (e.g., tables, multi-column layouts).

---

### Part 2 - OCR Tool Comparison

[YOUR REFLECTION HERE]

- Which tool would you choose for your capstone project's document processing needs?
- I want to use Marker for my capstone project because it is designed to handle complex PDFs and can convert them into Markdown format, which is ideal for feeding into an LLM. Its ability to preserve layout and handle tables and code makes it a strong choice for high-quality data extraction.
- How has OCR technology evolved from Tesseract to Marker/Docling?
- OCR technology has evolved significantly from Tesseract, which was primarily focused on basic text extraction from images, to modern tools like Marker and Docling that are designed to handle complex document formats and preserve layout. Tesseract is a general-purpose OCR engine that can struggle with complex layouts and formatting, while Marker and Docling are built to extract structured data from PDFs and other document types, making them more suitable for LLM pretraining pipelines.
- What role does layout awareness play in extraction quality?
- Layout awareness is crucial for extraction quality because it helps preserve the structure and formatting of the original document. This is especially important for complex documents that contain tables, multi-column layouts, images, and code snippets. Tools that are layout-aware can maintain the context and relationships between different elements in the document, which leads to higher-quality data for LLM training. In contrast, tools that lack layout awareness may produce jumbled or incomplete text, reducing the usefulness of the extracted data.

---

## Notebook 04: Speech Recognition (ASR)

**Completed:** 2026-05-27 22:43:59

### Part 1 - ASR in Pretraining

[YOUR REFLECTION HERE]

- How does ASR transcription quality compare to web-scraped text?
- I think ASR transcription quality can vary widely based on the model used, the audio quality, and the speaker's accent. While web-scraped text is often cleaner and more structured, ASR transcriptions can contain errors, misheard words, and lack punctuation. However, modern ASR models like Whisper v3 turbo have made significant improvements in accuracy, especially for clear audio. Post-processing steps such as punctuation restoration and error correction can help improve the quality of ASR text before it is used in training datasets.
- Which model size would you choose for transcribing 1000 hours of podcasts?
- I will chose the "base" model size for transcribing 1000 hours of podcasts. The "tiny" model may be too inaccurate for large-scale transcription, while the "small" model may be unnecessarily slow and resource-intensive. The "base" model offers a good balance of speed and accuracy, making it suitable for processing a large volume of audio data efficiently while maintaining reasonable transcription quality.
- What are the ethical considerations of transcribing public audio content?
- Ethical considerations include respecting privacy and consent, especially if the audio contains personal or sensitive information. Even if the content is publicly available, it may not be ethical to transcribe and use it without permission from the speakers. There is also the risk of misrepresentation if the ASR transcription contains errors, which could lead to misinformation or harm to individuals. Additionally, there may be copyright issues when transcribing and using content from podcasts or YouTube videos, so it's important to ensure that the content is used in compliance with copyright laws and platform policies.

---

### Part 2 - Custom Transcription

[YOUR REFLECTION HERE]

- What audio did you transcribe?
- I transcribed a podcast episode titled "DevFest 2025 Recap," which is a summary of the key highlights and announcements from the DevFest 2025 conference.
- How accurate was the transcription?
- The accuracy of the transcription was quite good, especially for clear sections of the audio. However, there were some errors in transcribing technical terms and names, which is a common issue with ASR. Overall, the transcription captured the main content of the podcast, but it may require some manual correction for specific details.
- What would you change for better results (model size, preprocessing)?
- For better results, I might experiment with the "base" model size to see if it improves accuracy, especially for technical terms. Additionally, I could apply some preprocessing to enhance the audio quality, such as noise reduction or normalization, which might help the ASR model perform better. Post-processing the transcription with a tool that corrects common ASR errors or restores punctuation could also improve the readability and usefulness of the transcribed text.

---

## Notebook 05: Data Cleaning Pipeline

**Completed:** 2026-05-27 22:51:42

### Part 1 - Pipeline Stage Analysis

[YOUR REFLECTION HERE]

- Which cleaning stage removed the most documents? Why?
- Filter stage removed the most documents because it identified non-English text that did not meet the target language criteria. This is a common issue when working with web-scraped data, which often contains multilingual content. The language filter is designed to ensure that only relevant language data is retained for training, which can lead to a significant reduction in dataset size if there is a lot of non-target language content.
- Were there any false positives (good content incorrectly removed)?
- Yes, the language filter may have removed some documents that contained a mix of English and non-English text, or documents that were primarily in English but had some non-English phrases. Additionally, the deduplication stage might have removed documents that were similar but not identical, which could be considered false positives if those documents contained unique information.
- How would you adjust the deduplication threshold for different use cases?
- For a use case that requires high precision and can tolerate some duplicates, I would set a higher threshold (e.g., 0.8 or 0.9) to ensure that only very similar documents are removed. For a use case that prioritizes dataset size reduction and can tolerate some loss of unique content, I would set a lower threshold (e.g., 0.6 or 0.7) to remove more documents that are somewhat similar.

---

### Part 2 - Scaling with DataTrove

[YOUR REFLECTION HERE]

- What additional cleaning steps would you add to your pipeline?
- I would consider adding a quality filtering stage that removes documents that are too short, have low word counts, or contain a high ratio of non-alphanumeric characters. Additionally, I might implement a stage to detect and remove boilerplate content (e.g., navigation menus, footers) using heuristics or machine learning models trained on labeled data.
- How would you handle the scale difference between 10 documents and 10 billion?
- To handle the scale difference, I would leverage distributed computing frameworks like Apache Spark or Dask to parallelize the cleaning process across a cluster of machines. For MinHash deduplication, I would partition the dataset into smaller chunks and compute MinHash signatures in parallel, then use a distributed hash table to identify and remove duplicates across partitions. Additionally, I would consider using more efficient data storage formats (e.g., Parquet) and streaming processing to handle the large volume of data without needing to load it all into memory at once.
- What was the most surprising thing you learned about DataTrove/FineWeb?
- DataTrove's use of a multi-stage deduplication process that combines both exact and approximate methods was particularly interesting, as it allows for more efficient processing of large datasets while still maintaining high-quality results. FineWeb's emphasis on quality filtering and the use of machine learning models to identify low-quality content was also a surprising and insightful approach to improving the overall quality of the training data.

---

## Notebook 05: Data Cleaning Pipeline

**Completed:** 2026-05-27 22:52:03

### Part 1 - Pipeline Stage Analysis

[YOUR REFLECTION HERE]

- Which cleaning stage removed the most documents? Why?
- Filter stage removed the most documents because it identified non-English text that did not meet the target language criteria. This is a common issue when working with web-scraped data, which often contains multilingual content. The language filter is designed to ensure that only relevant language data is retained for training, which can lead to a significant reduction in dataset size if there is a lot of non-target language content.
- Were there any false positives (good content incorrectly removed)?
- Yes, the language filter may have removed some documents that contained a mix of English and non-English text, or documents that were primarily in English but had some non-English phrases. Additionally, the deduplication stage might have removed documents that were similar but not identical, which could be considered false positives if those documents contained unique information.
- How would you adjust the deduplication threshold for different use cases?
- For a use case that requires high precision and can tolerate some duplicates, I would set a higher threshold (e.g., 0.8 or 0.9) to ensure that only very similar documents are removed. For a use case that prioritizes dataset size reduction and can tolerate some loss of unique content, I would set a lower threshold (e.g., 0.6 or 0.7) to remove more documents that are somewhat similar.

---

### Part 2 - Scaling with DataTrove

[YOUR REFLECTION HERE]

- What additional cleaning steps would you add to your pipeline?
- I would consider adding a quality filtering stage that removes documents that are too short, have low word counts, or contain a high ratio of non-alphanumeric characters. Additionally, I might implement a stage to detect and remove boilerplate content (e.g., navigation menus, footers) using heuristics or machine learning models trained on labeled data.
- How would you handle the scale difference between 10 documents and 10 billion?
- To handle the scale difference, I would leverage distributed computing frameworks like Apache Spark or Dask to parallelize the cleaning process across a cluster of machines. For MinHash deduplication, I would partition the dataset into smaller chunks and compute MinHash signatures in parallel, then use a distributed hash table to identify and remove duplicates across partitions. Additionally, I would consider using more efficient data storage formats (e.g., Parquet) and streaming processing to handle the large volume of data without needing to load it all into memory at once.
- What was the most surprising thing you learned about DataTrove/FineWeb?
- DataTrove's use of a multi-stage deduplication process that combines both exact and approximate methods was particularly interesting, as it allows for more efficient processing of large datasets while still maintaining high-quality results. FineWeb's emphasis on quality filtering and the use of machine learning models to identify low-quality content was also a surprising and insightful approach to improving the overall quality of the training data.

---

## Notebook 06: Text-to-Speech & Voice Synthesis

**Completed:** 2026-05-27 23:30:51

### Part 1 - TTS Synthesis

[YOUR REFLECTION HERE]

- How natural did the synthesized speech sound?
- It was surprisingly natural, with clear pronunciation and appropriate intonation. The voice had a conversational tone that made it easy to listen to.
- Which voice did you prefer and why?
- I preferred the 'en-US-AriaNeural' voice because it had a clear and pleasant tone that was easy to understand.
- What are the limitations of cloud-based TTS like edge-tts?
- One limitation is that it requires an internet connection, which may not be ideal in all situations. Additionally, there may be latency issues when synthesizing longer texts, and there could be costs associated with high usage.

---

### Part 2 - Voice Agent TTS Architecture

[YOUR REFLECTION HERE]

- Which TTS model would you choose for your voice agent project?
- I would choose Kokoro for my voice agent project because it offers a good balance of natural-sounding speech and low latency, which is crucial for real-time interactions. While edge-tts is a viable option, the network latency could be a bottleneck
- What's the biggest latency bottleneck in a voice pipeline (ASR vs LLM vs TTS)?
- The biggest latency bottleneck is often the LLM, especially if it's a large model running on CPU. ASR can also be slow, but there are optimized models for that. TTS can be fast with local models like Kokoro, but cloud-based TTS like edge-tts can introduce significant latency due to network round trips.
- How does edge-tts compare to local models like Kokoro for real-time use?
- Edge-tts can be a good option for non-real-time applications or where internet access is reliable, but for real-time voice agents, the latency introduced by network calls can degrade the user experience. Local models like Kokoro provide more consistent low latency, which is essential for maintaining a natural conversational flow.

---

## Notebook 07: Voice Agent with Pipecat

**Completed:** 2026-05-27 23:45:41

### Part 1 - Custom Voice Agent

[YOUR REFLECTION HERE]

- Did the agent maintain context across turns?
- Yes, the agent was able to build on previous questions and provide coherent responses that related to the earlier parts of the conversation. Each response referenced concepts introduced in the user's questions, showing that it maintained context effectively.
- What persona did you choose and how well did it work?
- I chose a persona of a friendly and knowledgeable tutor who explains complex topics in simple terms. This persona worked well for the conversation, as the responses were clear, concise, and built on the user's questions in a way that felt natural and helpful.
- What would you change to make the conversation more natural?
- I would try to make the responses even more conversational and less formal, perhaps by adding more natural language elements or by making the tone more casual. Additionally, I might experiment with different system prompts to see if I can encourage the model to generate responses that feel more like a real conversation rather than a structured explanation.

---

### Part 2 - Production Architecture

[YOUR REFLECTION HERE]

- Would you use Pipecat or build your own FastAPI voice server? Why?
- I would likely choose to use Pipecat for a production-ready voice agent, especially if I want to leverage its built-in features like WebRTC transport, VAD, and turn detection. Pipecat is designed specifically for orchestrating complex pipelines and handling real-time interactions, which would save a significant amount of development time compared to building a custom FastAPI server from scratch. Additionally, Pipecat's handling of interruptions (where the user can speak while the bot is still talking) is a crucial feature for creating a natural conversational experience, and implementing this manually would require additional effort and complexity.
- What's the most challenging part of building a real-time voice agent?
- The most challenging part is likely handling the real-time nature of voice interactions, especially managing latency and ensuring that the system can respond quickly enough to maintain a natural conversation flow. This includes optimizing the ASR and TTS components for speed, as well as designing the system to handle interruptions gracefully.
- How would you handle the case where the user interrupts the bot mid-sentence?
- Pipecat handles interruptions using its turn detection and VAD features. If the user starts speaking while the bot is still talking, Pipecat can detect this and immediately pause the TTS output, allowing the user's input to take precedence. Once the user finishes speaking, Pipecat can then resume or restart the TTS response as needed. This creates a more natural conversational flow, as it allows for dynamic interactions without forcing the user to wait for the bot to finish before responding.

---

## Notebook 08: Project Integration

**Completed:** 2026-05-28 00:27:37

### Data Pipeline Strategy

[YOUR REFLECTION HERE]

- Which data sources are most relevant for your project?
- I think the most useful extraction tools for my domain will be web scraping for technical documents and research papers like IEEE, and OCR for any scanned PDFs. ASR might be less critical unless I want to include audio sources.
- Which tools from this week will you actually use in your capstone?
- I think I'll primarily use trafilatura for web scraping, Tesseract for OCR, and MinHash for deduplication. I might experiment with faster-whisper for ASR if I find relevant audio content.
- What's the most challenging data quality issue you expect to face?
- I anticipate that a major data quality issue will be dealing with noisy and unstructured data from web sources. Ensuring that I can extract clean, relevant information without too much irrelevant content will be a challenge.

---

### Mini Pipeline Results

[YOUR REFLECTION HERE]

- What data did you collect and how did you clean it?
- I collected abstracts of research papers related to semiconductor manufacturing from arXiv. I then ran a cleaning pipeline that included language detection, deduplication using MinHash, and quality filtering to remove any low-quality or irrelevant abstracts.
- Were any documents removed by the pipeline? Why?
- Yes, some documents were removed during the quality filtering step due to low relevance or poor text quality.
- How would you scale this to a full dataset for your project?
- To scale this to a full dataset, I would set up an automated pipeline that continuously scrapes new papers from relevant sources like arXiv, IEEE, and other research databases. I would also implement more robust error handling and monitoring to ensure the pipeline runs smoothly. Additionally, I might consider parallelizing the scraping and cleaning processes to handle larger volumes of data more efficiently.

---

## Notebook 08: Project Integration

**Completed:** 2026-05-28 00:37:10

### Data Pipeline Strategy

[YOUR REFLECTION HERE]

- Which data sources are most relevant for your project?
- I think the most useful extraction tools for my domain will be web scraping for technical documents and research papers like IEEE, and OCR for any scanned PDFs. ASR might be less critical unless I want to include audio sources.
- Which tools from this week will you actually use in your capstone?
- I think I'll primarily use trafilatura for web scraping, Tesseract for OCR, and MinHash for deduplication. I might experiment with faster-whisper for ASR if I find relevant audio content.
- What's the most challenging data quality issue you expect to face?
- I anticipate that a major data quality issue will be dealing with noisy and unstructured data from web sources. Ensuring that I can extract clean, relevant information without too much irrelevant content will be a challenge.

---

### Mini Pipeline Results

[YOUR REFLECTION HERE]

- What data did you collect and how did you clean it?
- I collected abstracts of research papers related to semiconductor manufacturing from arXiv. I then ran a cleaning pipeline that included language detection, deduplication using MinHash, and quality filtering to remove any low-quality or irrelevant abstracts.
- Were any documents removed by the pipeline? Why?
- No documents were removed during the quality filtering step due to low relevance or poor text quality.
- How would you scale this to a full dataset for your project?
- To scale this to a full dataset, I would set up an automated pipeline that continuously scrapes new papers from relevant sources like arXiv, IEEE, and other research databases. I would also implement more robust error handling and monitoring to ensure the pipeline runs smoothly. Additionally, I might consider parallelizing the scraping and cleaning processes to handle larger volumes of data more efficiently.

---
