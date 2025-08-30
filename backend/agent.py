import openai
from openai import OpenAI

client = OpenAI(api_key="your API KEY")  # Replace with your actual API key

def create_plan_agent():
    try:
        assistant = client.beta.assistants.create(
            name="Be Healthy Plan Generator",
            instructions="You are a nutritionist specializing in Pakistani diets. Given user details (name, age, height, weight, gender, diseases, allergies), provide a structured plan with three sections: 'Food Plan', 'Foods/Activities to Avoid', and 'Exercise Plan'. Each section must have a 2-3 line description followed by 3-5 bullet points. Use only Pakistani foods (e.g., wheat, rice, lentils, vegetables, chicken, yogurt) in the Food Plan. For diseases/allergies, list specific foods or activities to avoid. Format clearly with markdown headings (###) and bullets (-).",
            model="gpt-4.1-mini"
        )
        return assistant
    except Exception as e:
        print(f"Error creating plan agent: {e}")
        raise

def create_chat_agent():
    try:
        assistant = client.beta.assistants.create(
            name="Be Healthy Chatbot",
            instructions="You are a concise nutritionist chatbot. Answer general queries about nutrition, health, or exercise in 1-2 short sentences. Focus on Pakistani foods or context if relevant. Avoid extra details unless asked.",
            model="gpt-4.1-mini"
        )
        return assistant
    except Exception as e:
        print(f"Error creating chat agent: {e}")
        raise

def get_plan(user_details: dict):
    try:
        assistant = create_plan_agent()
        thread = client.beta.threads.create()
        message_content = f"User details: {user_details}"
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=message_content)
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
    except Exception as e:
        print(f"Error in get_plan: {e}")
        return f"Error generating plan: {str(e)}"

def get_chat_response(query: str):
    try:
        assistant = create_chat_agent()
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=query)
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
    except Exception as e:
        print(f"Error in get_chat_response: {e}")
        return f"Error answering query: {str(e)}"