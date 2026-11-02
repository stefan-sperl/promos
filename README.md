# promos

Fernsteuerbare Werbung in eigener Sache für den
[Rentencountdown](https://github.com/stefan-sperl/Rentencountdown).

Die App lädt bei jedem Start die Datei `promos.json` aus diesem Repo
(über `raw.githubusercontent.com`) und zeigt daraus einmalig pro Kampagne
ein Fenster „Kennst du unsere anderen Apps?“. Änderungen hier wirken sich
ohne App-Update aus – `raw.githubusercontent.com` cached bis zu fünf Minuten.

```
https://raw.githubusercontent.com/stefan-sperl/promos/main/promos.json
```

## Eine Kampagne anlegen

1. Bilder (optional) nach `images/<app>/` legen, z. B.
   `images/feierabend-countdown/1.png`. Empfohlen: PNG oder JPG im
   Seitenverhältnis **3:2**, etwa **1200 × 800 px**, unter 400 KB pro Bild.
   Die App zeigt mehrere Bilder als Karussell.
2. In `promos.json` einen Eintrag ergänzen (siehe unten). Neue Einträge
   oben einfügen, denn die Reihenfolge ist die Priorität: pro App-Start wird
   höchstens ein noch nicht gesehenes Fenster gezeigt.
3. `enabled` auf `true` setzen, committen, fertig.

Zum Vorabtesten kann die App auf einen anderen Dateipfad zeigen, z. B. auf
einen Branch:

```bash
flutter run --dart-define=PROMO_URL=https://raw.githubusercontent.com/stefan-sperl/promos/entwurf/promos.json
```

## Felder

| Feld          | Pflicht | Bedeutung |
|---------------|---------|-----------|
| `id`          | ja      | Eindeutig; jede `id` wird pro Gerät nur einmal als Fenster gezeigt. Für eine neue Welle derselben App einfach eine neue `id` vergeben (z. B. mit Monat). |
| `app`         | ja      | Name der beworbenen App, erscheint in der Liste „Weitere Apps von uns“ in den Einstellungen. |
| `title`       | ja      | Überschrift des Fensters. |
| `text`        | ja      | Beschreibung, zwei bis drei Zeilen. |
| `emoji`       | nein    | Wird gezeigt, wenn es keine Bilder gibt oder ein Bild nicht lädt. Standard 📱. |
| `images`      | nein    | Liste von HTTPS-Bild-URLs aus diesem Repo (siehe Vorlage). Leer lassen für ein Fenster nur mit Emoji. |
| `ios`         | nein    | App-Store-Link. Fehlt er, erscheint die Kampagne auf iPhones nicht. |
| `android`     | nein    | Play-Store-Link. Fehlt er, erscheint die Kampagne auf Android nicht. Mit `referrer=utm_…` sind Installationen in der Play Console der Kampagne zuordenbar. |
| `from`        | nein    | Erster Anzeigetag `JJJJ-MM-TT` (einschließlich). |
| `until`       | nein    | Letzter Anzeigetag `JJJJ-MM-TT` (einschließlich). Danach verschwindet die Kampagne auch aus der Liste in den Einstellungen. |
| `minLaunches` | nein    | Erst ab so vielen App-Starts zeigen. Standard 3. |
| `button`      | nein    | Beschriftung des Buttons. Standard „App ansehen“. |
| `enabled`     | nein    | `false` schaltet die Kampagne komplett ab. Standard `true`. |

Nur `https://`-Links werden akzeptiert. Ein fehlerhafter Eintrag wird
übersprungen, die anderen funktionieren weiter. Ist die ganze Datei kaputt,
nutzt die App die zuletzt geladene Version.

## Bild-URLs

Ein Bild unter `images/feierabend-countdown/1.png` ist erreichbar als

```
https://raw.githubusercontent.com/stefan-sperl/promos/main/images/feierabend-countdown/1.png
```

Beim Austauschen eines Bildes am besten einen neuen Dateinamen verwenden
(`3.png` statt `1.png` überschreiben), damit kein alter Zwischenspeicher
greift.

## Wie die App Kampagnen zeigt

- Beim Start wartet die App drei Sekunden und zeigt höchstens ein Fenster:
  Meilenstein-Feier vor Bewertungs-Dialog vor App-Werbung vor der nativen
  Bewertungsabfrage. Eine Kampagne, die nicht drankommt, erscheint beim
  nächsten Start.
- „Nein danke“ und „App ansehen“ markieren die Kampagne als gesehen.
- Alle laufenden Kampagnen stehen zusätzlich in den Einstellungen unter
  „Weitersagen → Weitere Apps von uns“.
- Ohne Netz oder bei einem Fehler passiert nichts; es werden keine
  Nutzerdaten übertragen, nur die Datei abgerufen.

## Prüfung

`promos.schema.json` beschreibt das Format. Der Workflow in
`.github/workflows/validate.yml` prüft bei jedem Push, dass die Datei gültig
ist und alle Bild-URLs auf vorhandene Dateien in diesem Repo zeigen.
