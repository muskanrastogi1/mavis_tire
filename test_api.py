import os
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_connection():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        return False
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Make a simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API connection successful!'"}
            ],
            max_tokens=10
        )
        
        # Print the response
        print("API Response:", response.choices[0].message.content)
        print("API call successful!")
        return True
        
    except Exception as e:
        print(f"Error making API call: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_connection() 