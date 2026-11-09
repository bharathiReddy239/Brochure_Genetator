import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import gradio as gr  # noqa: I001
import importlib  # noqa: I001, RUF100

# from gradio.monitoring_dashboard import demo  # noqa: E402, F401, I001, RUF100
from src.ai_brochure_generator.scraper import scrape_website
from src.ai_brochure_generator.llm import generate_brochure_content
# pyright: ignore[reportMissingImports]  # noqa: F811, RUF100

generate_brochure_content = importlib.import_module(  # noqa: F811
    "src.ai_brochure_generator.llm"
).generate_brochure_content
from src.ai_brochure_generator.pdf_builder import create_pdf  # pyright: ignore[reportMissingImports]


def generate_brochure(url, max_pages):
    try:
        max_pages = int(max_pages)
        if max_pages < 1:
            return "Error: max_pages must be a positive integer."
    except ValueError:
        return "Error: max_pages must be a positive integer."

    try:
        scraped_content = scrape_website(url, max_page=max_pages)
        print(
            "SCRAPED:",
            type(scraped_content),
            list(scraped_content)[:3] if scraped_content else None,
        )  # noqa: T201")
        brochure_content = generate_brochure_content(scraped_content)
        create_pdf(brochure_content, "brochure.pdf")
        return "Brochure generated successfully! Check the output directory for 'brochure.pdf'."
    except Exception as e:  # noqa: BLE001
        import traceback

        traceback.print_exc()  # noqa: BLE001, RUF100
        return f"Error:{e}"  # noqa: RUF010, RUF100


demo = gr.Interface(
    fn=generate_brochure,
    inputs=[
        gr.Textbox(label="Website URL", placeholder="Enter the website URL"),
        gr.Number(label="Max Pages", value=5, precision=0),
    ],
    outputs=gr.Textbox(label="Output"),
    title="AI Brochure Generator",
    description="Enter a website URL and the maximum number of pages to scrape. The tool will generate a brochure in PDF format.",
)


if __name__ == "__main__":
    demo.launch()


# http://127.0.0.1:7860
