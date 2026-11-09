import pandas as pd
from datetime import datetime
from database import SessionLocal
from models import Weather, CelestialBody


def parse_date(date_str):
    if pd.isna(date_str) or not date_str:
        return None
    try:
        return datetime.strptime(str(date_str).split()[0], "%Y-%m-%d").date()
    except ValueError:
        return None


def seed_data(csv_path="GlobalWeatherRepository.csv"):
    db = SessionLocal()
    try:
        df = pd.read_csv(csv_path)
        print(f"Зчитано {len(df)} рядків з CSV. Заповнюємо нові поля...")

        db.query(CelestialBody).delete()
        db.query(Weather).delete()
        db.commit()

        for _, row in df.iterrows():
            temp_val = pd.to_numeric(row.get('temperature_celsius'), errors='coerce')

            weather_record = Weather(
                country=str(row.get('country', '')).strip(),
                location_name=str(row.get('location_name', '')).strip(),
                temperature_celsius=float(temp_val) if pd.notna(temp_val) else None,
                condition_text=str(row.get('condition_text', '')).strip(),
                last_updated=parse_date(row.get('last_updated'))
            )

            celestial_record = CelestialBody(
                weather=weather_record,
                latitude=float(row['latitude']) if pd.notna(row.get('latitude')) else None,
                longitude=float(row['longitude']) if pd.notna(row.get('longitude')) else None,
                timezone=str(row.get('timezone', '')).strip()
            )

            db.add(weather_record)
            db.add(celestial_record)

        db.commit()
        print("Базу даних успішно заповнено правильними полями!")

    except Exception as e:
        db.rollback()
        print(f"Помилка при імпорті даних: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()