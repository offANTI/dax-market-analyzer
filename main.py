import argparse
import sys
from src.extractor import fetch_data
from src.transformer import process_data
from src.database import save_to_db
from src.visualizer import create_visuals


def run_pipeline(full_update=True):
    print("\n" + "=" * 40)
    print("DAX-MARKET-ANALYZER START")
    print("=" * 40)

    dax_tickers = ['SAP.DE', 'SIE.DE', 'ALV.DE', 'BMW.DE', 'DTE.DE', 'AIR.DE']

    if full_update:
        # ШАГ 1: Экстракция
        rohdaten = fetch_data(dax_tickers)
        save_to_db(rohdaten, 'rohdaten_preise')

        # ШАГ 2: Трансформация
        analyse_ergebnisse = process_data(rohdaten)

        # ШАГ 3: Загрузка результатов
        save_to_db(analyse_ergebnisse, 'processed_analytics')

    # ШАГ 4: Визуализация (всегда выполняется или по флагу)
    create_visuals()

    print("=" * 40)
    print("✅ PIPELINE ERFOLGREICH BEENDET")
    print("=" * 40 + "\n")


def main():
    # Настройка парсера на немецком
    parser = argparse.ArgumentParser(
        description='DAX Market Analyzer CLI - Ein Tool zur Analyse von Aktiendaten.'
    )

    # Добавляем аргументы
    parser.add_argument(
        '--update',
        action='store_true',
        help='Führt den vollständigen ETL-Prozess aus (Daten laden, transformieren, speichern).'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Erstellt nur den visuellen Bericht basierend auf vorhandenen Daten.'
    )

    # Если запуск без аргументов, выводим помощь
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.update:
        run_pipeline(full_update=True)
    elif args.report:
        run_pipeline(full_update=False)


if __name__ == "__main__":
    main()
