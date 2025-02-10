import google.generativeai as genai  
from dotenv import load_dotenv  
import os  
from langchain_community.document_loaders import TextLoader, PyPDFLoader  

# Load environment variables  
load_dotenv(".env")  
api_key = os.getenv("GEMINI_API_KEY")  

# Configure Gemini API  
genai.configure(api_key=api_key)  

# Define prompts  
prompt_for_topics_and_concepts_extraction = """Extract the main topics and subtopics from this document in a clean, hierarchical format.
Output Format:
- Main Topic 1
  - Subtopic 1
  - Subtopic 2
- Main Topic 2
  - Subtopic 1
  - Subtopic 2
Do not provide any additional text apart from the topics and subtopics.
Document:
"""

prompt_for_combining_topics_and_concepts = """You are an expert in instructional design. Given a list of extracted topics from multiple documents:
- Remove duplicates and merge overlapping concepts.
- Group related topics under broader themes.
- Provide only the final combined list without additional explanations.
Input Data:
"""

prompt_for_sequencing_topics_and_concepts = """You are an expert in curriculum development. Organize the given topics in a logical learning sequence:
- Arrange them in an order that ensures smooth learning from basic to advanced.
- Suggest breaking complex topics into progressive subtopics.
Output Format:
A structured list of topics in optimal learning order.
Input Data:
"""

# New Prompt for Slide Titles
prompt_for_generating_slide_titles = """You are designing a presentation based on structured topics. Your task is to:
- Generate **clear, concise, and engaging slide titles** based on the given topics.
- Keep each title short (max 8 words).
- Ensure the sequence flows naturally for an effective presentation.
Output Format:
1. [Slide Title 1]
2. [Slide Title 2]
3. [Slide Title 3]
...
Do not provide any additional text apart from the slide titles.

Input Data:
"""

# Define generation config  
gen_config = {"temperature": 0.7, "max_output_tokens": 1024}

class AIProcessor:
    @staticmethod  
    async def generate_response(prompt: str, data: str) -> str:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash", generation_config=gen_config)
            inputs = f"{prompt}\n{data}"
            response = await model.generate_content_async(inputs)

            if not response.parts:
                raise ValueError("No valid response returned.")

            return response.text

        except Exception as e:
            raise ValueError(f"Error generating response: {str(e)}")

async def main():
    file_path = r"C:\Users\dP-PL\Desktop\prompt\docs-pdf\dsml.pdf"  

    # Load text from file (PDF or TXT)
    if file_path.endswith(".txt"):
        loader = TextLoader(file_path)
        data = loader.load()
        text_content = data[0].page_content  
    elif file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()
        text_content = "".join(page.page_content for page in pages)  
    else:
        raise ValueError("Unsupported file format. Please use .txt or .pdf")

    # Step 1: Extract Topics and Concepts
    extracted_topics = await AIProcessor.generate_response(prompt_for_topics_and_concepts_extraction, text_content)

    # Step 2: Combine Topics (if multiple documents are used)
    combined_topics = await AIProcessor.generate_response(prompt_for_combining_topics_and_concepts, extracted_topics)

    # Step 3: Sequence Topics
    sequenced_topics = await AIProcessor.generate_response(prompt_for_sequencing_topics_and_concepts, combined_topics)

    # Step 4: Generate Slide Titles (instead of TOC)
    slide_titles = await AIProcessor.generate_response(prompt_for_generating_slide_titles, sequenced_topics)

    # Print Final Slide Titles
    print("\nFinal Slide Titles:\n", slide_titles)

# Run the async function  
import asyncio  
asyncio.run(main())  
