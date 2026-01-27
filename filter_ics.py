import requests
from icalendar import Calendar

ICS_URL = "https://sked.lin.hs-osnabrueck.de/sked/jg/23SPS.ics"

KEYWORDS = [
    "Datenbanken", "IT-Sicherheit", "Big Data",
    "Integrierte Managementsysteme A",
    "Internationales Marketing",
    "Marketing: Planung von Marketingstrategien B",
    "Projektorientierte Unternehmens",
    "Cross Cultural",
]

def norm(s: str) -> str:
    return (s or "").casefold()

kw_norm = [k.casefold() for k in KEYWORDS]

r = requests.get(ICS_URL)
r.raise_for_status()

# wichtig: bytes nehmen und selbst als utf-8 dekodieren (statt requests raten lassen)
text = r.content.decode("utf-8", errors="replace")

cal = Calendar.from_ical(text)
out = Calendar()
out.add("PRODID", "-//filtered//EN")
out.add("VERSION", "2.0")

kept = 0
total = 0

for comp in cal.walk("VEVENT"):
    total += 1
    summary = str(comp.get("SUMMARY", ""))
    desc = str(comp.get("DESCRIPTION", ""))
    loc = str(comp.get("LOCATION", ""))

    hay = norm(summary) + "\n" + norm(desc) + "\n" + norm(loc)

    if any(k in hay for k in kw_norm):
        out.add_component(comp)
        kept += 1

with open("filtered.ics", "wb") as f:
    f.write(out.to_ical())

print(f"✅ Fertig! {kept}/{total} Events übernommen.")
