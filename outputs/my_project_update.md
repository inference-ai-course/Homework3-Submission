# Week 3 Project Update: Pretraining Data & Voice Agents

## Project Description

The vacation Planer will take user's request and suggest best vacation plan.

## Data Pipeline Strategy

Based on your project goal of building a Vacation Planer that takes user requests and suggests the best vacation plans, here are some recommendations for designing a data pipeline strategy:

1. Data Sources:
   - Travel websites (e.g., Expedia, Booking.com) to collect information about available flights, hotels, rental cars, etc.
   - PDF documents from travel guides, blogs, and reviews to gather insights on destinations, activities, accommodations, etc.
   - Audio files of user conversations or voice assistants to understand natural language queries and preferences.

2. Extraction Tools:
   - Web scraping libraries (e.g., BeautifulSoup, Scrapy) for extracting data from websites.
   - PDF parsing tools (e.g., PyPDF2, pdfplottter) for extracting text and relevant information from travel guides and documents.
   - Speech-to-text APIs (e.g., Google Cloud Speech-to-Text, IBM Watson Speech to Text) for converting audio files into transcriptions.

3. Cleaning Steps:
   - Remove stop words and perform stemming/lemmatization on extracted text data to normalize the content.
   - Handle missing or inconsistent data by filling in gaps or removing incomplete entries.
   - Perform deduplication of records to ensure unique vacation plans or destinations are not repeated.
   - Anonymize personally identifiable information (PII) such as names, addresses, etc., before storing or processing the data.

4. Voice Capabilities:
   - Integrate speech recognition APIs to allow users to interact with the Vacation Planer using voice commands.
   - Use natural language understanding techniques to extract relevant entities and preferences from user queries (e.g., destination, dates, budget).
   - Provide voice feedback for suggested vacation plans or recommendations.

5. Data Volume and Processing Time:
   - The data volume will depend on the scale of your project. Start with a smaller dataset and gradually expand as needed.
   - Consider using cloud-based storage solutions like Google Cloud Storage or Amazon S3 to store large amounts of text, PDFs, and audio files.
   - Optimize processing time by parallelizing tasks, using efficient data structures, and leveraging distributed computing frameworks if required.

6. Additional Considerations:
   - Implement a user authentication system to securely access the Vacation Planer's features.
   - Use version control (e.g., Git) to track changes in your codebase and collaborate with others.
   - Set up monitoring and logging mechanisms to capture errors, exceptions, and important events during runtime.

Remember to prioritize data privacy and security throughout the pipeline. Ensure that user information is handled securely and comply with relevant regulations such as GDPR or CCPA.

As you progress through the project, continuously evaluate and iterate on your data pipeline based on feedback from users and changing requirements. Regularly monitor performance metrics like processing time, error rates, and data quality to ensure a smooth user experience.

## Mini Pipeline Results

- Documents collected: 5
- Documents after cleaning: 5

## Reflections

### Data Strategy
[YOUR REFLECTION HERE]
Web sites like TripAdvisor, Lonely Planet, and some travel agency's brouchures in PDF format would be great data sources for travel recommendations. For web scraping, I would use Trafilatura for its robustness in extracting content from complex web pages, and for PDFs
I might use docling for docuements collect, and trafilatura for web crawling. 
I will also use data cleaning pipelines to pre access  data.
OCR quality might be an issue for scanned brochures, so I will need to experiment with Tesseract and Marker to see which gives better results.
- Which data sources are most relevant for your project?
- Which tools from this week will you actually use in your capstone?
- What's the most challenging data quality issue you expect to face?

### Pipeline Execution
[YOUR REFLECTION HERE]
I  cloolect data for Prgramming language in AI era.
No documents were removed by the pipeline. I guess the data is clean enough for my use case.
Scaling to a full dataset would involve automating the scraping process to run on a schedule, and using cloud storage and processing (e.g., AWS S3 + Lambda) to handle larger volumes of data. I would also implement monitoring to track data quality and pipeline performance.    

- What data did you collect and how did you clean it?
- Were any documents removed by the pipeline? Why?
- How would you scale this to a full dataset for your project?

## Tools I Plan to Use

[STUDENT: List the specific tools from Week 3 you'll use in your capstone]

## Next Steps

[STUDENT: What will you build next week with RAG and vector databases?]
