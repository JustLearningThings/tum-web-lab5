import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='go2web')
    parser.add_argument('--url', '-u', type=str, help='website URL')
    parser.add_argument('--search', '-s', type=str, nargs='+', help='search the terms followed by the flag')

    args = parser.parse_args()

    return args