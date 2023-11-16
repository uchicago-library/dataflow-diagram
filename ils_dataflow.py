import argparse
import configparser
import csv
import logging
import sys

import netdiag


"""Create visual diagram of data flow through ILS systems"""


def read_config(filename):
    """Parse the named config file and return an config object"""

    config = configparser.ConfigParser()
    config.read(filename)
    return config


def parse_args():
    """Parse command line arguments and return a Namespace object."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-d",
        "--data_flow",
        help="data flow descriptions in CSV file",
    )
    parser.add_argument(
        "-e",
        "--environments",
        help="environment descriptions in CSV",
    )
    parser.add_argument(
        "-s",
        "--systems",
        help="system descriptions in CSV",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        help="Output file",
        default=sys.stdout,
        type=argparse.FileType("w"),
    )
    parser.add_argument(
        "-C", "--config_file", help="Name of config file", default="config.ini"
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity level"
    )
    return parser.parse_args()


def read_environments(filename):
    """Reads CSV file of environment information, returns dictionary"""

    environments = []

    with open(filename) as csvfile:
        sys_reader = csv.DictReader(csvfile)
        for row in sys_reader:
            if row['Environment']:
                code = netdiag.to_code(row['Environment'])
                env = netdiag.Environment(code, row['Environment'], row['Host'])
                environments.append(env)
    return environments

def read_systems(filename):
    """Reads CSV file of system information, returns dictionary"""

    systems = []

    with open(filename) as csvfile:
        sys_reader = csv.DictReader(csvfile)
        for row in sys_reader:
            if row['System']:
                code = netdiag.to_code(row['System'])
                s = netdiag.System(code, row['System'], row['Environment'])
                systems.append(s)
    return systems

def parse_data(line):
    """Placeholder function for parsing input data"""
    return line


def process_data(data):
    """Placeholder for processing the data"""
    return data


def main():
    args = parse_args()
    config = read_config(args.config_file)
    # Logic or function to override config values from the command line arguments would go here

    network = netdiag.Network('ILS')
    for e in read_environments(args.environments):
        network.add_environment(e)
    for s in read_systems(args.systems):
        network.add_system(s)

    network.write_graphviz(sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
        
