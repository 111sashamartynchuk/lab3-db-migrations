from sqlalchemy import text
from database import SessionLocal


def update_go_outside_status():
    db = SessionLocal()
    try:
        print("Оновлюємо значення go_outside у таблиці celestial_data...")

        # Миттєве оновлення всіх 170k записів одним запитом у БД
        db.execute(text("""
            UPDATE celestial_data 
            SET go_outside = (weather_data.temperature_celsius >= 15.0)
            FROM weather_data 
            WHERE celestial_data.weather_id = weather_data.id
        """))

        db.commit()
        print("Успішно оновлено логічне поле для всіх записів!")
    except Exception as e:
        db.rollback()
        print(f"Помилка при оновленні: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    update_go_outside_status()