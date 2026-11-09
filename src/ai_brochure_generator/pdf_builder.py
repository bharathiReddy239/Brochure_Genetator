from reportlab.lib.pagesizes import A4  # noqa: I001
from reportlab.lib import colors  # noqa: F401, I001, RUF100
import reportlab.pdfgen  # noqa: F401, RUF100
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # noqa: F401
from reportlab.lib.enums import TA_CENTER  # noqa: F401
from reportlab.lib.units import inch  # noqa: F401
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable  # noqa: F401
from xml.sax.saxutils import escape
from pathlib import Path
import re
import tempfile  # noqa: F401

OUTPUT_DIR = Path(__file__).parent.parent / "output_brouchures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_pdf(brochure_content, output_filename):
    output_path = OUTPUT_DIR / output_filename
    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    if isinstance(brochure_content, dict):
        text = "\n\n".join(str(v) for v in brochure_content.values() if v)
    else:
        text = str(brochure_content or "")
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue

        if line.startswith("#"):
            title = escape(line.lstrip("#").strip().replace("**", ""))
            story.append(Spacer(1, 10))
            story.append(Paragraph(title, styles["Heading2"]))
            continue

        safe = escape(line)
        safe = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", safe)
        if line.startswith(("-", "*")):
            story.append(
                Paragraph(safe[1:].lstrip(), styles["BodyText"], bulletText="•")
            )
        else:
            story.append(Paragraph(safe, styles["BodyText"]))

        doc.build(story)
    return str(output_path)
    # If the content is a string, wrap it in a dictionary with a default key
    # brochure_content = {"content": brochure_content}


#     # Add company name and logo
#     company_name = brochure_content.get("company_name", "Company Name")
#     logo_path = brochure_content.get("logo_path", None)
#     if logo_path:
#         story.append(Image(logo_path, width=2 * inch, height=2 * inch))
#     story.append(Paragraph(company_name, styles["Title"]))
#     story.append(Spacer(1, 12))

#     # Add other sections
#     for section in [
#         "introduction",
#         "about",
#         "products_services",
#         "mission_vision",
#         "key_strengths",
#         "contact_info",
#     ]:
#         content = brochure_content.get(section, "")
#         if content:
#             story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
#             story.append(Spacer(1, 12))
#             story.append(
#                 Paragraph(section.replace("_", " ").title(), styles["Heading2"])
#             )
#             story.append(Spacer(1, 6))
#             story.append(Paragraph(content, styles["BodyText"]))
#             story.append(Spacer(1, 12))

#     doc.build(story)

#     def add_page_numbers(canvas, doc):  # noqa: F811, RUF100
#         page_num = canvas.getPageNumber()
#         text = f"Page {page_num}"
#         canvas.setFont("Helvetica", 10)
#         canvas.drawRightString(
#             A4[0] - inch, 0.75 * inch, text
#         )  # Adjust position as needed


# if __name__ == "__main__":
#     test_content = {
#         "company_name": "Test Company",
#         "logo_path": None,
#         "introduction": "This is a test introduction.",
#         "about": "This is a test about section.",
#         "products_services": "These are test products and services.",
#         "mission_vision": "This is a test mission and vision statement.",
#         "key_strengths": "These are test key strengths.",
#         "contact_info": "This is test contact information.",
#     }
#     create_pdf(test_content, "my_brochure.pdf")
#     print("PDF created successfully inside the output_brochure folder.")
