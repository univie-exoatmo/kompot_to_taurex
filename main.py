import parameters as pars
import util


def main():
    util.make_result_dir(pars.PROJECT_NAME)

    # Read the raw Kompot results
    thermal, species = util.read_kompot_results()

    # Convert to usable frame
    kompot_frame = util.prepare_kompot_arrays(thermal, species)

    # Some sanity checks
    util.sanity_plots(thermal, species, kompot_frame)

    # Return for use in TauREx
    util.save_for_taurex(kompot_frame)


if __name__ == "__main__":
    main()
