"""Create visual diagram of data flow through ILS systems.

Reads three spreadsheets of data describing hosting environments, systems, and data flows,
and produces a diagram.
"""

import argparse
import configparser
import csv
import logging
import sys

import netdiag


def read_config(filename):
    """Parse the named config file and return an config object.

    Place holder, not yet in use.
    """

    config = configparser.ConfigParser()
    config.read(filename)
    return config


def parse_args():
    """Parse command line arguments and return a Namespace object."""

    epilog_header = "INPUT FILES\n"
    env_help = read_environments.__doc__.partition('.')[2]
    sys_help = read_systems.__doc__.partition('.')[2]
    df_help = read_dataflows.__doc__.partition('.')[2]
    epilog = epilog_header + env_help + sys_help + df_help

    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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

def read_dataflows(filename):
    """Reads CSV file of data flow information, returns list.

    DATAFLOW file:
    The CSV file of dataflow information must have the following columns,
    with these headers, at a minimum:

    source: Source system for data, as named in Systems.
    target: Target system for data, as named in Systems.
    mode:   Data transfer is read-only (`r`) or it writes to storage (`w`).
    """

    dataflows = []

    with open(filename) as csvfile:
        sys_reader = csv.DictReader(csvfile)
        for row in sys_reader:
            if row['source'] and row['target']:
                src = netdiag.to_code(row['source'])
                trgt = netdiag.to_code(row['target'])
                mode = row['mode']
                df = netdiag.DataFlow(src, trgt, mode)
                dataflows.append(df)
    return dataflows

def read_environments(filename):
    """
    Reads CSV file of environment information, returns dictionary.

    ENVIRONMENT file:
    The CSV file of Environment information must have the following columns,
    with these headers, at a minimum:

    Environment: Name of the environment, will be referenced in the Systems
                 spreadsheet.
    Host:        The name of the hosting provider.
    On Campus:   Indicate if this is on campus, the string will be evaluated
                 as a boolean (e.g. 'x' evaluates as `True`, blank evaluates
                 as False).
    """

    environments = []

    with open(filename) as csvfile:
        sys_reader = csv.DictReader(csvfile)
        for row in sys_reader:
            if row['Environment']:
                code = netdiag.to_code(row['Environment'])
                env = netdiag.Environment(code, row['Environment'],
                                          row['Host'], bool(row['On Campus']))
                environments.append(env)
    return environments

def read_systems(filename):
    """
    Reads CSV file of system information, returns dictionary.

    SYSTEMS file:
    The CSV file of system information must have the following columns, with
    these headers, at a minimum:

    System:      Name of the system, will be referenced in the data flow
                 spreadsheet.
    Environment: The name of the environment this system is housed in, may be
                 blank if it is not in an environment that we feel we need to
                 make particular note of.
    """

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

    # Note: order of reading is significant when building up the
    # network. must read environments, then systems, then
    # dataflow. There are dependencies among the data and how it is
    # interpreted.

    network = netdiag.Network('ILS')
    for e in read_environments(args.environments):
        network.add_environment(e)
    for s in read_systems(args.systems):
        network.add_system(s)
    for df in read_dataflows(args.data_flow):
        network.add_dataflow(df)

    dot = network.digraph2()
    print(dot.render(format='png'))

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
