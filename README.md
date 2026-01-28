# Web Scraping & API Integration – Quotes Project

## Përshkrimi i Projektit

Qëllimi i kësaj detyre është përdorimi i **web scraping** dhe **API-ve publike** për të marrë, përpunuar dhe ruajtur të dhëna. Projekti demonstron se si mund të nxirren të dhëna nga një faqe interneti publike dhe si këto të dhëna mund të pasurohen duke përdorur një API të jashtme.

Në këtë projekt:
- Nxirren citate (quotes) nga faqja https://quotes.toscrape.com
- Mblidhen informacione shtesë për autorët duke përdorur Wikipedia REST API
- Të gjitha të dhënat ruhen në një skedar CSV
- Projekti është i përgatitur për t’u ngarkuar në GitHub

## Tutorial: Si ta Ekzekutosh Projektin

1. **Kërkesat Paraprake**
   - Python 3.9 ose më i ri
   - pip
   - Terminal

2. **Klono Projektin nga GitHub**
   ```bash
   git clone https://github.com/USERNAME/quotes-scraper.git
   cd quotes-scraper
   ```

3. **Instalo Libraritë e Nevojshme**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ekzekuto Programin**
   ```bash
   python main.py
   ```

5. **Rezultati**
   - Krijohet dosja `output/`
   - Gjenerohet `quotes_with_wiki.csv`

## Teknologjitë e Përdorura
- Python
- Requests
- BeautifulSoup (bs4)
- Wikipedia REST API
- CSV module
- Git & GitHub
