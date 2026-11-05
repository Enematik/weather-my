# Wetter & Regenradar (PWA)

Leichte Wetter-App für das iPhone (und jeden Browser) als Progressive Web App:

- **Ortssuche** mit Autovervollständigung (Open-Meteo Geocoding)
- **Regenradar** der letzten 2 Stunden als Animation mit Zeit-Slider und Zoom
  (RainViewer-API, kostenlos, Key-frei)
- **Aktuelles Wetter**, 24-h-Regen-/Temperatur-Chart und 7-Tage-Vorhersage (Open-Meteo, Key-frei)
- **Favoriten**: gefundene Orte werden lokal gespeichert (localStorage) und bleiben
  auch nach dem Schließen erhalten; „Mein Standort“ per GPS-Button
- **PWA**: Startbildschirm-Icon, Vollbildmodus, Offline-Abruf der App-Seite

## Icons erzeugen (einmalig, vor dem Push)

Die App-Icons (`icon-512.png`, `icon-192.png`, `apple-touch-icon.png`) sind nicht im
Ordner enthalten. Sie werden mit dem mitgelieferten Skript erzeugt (nur Standard-Python,
keine Zusatzpakete):

```
cd wetterapp
python make_icons.py
```

Vor dem Push die Testdatei `_test_icons.py` löschen (nicht für die App nötig).

## Auf dem iPhone installieren

1. Die Seite in **Safari** öffnen
2. Teilen-Button → „Zum Home-Bildschirm“
3. App startet fullscreen mit eigenem Icon

## GitHub Pages bereitstellen

1. GitHub-Repository anlegen (z. B. `wetter-app`), alle Dateien dieses Ordners in den Repo-Root pushen
   ```
   git init
   git add .
   git commit -m "Wetter-PWA"
   git remote add origin https://github.com/<dein-user>/wetter-app.git
   git push -u origin main
   ```
2. Im Repo: **Settings → Pages** → „Source“ auf `main` / Root-Ordner stellen → Save
3. Nach dem Deploy ist die App erreichbar unter
   `https://<dein-user>.github.io/wetter-app/`
4. Auf dem iPhone diese URL in Safari öffnen und „Zum Home-Bildschirm“ wählen
   (GPS benötigt HTTPS – GitHub Pages liefert HTTPS)

Hinweis: `.nojekyll` verhindert das Jekyll-Build; die App läuft dadurch ohne Build-Schritt.
Bei einem **Projekt-Page** im Unterordner `/docs` einfach alle Dateien dorthin legen.

## Datenquellen & Credits

- Wetterdaten: [Open-Meteo](https://open-meteo.com/) – frei für nicht-kommerzielle Nutzung
- Radarbilder: [RainViewer API](https://www.rainviewer.com/api.html) – Attribution erforderlich
  (Credit ist in der App sichtbar verlinkt)

Beide APIs laufen ohne API-Key, nur via HTTPS.

## Radar-Abdeckung

RainViewer deckt USA, Westeuropa (FR, IT, CH …) ab – **in Deutschland und Österreich
liefert es oft keine Radardaten** (die DWD-Radarbilder sind kein frei zugängliches
Tile-API). Die App zeigt dann einen Hinweis und einen Link zum offiziellen
[DWD-Radarfilm](https://www.wettergefahren.de/wetter/deutschland/aktuell/radarfilm.html).
Der Regen-Chart und die Vorhersagen (Open-Meteo) funktionieren überall, auch in Deutschland.
