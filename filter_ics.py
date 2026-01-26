import requests
from ics import Calendar


# URL deiner Hochschul-ICS-Datei
ICS_URL = "https://sked.lin.hs-osnabrueck.de/sked/jg/23SPS.ics"

# Schlüsselwörter, nach denen gefiltert wird                                                                                           
KEYWORDS = ["Datenbank-Engineering", "IT-Sicherheit","Big Data", "Integrierte Managementsysteme A","Marketing: Internationales", "Marketing: Planung von Marketingstrategien B",  "Projektorientierte Unternehmens" ]
# IT-Sicherheit A oder B(was passt besser, B= EBU); Integrierte Managementsysteme A (gibt auch B); Projekt UNFührung testen weil kein Projektmang-> vllt eher noch ein marketing

def force_utf8(text):
    """Wandelt falsch decodierte Strings (fÃ¼) in echte Umlaute um."""
    if not text:
        return ""
    try:
        # Das fixt den typischen Fehler der ICS-Quelle
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Falls schon korrekt, einfach zurückgeben
        return text
# --- Kalender laden ---
response = requests.get(ICS_URL)
response.raise_for_status()
ics_lines = []
for line in response.text.splitlines():
    # Jede Zeile durch force_utf8 schicken
    ics_lines.append(force_utf8(line))
ics_fixed = "\n".join(ics_lines)

# 3. ICS parsen
calendar = Calendar(ics_fixed)

filtered = Calendar()

for event in calendar.events:
    # ALLES sofort ins richtige Format
    event.name = force_utf8(event.name)
    if event.description:
        event.description = force_utf8(event.description)
    if event.location:
        event.location = force_utf8(event.location)

    # Jetzt ganz normal mit Umlauten filtern (genauso, wie du sie oben in KEYWORDS schreibst)
    if any(kw.lower() in (event.name or "").lower() for kw in KEYWORDS):
        filtered.events.add(event)

with open("filtered.ics", "w", encoding="utf-8") as f:
    f.writelines(filtered.serialize_iter())


print("✅ Fertig! Gefilterte Datei gespeichert.")
