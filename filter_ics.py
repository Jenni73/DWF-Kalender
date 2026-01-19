import requests
from ics import Calendar
import unicodedata

# URL deiner Hochschul-ICS-Datei
ICS_URL = "https://sked.lin.hs-osnabrueck.de/sked/jg/23SPS.ics"

# Schlüsselwörter, nach denen gefiltert wird                                                                                           
KEYWORDS = ["Datenbank-Engineering", "IT-Sicherheit","Big Data", "Integrierte Managementsysteme A", "Marketing: Planung von Marketingstrategien B",  "Projektorientierte Unternehmens" ]
# IT-Sicherheit A oder B(was passt besser, B= EBU); Integrierte Managementsysteme A (gibt auch B); Projekt UNFührung testen weil kein Projektmang

def fix_umlauts(text: str) -> str:
    """Repariert falsch dekodierte UTF-8-Umlaute (fÃ¼ -> ü etc.)"""
    if not text:
        return ""
    try:
        return text.encode("latin1").decode("utf-8")
    except UnicodeError:
        return text

def normalize(text: str) -> str:
    text = fix_umlauts(text)
    text = unicodedata.normalize("NFKC", text)
    return text.strip().lower()

# --- Kalender laden ---
response = requests.get(ICS_URL)
response.raise_for_status()
calendar = Calendar(response.text)

filtered = Calendar()

for event in calendar.events:
    raw_name = event.name or ""
    clean_name = normalize(raw_name)

    if any(kw in clean_name for kw in KEYWORDS):
        # 🔧 Inhalte reparieren, bevor sie exportiert werden
        event.name = fix_umlauts(event.name)
        if event.description:
            event.description = fix_umlauts(event.description)
        if event.location:
            event.location = fix_umlauts(event.location)

        filtered.events.add(event)


with open("filtered.ics", "w", encoding="utf-8") as f:
    f.writelines(filtered.serialize_iter())

print("✅ Fertig! Gefilterte Datei gespeichert.")
