"""CLI-демонстрація лабораторної роботи №2, варіант 8."""
import argparse
import json
from pathlib import Path

from lab2 import process_accounts, reduce_stats


def main():
    parser = argparse.ArgumentParser(description="Аналіз банківських рахунків")
    parser.add_argument("--data", default="sample_data.json", help="Шлях до JSON-файлу")
    parser.add_argument("--top", type=int, default=3, help="Кількість записів у рейтингу")
    parser.add_argument("--boost-city", default="Kyiv", help="Місто для застосування коефіцієнта")
    parser.add_argument("--factor", type=float, default=1.1, help="Коефіцієнт для міста")
    parser.add_argument("--min-turnover", type=float, default=0.0, help="Мінімальний оборот")
    args = parser.parse_args()

    with Path(args.data).open("r", encoding="utf-8") as file:
        accounts = json.load(file)

    results = process_accounts(
        accounts,
        top_n=args.top,
        city=args.boost_city,
        factor=args.factor,
        min_turnover=args.min_turnover,
    )

    print("\nТОП рахунків:")
    if not results:
        print("Немає рахунків, які відповідають умовам.")
    for account in results:
        print(
            f"ID: {account.get('id')} | "
            f"Ім'я: {account.get('name')} | "
            f"Місто: {account.get('city')} | "
            f"Оборот: {account.get('turnover', 0):.2f}"
        )

    print("\nСтатистика для показаного рейтингу:")
    stats = reduce_stats(results)
    print(f"Кількість рахунків: {int(stats['count'])}")
    print(f"Загальний оборот: {stats['turnover']:.2f}")
    print(f"Середній оборот: {stats['avg_turnover']:.2f}")


if __name__ == "__main__":
    main()
