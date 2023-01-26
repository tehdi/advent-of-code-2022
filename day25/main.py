import logging
import argparse
import math

def configure_logging(verbose, output_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    if output_file is None:
        logging.basicConfig(
            format='%(message)s',
            level=log_level
        )
    else:
        logging.basicConfig(
            format='%(message)s',
            level=log_level,
            filename=output_file
        )

SNAFU_TO_DECIMAL = {
    '0':  0,
    '1':  1,
    '2':  2,
    '-': -1,
    '=': -2
}

DECIMAL_REMAINDER_TO_SNAFU = {
    0: '0',
    1: '1',
    2: '2',
    3: '=',
    4: '-'
}

def snafu_to_decimal(snafu):
    decimal = 0
    for index,char in enumerate(snafu[::-1]):
        decimal += (5 ** index) * SNAFU_TO_DECIMAL[char]
    return decimal

def decimal_to_snafu(decimal):
    if decimal == 0: return '0'
    running = decimal
    snafu = ''
    while running > 0:
        remainder = running % 5
        snafu = DECIMAL_REMAINDER_TO_SNAFU[remainder] + snafu
        running = round(running/5)
    return snafu

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-f', '--input-file', default='input.txt')
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', '--debug', default=False, action='store_true')
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    decimal_total = 0
    with open(filename) as input_file:
        while (snafu := input_file.readline().rstrip()):
            this_decimal = snafu_to_decimal(snafu)
            decimal_total += this_decimal
            logging.debug(f"{snafu} = {this_decimal} => {decimal_total}")
    snafu_total = decimal_to_snafu(decimal_total)
    logging.info(f"Decimal total: {decimal_total}")
    logging.info(f"SNAFU total: {snafu_total}")
