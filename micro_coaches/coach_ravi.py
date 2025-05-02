from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Define the prompt template for Ravi
prompt_template = """
You are Coach Ravi Riser 📚, a {role} for high school students (Grade 9–12).
You speak in a {tone} tone and respond in {language}.

Student Goal: {goal}

You support students with:
- Exam preparation
- Study strategies
- Stream and course selection
- Career planning

Student Message: "{student_message}"

Always respond with clarity, enthusiasm, and motivation.
"""

# Initialize OpenAI key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI chat model
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=openai_api_key  # Correct key usage
)

# Create a ChatPromptTemplate
prompt = ChatPromptTemplate.from_template(prompt_template)

# Function to generate response
def get_ravi_prompt(tone, language, goal, role, student_message):
    print("Inside ravi coach function")
    print(f"OpenAI API Key: {openai_api_key}")
    print(tone, language, goal, role, student_message)

    try:
        formatted_prompt = prompt.format_messages(
            role=role,
            tone=tone,
            language=language,
            goal=goal,
            student_message=student_message
        )

        result = llm.invoke(formatted_prompt)
        print("Model response:", result)
        return result.content
    except Exception as e:
        print(f"Error occurred while invoking the model: {e}")
        return str(e)
