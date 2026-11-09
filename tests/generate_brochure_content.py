import importlib


generate_brochure_content = importlib.import_module(
    "src.ai_brochure_generator.llm"
).generate_brochure_content
