from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

class ChatBot:
    def __init__(self):
     

        self.client = Groq(api_key=api_key)
        self.system_prompt = """You are a helpful assistant that answers questions based on website content. 
        Always respond truthfully based on the provided context. If unsure, say you don't know."""

    def generate_response(self, query, context, source_url):
        """Generate response using RAG"""
        context_text = "\n\n".join([doc.page_content for doc in context])
        
        prompt = f"""Context: {context_text}
        
        Question: {query}
        
        Answer:"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model="mixtral-8x7b-32768",
                temperature=0.5
            )
            return f"{response.choices[0].message.content}\nSource: {source_url}"
        except Exception as e:
            return f"Error generating response: {str(e)}"