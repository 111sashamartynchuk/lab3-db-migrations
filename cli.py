import sys
import typer
from datetime import datetime
from sqlalchemy import func
from database import SessionLocal
from models import Weather, CelestialBody

app = typer.Typer(help="CLI інструмент для роботи з погодними даними")


@app.command()
def stats():
    """Показати загальну статистику погодних даних"""
    db = SessionLocal()
    total = db.query(Weather).count()
    good = db.query(CelestialBody).filter(CelestialBody.go_outside == True).count()
    bad = db.query(CelestialBody).filter(CelestialBody.go_outside == False).count()

    typer.echo(f"📊 Загальна кількість записів: {total}")
    typer.echo(f"☀️ Сприятливі дні (>=15°C): {good}")
    typer.echo(f"❄️ Несприятливі дні (<15°C): {bad}")
    db.close()


@app.command()
def search(
        country: str = typer.Option(None, help="Назва країни"),
        date: str = typer.Option(None, help="Дата у форматі YYYY-MM-DD")
):
    """Інтерактивний пошук погоди з підказками про доступні дати та повторним введенням"""
    if not isinstance(country, str):
        country = None
    if not isinstance(date, str):
        date = None

    db = SessionLocal()

    try:
        while True:
            # За запитом користувача отримуємо назву країни
            if not country:
                country_input = typer.prompt("\n🌍 Введіть назву країни (або 'q' для виходу)")
                if country_input.strip().lower() in ['q', 'exit', 'вихід']:
                    typer.echo("Завершення роботи CLI.")
                    break
                country_val = country_input.strip()
            else:
                country_val = country

            # Двзнаємося мінімальну та максимальну дату в БД для цієї країни
            date_range = db.query(
                func.min(Weather.last_updated),
                func.max(Weather.last_updated)
            ).filter(Weather.country.ilike(f"%{country_val}%")).first()

            if not date_range or not date_range[0]:
                typer.echo(f"❌ Країну '{country_val}' не знайдено в базі даних. Спробуйте ще раз.")
                country = None
                continue

            min_d, max_d = date_range
            typer.echo(f"📅 Для території '{country_val}' доступні дати з {min_d} по {max_d}")

            # Запитуємо дату
            if date is None:
                date_input = typer.prompt(
                    "Введіть дату у форматі YYYY-MM-DD (або натисніть Enter для всіх доступних)",
                    default=""
                )
                date_val = date_input.strip()
            else:
                date_val = date.strip()

            # Формуємо запит до БД
            query = db.query(Weather).filter(Weather.country.ilike(f"%{country_val}%"))

            if date_val:
                try:
                    target_date = datetime.strptime(date_val, "%Y-%m-%d").date()
                    query = query.filter(Weather.last_updated == target_date)
                except ValueError:
                    typer.echo("❌ Помилка: некоректний формат дати! Використовуйте YYYY-MM-DD (наприклад, 2024-05-16).")
                    date = None
                    continue

            records = query.limit(5).all()

            if not records:
                typer.echo(
                    f"⚠️ На дату '{date_val}' записів не знайдено. Спробуйте іншу дату з діапазону {min_d} .. {max_d}.")
                date = None
                continue

            # Виведення результатів
            typer.echo(f"\n🔍 Знайдено записи для '{country_val}':")
            for r in records:
                c_info = r.celestial_info
                status = "Варто виходити 🟢" if (c_info and c_info.go_outside) else "Краще одягнутися тепліше 🔴"
                tz = f" | Часовий пояс: {c_info.timezone}" if c_info else ""
                typer.echo(
                    f" - Дата: {r.last_updated} | Температура: {r.temperature_celsius}°C ({r.condition_text}) | {status}{tz}")

            again = typer.prompt("\nБажаєте зробити ще один пошук? (y/n)", default="y")
            if again.strip().lower() not in ['y', 'yes', 'так', 'т']:
                typer.echo("Роботу завершено.")
                break

            country = None
            date = None

    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        search()
    else:
        app()