import os
from openai import OpenAI
from django.conf import settings

class LLMService:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        print(f"API Key found: {'Yes' if api_key else 'No'}")  # Debug line
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        
    def filter_response(self, user_query, potential_responses):
        """
        Use LLM to filter and select the most appropriate response from potential responses
        """
        if not potential_responses:
            return "I'm sorry, I don't have any responses to choose from."

        # Limit the number of responses to prevent token limit issues
        max_responses = 10
        if len(potential_responses) > max_responses:
            # Take a sample of responses
            potential_responses = potential_responses[:max_responses]

        # Create a prompt for the LLM
        prompt = f"""Given the user query: "{user_query}"
        Select the most appropriate response from these options:
        {potential_responses}
        
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
            
            selected_response = response.choices[0].message.content.strip()
            
            # If the selected response isn't in our list, return the first response
            if selected_response not in potential_responses:
                return potential_responses[0]
                
            return selected_response
            
        except Exception as e:
            print(f"Error in LLM filtering: {str(e)}")
            return potential_responses[0] if potential_responses else "I'm sorry, I couldn't process that request." 