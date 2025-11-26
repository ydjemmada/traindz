# 📋 Manual Data Entry Guide for SNTF Train Schedules

## Quick Start

1. **Edit the data file**: Open `train_data.json` in your text editor
2. **Add your trains**: Follow the examples in the file
3. **Run the import**: `python3 backend/scripts/import_from_json.py`

## File Location

Main data file: `/home/mathxro/AntiGrav/train_data.json`

## How to Add a New Train

### Step 1: Copy this template

```json
{
  "number": "YOUR_TRAIN_NUMBER",
  "line": "Alger-Thenia",
  "route": "Alger - Thenia",
  "days_operational": "[*]",
  "stops": [
    {
      "station_name": "Alger",
      "time": "HH:MM"
    },
    {
      "station_name": "Next Station",
      "time": "HH:MM"
    }
  ]
}
```

### Step 2: Fill in the details

- **number**: Train number (e.g., "27", "B609", "1025")
- **line**: Line name for reference (not used in database)
- **route**: Must match EXACTLY one of these:
  - `"Alger - Thenia"`
  - `"Thenia - Alger"`
  - `"Alger - El Affroun"`
  - `"El Affroun - Alger"`
  - `"Alger - Zéralda"`
  - `"Zéralda - Alger"`
  - `"Agha - Aeroport"`
- **days_operational**: 
  - `"[*]"` = Runs every day
  - `"[1]"` = Does not run on Fridays
  - `"[2]"` = Runs only on Fridays
- **stops**: Array of stations in order with times (HH:MM format)

### Step 3: Station Names

**⚠️ IMPORTANT**: Station names must match EXACTLY (case-sensitive)

**Alger-Thenia Line:**
- Alger, Agha, Ateliers, Hussein Dey, Caroubier, El Harrach
- Oued Smar, Bab Ezzouar, Dar El Beida, Rouiba, Rouiba Ind
- Rouiba SNVI, Reghaia, Reghaia Ind, Boudouaou, Corso
- Boumerdes, Tidjelabine, Thenia

**Alger-El Affroun Line:**
- Alger, Agha, Ateliers, Hussein Dey, Caroubier, El Harrach
- Gué de Constantine, Ain Naadja, Baba Ali, Birtouta, Boufarik
- Beni Mered, Blida, Chiffa, Mouzaia, El Affroun

**Alger-Zéralda Line:**
- Alger, Agha, Ateliers, Hussein Dey, Caroubier, El Harrach
- Gué de Constantine, Ain Naadja, Baba Ali, Birtouta
- Tessala El Merdja, Sidi Abdelah, Zéralda

**Airport Line:**
- Agha, El Harrach, Bab Ezzouar, Aeroport Houari Boumediene

## Example: Adding Train 47

```json
{
  "number": "47",
  "line": "Alger-Thenia",
  "route": "Alger - Thenia",
  "days_operational": "[*]",
  "stops": [
    {
      "station_name": "Alger",
      "time": "12:35"
    },
    {
      "station_name": "Agha",
      "time": "12:38"
    },
    {
      "station_name": "El Harrach",
      "time": "12:52"
    },
    {
      "station_name": "Boumerdes",
      "time": "13:28"
    },
    {
      "station_name": "Thenia",
      "time": "13:37"
    }
  ]
}
```

## Running the Import

After editing `train_data.json`:

```bash
cd /home/mathxro/AntiGrav
python3 backend/scripts/import_from_json.py
```

The script will:
- ✅ Validate your data
- ✅ Skip example trains
- ✅ Update existing trains if they already exist
- ✅ Show you what was imported
- ⚠️  Warn you about any errors (wrong station names, etc.)

## Tips

1. **Remove the EXAMPLE trains** before importing
2. **Check station names carefully** - they must match exactly
3. **Times must be in 24-hour format** (HH:MM): "06:30", "14:45"
4. **Route names are case-sensitive**
5. The script is safe to run multiple times - it will update existing trains

## Need Help?

Check the `available_stations` and `available_routes` sections in `train_data.json` for valid values.
