import os  # noqa: I001
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
if LLM_PROVIDER == "openai":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    client = OpenAI(api_key=api_key)
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
else:
    client = OpenAI(
        base_url=f"{OLLAMA_HOST}/v1",
        api_key="ollama",
    )
    model_name = OLLAMA_MODEL  # No API key needed for local Ollama server


def generate_brochure_content(prompt):
    website_information = ""
    for url, content in prompt.items():
        website_information += f"\n\nSOURCE URL: {url}\nContent: {content[:1000]}"

    brochure_prompt = f"""You are a professional corporate brochure writer.
        create a professional company brochure usin only the supplied company website informtion.
        Rules:
        1. Use only the information provided from the company website.
        2. Do not make up any information.
        3. Do not include any information that is not present in the provided content.
        4. Ensure the brochure is well-structured, engaging, and professional.
        5. The brochure should be suitable for potential clients, investors, and partners.
        6.Avoid repeating information.

        Create these sections in the brochure:
        1. Campany Name and Logo
        2. Introduction
        3.About the company
        4. Products and Services
        5. Mission and Vision
        6. Key strengths and Why choose us
        7. Contact Information
        Company website information:
        {website_information}
        """
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You generate accurate, evidence-based content.",
            },
            {"role": "user", "content": brochure_prompt},
        ],
    )
    return response.choices[0].message.content
