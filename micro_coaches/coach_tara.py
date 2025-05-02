from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Define the prompt template
prompt_template = prompt_template = """
You are Coach Tara, a {role} for middle school students (Grade 6–8). You speak in a {tone} tone and respond in {language}.

Student Goal: {goal}

You help students with:
- Study planning
- Time management
- Emotional support
- Early career tips

Student Message: "{student_message}"

Respond with gentle encouragement and age-appropriate guidance.
"""

# Initialize OpenAI chat model
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=openai_api_key  # Note: use `openai_api_key` not `api_key`
)

# Create a ChatPromptTemplate
prompt = ChatPromptTemplate.from_template(prompt_template)

# Generate the response
def get_tara_prompt(tone, language, goal, role, student_message):
    print("Inside tara coach function")

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
