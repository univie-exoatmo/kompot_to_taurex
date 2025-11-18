import argparse
import os

import parameters as pars
import util


def main():
    # Make destinations
    util.make_result_dir(pars.PROJECT_NAME)

    # Read the raw Kompot results
    thermal, thermal_cols, species = util.read_kompot_results()

    # Convert to usable frame
    kompot_frame = util.prepare_kompot_arrays(thermal, thermal_cols, species)

    # Some sanity checks
    util.sanity_plots(thermal, thermal_cols, species, kompot_frame)

    # Return for use in TauREx
    util.save_for_taurex(kompot_frame)


def arguments():
    """CLAs"""
    parser = argparse.ArgumentParser(description="RT script arguments")
    parser.add_argument(
        "-t", "--taurex", help="Run with TauREx",
        action=argparse.BooleanOptionalAction,
        default=False
    )

    return parser.parse_args()


if __name__ == "__main__":
    # Handle CLAs
    args = arguments()

    # Main routine
    main()

    # If desired, run TauREx
    if args.taurex:
        os.system(
            f"taurex -i {pars.PROJECT_NAME}/kompot_taurex.par "
            f"-o {pars.PROJECT_NAME}/kompot_taurex.h5"
        )
        os.system(
            f"taurex-plot -i {pars.PROJECT_NAME}/kompot_taurex.h5 "
            f"-o {pars.PROJECT_NAME}/plots --all"
        )
