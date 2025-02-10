import google.generativeai as genai  
from dotenv import load_dotenv  
import os  
from langchain_community.document_loaders import TextLoader  

# Load environment variables  
load_dotenv(".env")  

# Retrieve API key from .env file  
api_key = os.getenv("GEMINI_API_KEY")  

# Configure Gemini API  
genai.configure(api_key=api_key)  

# Define the prompt for topic sequencing  
prompt_for_sequencing_topics_and_concepts = "Organize the following text into sequenced topics and key concepts:"  

# Define generation config  
get_topics_and_concepts_config = {
    "temperature": 0.7,
    "max_output_tokens": 512,
}

class AIProcessor:
    @staticmethod  
    async def sequencing_topics_and_concepts(data: str) -> str:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash", generation_config=get_topics_and_concepts_config)
            inputs = f"{prompt_for_sequencing_topics_and_concepts}\n{data}"
            sequenced_topics_and_concepts = await model.generate_content_async(inputs)
            return sequenced_topics_and_concepts.text
        except Exception as e:
            raise ValueError(f"Error sequencing topics and concepts: {str(e)}")

async def main():
    # Load text from file  
    loader = TextLoader(r"C:\Users\dP-PL\Desktop\prompt\docs-pdf\sample.txt")  
    data = loader.load()
    text_content = data[0].page_content  # Extract text  

    # Print extracted text  
    print("Extracted Text:\n", text_content)  

    # Process with Gemini AI  
    sequenced_topics = await AIProcessor.sequencing_topics_and_concepts(text_content)  

    # Print the sequenced topics  
    print("\nSequenced Topics and Concepts:\n", sequenced_topics)

# Run the async function  
import asyncio  
asyncio.run(main())  
