import typer
from database import SessionLocal
from models import Weather

app = typer.Typer(help="CLI інструмент для роботи з погодними даними")


@app.command()
def stats():
    """Показати загальну статистику погодних даних"""
    db = SessionLocal()
    total = db.query(Weather).count()
    good = db.query(Weather).filter(Weather.go_outside == True).count()
    bad = db.query(Weather).filter(Weather.go_outside == False).count()

    typer.echo(f"Загальна кількість записів: {total}")
    typer.echo(f"☀Теплі дні (>=15°C): {good}")
    typer.echo(f"Прохолодні/холодні дні (<15°C): {bad}")
    db.close()


@app.command()
def country(name: str):
    db = SessionLocal()
    records = db.query(Weather).filter(Weather.country.ilike(f"%{name}%")).limit(5).all()

    if not records:
        typer.echo(f"Країну '{name}' не знайдено.")
        db.close()
        return

    typer.echo(f"\nЗнайдено записи для '{name}':")
    for r in records:
        status = "Варто виходити " if r.go_outside else "Краще одягнутися тепліше "
        tz = f" | Часовий пояс: {r.celestial_info.timezone}" if r.celestial_info else ""
        typer.echo(
            f" - Дата: {r.last_updated} | Температура: {r.temperature_celsius}°C ({r.condition_text}) | {status}{tz}")

    db.close()


if __name__ == "__main__":
    app()