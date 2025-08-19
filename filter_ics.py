import requests
from ics import Calendar

# URL deiner Hochschul-ICS-Datei
ICS_URL = "https://sked.lin.hs-osnabrueck.de/sked/jg/23SPS.ics"

# Schlüsselwörter, nach denen gefiltert wird
KEYWORDS = ["Supply Chain", "Controlling","Informationsmanagement", "Projektierung von ", "Usability", "Produktionsplanung","Projektmanagement", "Businessplanung" ]

response = requests.get(ICS_URL)
response.raise_for_status()
calendar = Calendar(response.text)

filtered = Calendar()
for event in calendar.events:
    if any(k.lower() in event.name.lower() for k in KEYWORDS):
        filtered.events.add(event)

with open("filtered.ics", "w", encoding="utf-8") as f:
    f.writelines(filtered.serialize_iter())

print("✅ Fertig! Gefilterte Datei gespeichert.")
