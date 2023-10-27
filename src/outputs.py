import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, RESULTS_DIR, FILE_OUTPUT, PRETTY_OUTPUT

RESULTS_FILE_MESSAGE = 'Файл с результатами был сохранен: {file_path}'

def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(RESULTS_FILE_MESSAGE.format(file_path=file_path))


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)

OUTPUTS = {
    PRETTY_OUTPUT: pretty_output,
    FILE_OUTPUT: file_output,
    None: default_output,
}

def control_output(results, cli_args, outputs = OUTPUTS):
    outputs[cli_args.output](results, cli_args)