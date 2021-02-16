import sys
sys.path.insert(0, "/srv/home/zgaleday/pgn")

from pgn.datasets.OneVsManyDataset import OneVsManyDataset
from pgn.datasets.ManyVsManyDataset import ManyVsManyDataset
from pgn.datasets.FPDataset import FPDataset
from pgn.data.data_utils import format_data_directory
from pgn.args import DataArgs


def process_raw(args: DataArgs):
    if args.construct_graphs:
        format_data_directory(args)
        #Add check to see if dataset already processed.
        if args.dataset_type == 'many_v_many':
            ManyVsManyDataset(args)
        elif args.dataset_type == 'one_v_many':
            OneVsManyDataset(args)
        elif args.dataset_type == 'fp':
            FPDataset(args)
        else:
            raise ValueError("Please input a valid dataset type.")


if __name__ == "__main__":

    args = DataArgs()
    # For parsing from terminal
    args.parse_args()
    args.process_args()

    process_raw(args)
