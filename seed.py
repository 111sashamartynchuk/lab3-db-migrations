import pandas as pd
from datetime import datetime
from database import SessionLocal
from models import Weather, WindDirectionEnum

def parse_time(time_str):
    if pd.isna(time_str) or not time_str:
        return None
    try:
        return datetime.strptime(str(time_str).strip(), "%I:%M %p").time()
    except ValueError:
        return None

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
        print(f"Зчитано {len(df)} рядків з CSV. Починаємо імпорт...")

        records = []
        for _, row in df.iterrows():
            wind_dir_raw = str(row.get('wind_direction', '')).strip()
            try:
                wind_dir_enum = WindDirectionEnum[wind_dir_raw] if wind_dir_raw in WindDirectionEnum.__members__ else None
            except KeyError:
                wind_dir_enum = None

            weather_record = Weather(
                country=row.get('country'),
                wind_degree=int(row['wind_degree']) if pd.notna(row.get('wind_degree')) else None,
                wind_kph=float(row['wind_kph']) if pd.notna(row.get('wind_kph')) else None,
                wind_direction=wind_dir_enum,
                last_updated=parse_date(row.get('last_updated')),
                sunrise=parse_time(row.get('sunrise')),
                sunset=parse_time(row.get('sunset')),
                moonrise=parse_time(row.get('moonrise')),
                moonset=parse_time(row.get('moonset')),
                moon_phase=row.get('moon_phase'),
                moon_illumination=int(row['moon_illumination']) if pd.notna(row.get('moon_illumination')) else None
            )
            records.append(weather_record)

        db.bulk_save_objects(records)
        db.commit()
        print("Дані успішно імпортовано в базу даних!")

    except Exception as e:
        db.rollback()
        print(f"Помилка при імпорті даних: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()