
## Notebook 01: Environment Setup

**Completed:** 2026-04-15 17:03:45

### Path Selection

I chose Path B because I have access to both cloud APIs and Ollama, and I want the flexibility to compare them. Path A would limit me to only cloud APIs, while Path C would restrict me to Ollama. By choosing Path B, I can evaluate the trade-offs between cost, speed, and flexibility across both options.
Compare to Path A, I can potentially save costs by using Ollama for smaller tasks or experimentation, while leveraging cloud APIs for larger or more complex queries. Compared to Path C, I can access a wider range of models and features available in the cloud, which may not be present in Ollama. Overall, Path B offers the best balance for my needs in this assignment.
- Why did you choose Path A/B/C?
- What trade-offs did you consider (cost vs. speed vs. flexibility)?
- Have you used Ollama before? If so, how does it compare to cloud APIs?

---

## Notebook 02: Web Scraping & Text Extraction

**Completed:** 2026-04-17 09:59:46

### Part 1 - trafilatura Extraction

[YOUR REFLECTION HERE]
This url is a news article about a celebrity's life story. It is a dynamic page with a lot of images and ads and lazy loading content
It did extract some content, but it missed a lot of the main text and included some irrelevant parts like ads and image captions. The extracted text was also somewhat jumbled and not well-structured.

---

### Part 2 - Crawl4AI vs trafilatura

[YOUR REFLECTION HERE]
trafilatura trturns clean plain text without majoy issues for simple static page, 
but for javascript heavy dynamic pages it can miss some the main content.
Crawl4AI keeps some structure and can capture more content, 
but it may be slower and produce more verbose output.
For LLM usage, structured md type output can be more useful.

---

### Part 3 - arXiv Paper Dataset

[YOUR REFLECTION HERE]
I picked AI safety and robotics, 
I wanted to see what recent papers are saying about the intersection of these fields and what the current research trends are. I was surprised that there were a lot of papers on using LLMs for robotics control and safety monitoring, 
which seems like a hot area right now. To scale this scraping approach for a real pretraining dataset, you would need to automate the process across many topics and sources, handle rate limits and CAPTCHAs, and implement robust error handling and data cleaning pipelines to ensure high-quality text extraction at scale.
I do this scraping approach can be a good way to build a focused pretraining dataset on specific research areas, but it would require significant engineering effort to scale and maintain over time. 
- What topic did you choose and why?
- Were you surprised by any of the papers found?
- How could this scraping approach scale to build a real pretraining dataset?

---

## Notebook 03: Document OCR & PDF Extraction

**Completed:** 2026-04-17 11:46:49

### Part 1 - Tesseract OCR Quality

[YOUR REFLECTION HERE]
The main context is correctly extracted, but some info are missing.
Alll these missing info are the had strong colour background, which may cause the OCR model to fail to extract them.
I guess for plain backgroud, Tesseract can work well, but for more complex background, it may fail to extract the text correctly.
- What text did Tesseract extract correctly?
- Were there any errors, missing text, or ordering issues?
- For what types of documents would Tesseract be sufficient?

---

### Part 2 - OCR Tool Comparison

[YOUR REFLECTION HERE]
Tesseract is good, but it may fail to extract text correctly when the background is complex.
EasyOCR is better  than Tesseract, it can handle more languages and has better accuracy, but it may still struggle with very complex layouts or low-quality scans.
Marker, I don't know. I tried Marker several times, but it crashed every time, I didn't see result from it.
Docling is faster and better result.
If I need to extract text from simple scanned documents, I will use docling.

---

## Notebook 04: Speech Recognition (ASR)

**Completed:** 2026-04-17 12:28:54

### Part 1 - ASR in Pretraining

[YOUR REFLECTION HERE]
ASR transcription quality is worse than web-scraped text
FASTER-WHISPER seems better.
Definitely, quality of ASR transcriptions.
- How does ASR transcription quality compare to web-scraped text?
- Which model size would you choose for transcribing 1000 hours of podcasts?
- What are the ethical considerations of transcribing public audio content?

---

### Part 2 - Custom Transcription

[YOUR REFLECTION HERE]
I used sample-3, it loooks good, but there are some errors in the transcription, maybe because of the background noise.
- What audio did you transcribe?
- How accurate was the transcription?
- What would you change for better results (model size, preprocessing)?

---

## Notebook 05: Data Cleaning Pipeline

**Completed:** 2026-04-17 13:51:23

### Part 1 - Pipeline Stage Analysis

[YOUR REFLECTION HERE]
Mininhash deduplication removed one document, because two documents are very similar, they have the same content except for a few words. 
I think the threshold is good for this dataset, but for larger datasets with more variation, I might want to lower it to 0.6 or 0.5 to catch more duplicates.

- Which cleaning stage removed the most documents? Why?
- Were there any false positives (good content incorrectly removed)?
- How would you adjust the deduplication threshold for different use cases?

---

### Part 2 - Scaling with DataTrove

[YOUR REFLECTION HERE]
Addtional cleaning steps I would add to my pipeline include:
    -  HTML entity normalization 
    -  JavaScript content removal
    -  Regular expression for PII

Tos scale to billions of documents, I would:
- Use distributed processing frameworks like Spark or Dask to parallelize the cleaning steps across a cluster
- For MinHash deduplication, I would partition the dataset into smaller chunks, compute MinHash signatures for each chunk, 
  and then use a distributed join to find duplicates across chunks. 

I think DataTrove/FineWeb can handle many cases of noise and duplication at scale, but it might need large amount of
resources like memory, computing capacity. 

- What additional cleaning steps would you add to your pipeline?
- How would you handle the scale difference between 10 documents and 10 billion?
- What was the most surprising thing you learned about DataTrove/FineWeb?

---

## Notebook 06: Text-to-Speech & Voice Synthesis

**Completed:** 2026-04-17 14:17:00

### Part 1 - TTS Synthesis

[YOUR REFLECTION HERE]
The sound is good, almost the same as human voice.
I like AriaNeural, it sounds more natural.
I think emotion is the limitation of cloud-based TTS, it may sound robotic and lack emotional expression.
- How natural did the synthesized speech sound?
- Which voice did you prefer and why?
- What are the limitations of cloud-based TTS like edge-tts?

---

### Part 2 - Voice Agent TTS Architecture

[YOUR REFLECTION HERE]
Kokoro sounds better, but it took long time to synthesize. 
If I use it in voice agent, the latency may be too high, it may cause bad user experience.
Edge-tts is good enough for applications.
- Which TTS model would you choose for your voice agent project?
- What's the biggest latency bottleneck in a voice pipeline (ASR vs LLM vs TTS)?
- How does edge-tts compare to local models like Kokoro for real-time use?

---

## Notebook 07: Voice Agent with Pipecat

**Completed:** 2026-04-17 15:03:57

### Part 1 - Custom Voice Agent

[YOUR REFLECTION HERE]
Agent did maintain context across turns.
I ask the agent to be a tutor, and it did well.
I'd like to makethe persona more specific.
- Did the agent maintain context across turns?
- What persona did you choose and how well did it work?
- What would you change to make the conversation more natural?

---

### Part 2 - Production Architecture

[YOUR REFLECTION HERE]
I don't have experience with Pipecat, but as a framework it likely abstracts away a lot of the complexities of building a voice agent. I will try later.
It's mature technology anf easy to implement.
Stop the botwaiting for the user to finish speaking.
- Would you use Pipecat or build your own FastAPI voice server? Why?
- What's the most challenging part of building a real-time voice agent?
- How would you handle the case where the user interrupts the bot mid-sentence?

---
