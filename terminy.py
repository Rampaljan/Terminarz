from datetime import datetime, timedelta
from tabulate import tabulate
import subprocess

vehicles = [
    {"Pojazd": "Mercedes Sprinter    ", "Przegląd": "2025-09-27", "Ubezpieczenie": "2025-03-30"},
    {"Pojazd": "Volvo XC90           ", "Przegląd": "2025-11-05", "Ubezpieczenie": "2025-03-20"},
    {"Pojazd": "Opel Vivaro          ", "Przegląd": "2025-08-07", "Ubezpieczenie": "2025-10-10"},
    {"Pojazd": "Yamaha DragStar      ", "Przegląd": "2025-04-30", "Ubezpieczenie": "2026-01-16"},
    {"Pojazd": "Laweta Rydwan        ", "Przegląd": "2025-08-07", "Ubezpieczenie": "2026-01-24"},
    {"Pojazd": "Jaguar XE            ", "Przegląd": "2025-03-14", "Ubezpieczenie": "2025-09-13"},
    {"Pojazd": "Transporter T4       ", "Przegląd": "2025-03-14", "Ubezpieczenie": "2025-09-06"},
    {"Pojazd": "Przyczepka SAM       ", "Przegląd": None        , "Ubezpieczenie": "2025-05-04"},
    {"Pojazd": "Przyczepa Podłodziowa", "Przegląd": "2025-08-07", "Ubezpieczenie": "2025-08-27"},
    {"Pojazd": "Junak RS125          ", "Przegląd": "2025-07-24", "Ubezpieczenie": "2025-06-04"},
    {"Pojazd": "Peugot Partner       ", "Przegląd": "2025-03-14", "Ubezpieczenie": "2025-07-08"}
]

def get_nearest_dates(vehicles):
    today = datetime.today().date()
    next_month = today + timedelta(days=30)
    
    przeglady = [(v["Pojazd"], "Przegląd", datetime.strptime(v["Przegląd"], "%Y-%m-%d").date()) 
                 for v in vehicles if v["Przegląd"]]
    ubezpieczenia = [(v["Pojazd"], "Ubezpieczenie", datetime.strptime(v["Ubezpieczenie"], "%Y-%m-%d").date()) 
                      for v in vehicles if v["Ubezpieczenie"]]
    
    all_dates = przeglady + ubezpieczenia
    najblizszy_przeglad = min(przeglady, key=lambda x: x[2]) if przeglady else None
    najblizsze_ubezpieczenie = min(ubezpieczenia, key=lambda x: x[2]) if ubezpieczenia else None
    
    upcoming = []
    global days_left_min
    days_left_min = 32
    for pojazd, typ, date in all_dates:
        if today <= date <= next_month:
            days_left = (date - today).days
            upcoming.append(f"UWAGA, w ciągu {days_left} dni masz termin {typ.lower()} pojazdu: {pojazd}")
            if days_left_min > days_left:
                days_left_min = days_left
    
    if not upcoming:
        subprocess.run(["taskkill", "/f", "/im", "cmd.exe"], check=True)
    
    return najblizszy_przeglad, najblizsze_ubezpieczenie, upcoming

najblizszy_przeglad, najblizsze_ubezpieczenie, upcoming_messages = get_nearest_dates(vehicles)


print("""\n\n\nWszystkie Przeglądy i Ubezpieczenia:\n""")
print(tabulate(vehicles, headers="keys", tablefmt="grid"))


# Sprawdzamy, czy są jakiekolwiek terminy na najbliższy miesiąc
if not any("termin" in message for message in upcoming_messages):
    subprocess.run(["taskkill", "/f", "/im", "cmd.exe"], check=True)
else:
    print("""\nWiadomości dotyczące terminów w najbliższym miesiącu:\n""")
    print("\n".join(upcoming_messages))


if days_left_min != 30 and days_left_min > 14:
    subprocess.run(["taskkill", "/f", "/im", "cmd.exe"], check=True)
