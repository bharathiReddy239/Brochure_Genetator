<!-- AI Brochure Generator -->
Turns company website into PDF Brochure
<!-- How it is works -->
1.Scraper.py reads the homepage and find useful links
2.llm.py sends the page text to local model through ollama
3.Pdf builder.py turns the answer into PDF
<!-- REquirement -->
Python 3.11
uv
Ollama
<!-- setup -->
bash 
git clone
cd Brochure_Generator
