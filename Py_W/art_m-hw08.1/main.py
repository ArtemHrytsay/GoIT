from pprint import pprint
from pathlib import Path

import argparser as ap
import seed as seed


def main():
    # parser = ap.create_parser()
    # args = parser.parse_args()
    # data = args.data
    data = ""
    
    if not data:
        data = Path.cwd() #/ args.data
    seed.seed(data)

    while True:
        command         = input('Command > ')
        commands        = ap.parse_command(command)
        parsed_commands = ap.parse_commands(commands)
        pprint(parsed_commands)
        continue

if __name__ == "__main__":
    main()
