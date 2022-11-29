from pathlib import Path
import bitstring
import argparse


# bitstring.BitArray("0b"+f"{0x40:014b}"+f"{0x19:06b}"+f"{0x6:04b}").bytes


def read_cuefile(cuefile):


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cuefile", nargs='?')
    parser.add_argument("binfile", nargs='?')
    args = parser.parse_args()

    read_cuefile(args.cuefile)