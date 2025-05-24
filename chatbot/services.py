import os
from openai import OpenAI
from django.conf import settings

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def filter_response(self, user_query, potential_responses):
        """
        Use LLM to filter and select the most appropriate response from potential responses
        """
        # Create a prompt for the LLM
        prompt = f"""Given the user query: "{user_query}"
        And these potential responses:
        {potential_responses}
        
        Select the most appropriate response that best matches the user's intent.
        Return only the selected response text, nothing else."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change this to other models
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that selects the most appropriate response."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent responses
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in LLM filtering: {str(e)}")
            return potential_responses[0] if potential_responses else "I'm sorry, I couldn't process that request." 