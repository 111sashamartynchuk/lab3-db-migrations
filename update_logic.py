from database import SessionLocal
from models import Weather

def update_go_outside_status():
    db = SessionLocal()
    try:
        print("Оновлюємо значення go_outside (температура >= 15°C)...")
        updated_rows = db.query(Weather).filter(Weather.temperature_celsius.isnot(None)).update(
            {Weather.go_outside: Weather.temperature_celsius >= 15.0},
            synchronize_session=False
        )
        db.commit()
        print(f"Успішно оновлено {updated_rows} записів!")
    except Exception as e:
        db.rollback()
        print(f"Помилка при оновленні: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_go_outside_status()