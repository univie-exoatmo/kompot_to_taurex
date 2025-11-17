import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import shutil
import typing as tp

import parameters as pars


def replace_taurex_parameter(parfile: str, parname, parvalue: tp.Any) -> str:
    custom_parfile = re.sub(
        rf"\b{parname}\s*=\s*[^#\n]+", f"{parname} = {parvalue}", parfile
    )

    return custom_parfile


def write_taurex_par_file(p_min, p_max, n_layers) -> None:
    custom_parfile = pars.TAUREX_PARFILE

    # User-defined replacement
    for key, value in pars.REPLACE_KEYS.items():
        custom_parfile = replace_taurex_parameter(custom_parfile, key, value)

    # Conversion-depended replacements
    # Keep in mind that the p_min and p_max values need to be given in Pa!
    for key, value in zip(
        ["atm_min_pressure", "atm_max_pressure", "nlayers"],
        [p_min * 1e5, p_max * 1e5, n_layers]
    ):
        custom_parfile = replace_taurex_parameter(custom_parfile, key, value)

    # Create a parameter-file
    with open(f"{pars.PROJECT_NAME}/kompot_taurex.par", "w") as f:
        f.write(custom_parfile)

    return


def save_for_taurex(kompot_frame: pd.DataFrame) -> None:
    # P-T file
    tp_subframe = kompot_frame[["temperature_K", "pressure_bar"]]
    tp_subframe.to_csv(
        f"{pars.PROJECT_NAME}/pt_profile.dat", sep=" ",
        index=False, header=False
    )

    # Chemisty file
    species_subframe = kompot_frame[[f"{gas}_MR" for gas in pars.GASES]]
    species_subframe.to_csv(
        f"{pars.PROJECT_NAME}/chemistry_profile.dat", sep=" ",
        index=False, header=False
    )

    # Some information for the TauREx parameter file
    nlayers = tp_subframe.shape[0]
    p_min = np.min(tp_subframe["pressure_bar"])
    p_max = np.max(tp_subframe["pressure_bar"])

    # Make the TauREx parameter file from this
    write_taurex_par_file(p_min, p_max, nlayers)


def sanity_plots(
        tp_frame: pd.DataFrame, sd_frame: pd.DataFrame,
        convert_frame: pd.DataFrame
) -> None:
    fig, ax = plt.subplots(ncols=2, constrained_layout=True)
    ax_pt, ax_vmr = ax

    # Thermal profile
    ax_pt.plot(
        tp_frame[pars.TP_TEMPERATURE_COL], tp_frame[pars.TP_PRESSURE_COL],
        label="From Kompot",
    )
    ax_pt.plot(
        convert_frame["temperature_K"], convert_frame["pressure_bar"],
        label="Converted", alpha=0.5
    )

    # Mixing ratio profiles
    for gas in pars.GASES:
        ax_vmr.plot(
            np.log10(convert_frame[f"{gas}_MR"]),
            convert_frame["pressure_bar"], label=gas
        )

    for axis in ax:
        axis.legend()
        axis.set(yscale="log", ylabel="Pressure [bar]")
        axis.invert_yaxis()
    ax_pt.set(xlabel="Temperature [K]")
    ax_vmr.set(xlabel="Mixing ratio")

    fig.savefig(f"{pars.PROJECT_NAME}/plots/sanity_check.pdf")
    return


def read_kompot_results() -> tuple:
    thermal_properties_file = pd.read_csv(
            pars.THERMAL_PROP, skiprows=pars.TP_SKIPROWS, delimiter="\\s+"
    )
    species_densities_file = pd.read_csv(
            pars.SPECIES_PROP, skiprows=pars.SD_SKIPROWS, delimiter="\\s+"
    )

    return thermal_properties_file, species_densities_file


def read_kompot_column(
        raw_frame: pd.DataFrame, select_column: str,
        restrict_indicies: np.ndarray
) -> np.ndarray:
    array = raw_frame[select_column].to_numpy()[restrict_indicies]

    return array


def prepare_kompot_arrays(
        tp_frame: pd.DataFrame, sd_frame: pd.DataFrame
):
    # Usable data frame
    return_frame = pd.DataFrame()

    # Index overlap from both files
    tp_idxs, sd_idxs = homogenise_indicies(tp_frame, sd_frame)

    # FROM THERMAL PROPERTIES
    return_frame["pressure_bar"] = read_kompot_column(
        tp_frame, pars.TP_PRESSURE_COL, tp_idxs
    )
    return_frame["temperature_K"] = read_kompot_column(
        tp_frame, pars.TP_TEMPERATURE_COL, tp_idxs
    )
    return_frame["total_nd"] = read_kompot_column(
        tp_frame, pars.TP_TOTAL_ND_COL, tp_idxs
    )

    # FROM SPECIES DENSITIES
    for species in pars.GASES:
        array = read_kompot_column(sd_frame, species, sd_idxs)
        return_frame[f"{species}_MR"] = array / return_frame["total_nd"]

    return return_frame


def homogenise_indicies(
        tp_frame: pd.DataFrame, sd_frame: pd.DataFrame
) -> tuple:
    altitude_tp = np.round(
        tp_frame[pars.TP_ALT_COL].to_numpy(), decimals=2
    )
    altitude_sd = np.round(
        sd_frame[pars.SD_ALT_COL].to_numpy() * 1e-5, decimals=2
    )

    # Returns overlap array, and overlap indicies from arrays 1 & 2
    _, tp_idxs, sd_idxs = np.intersect1d(
        altitude_tp, altitude_sd, return_indices=True
    )

    return tp_idxs, sd_idxs


def make_result_dir(project_name: str = "kompot"):
    # Sub-directory names
    KOMPOT_DATA = "kompot_data"
    PLOTS = "plots"

    # Make a save director (or overwrite if it exists)
    directory_safety_check(project_name)

    # Folder sub-structure
    for folder_name in [KOMPOT_DATA, PLOTS]:
        os.makedirs(f"{project_name}/{folder_name}")

    # Also save the Kompot files used as input
    for filename in [pars.THERMAL_PROP, pars.SPECIES_PROP]:
        shutil.copy2(filename, f"{project_name}/{KOMPOT_DATA}")


def directory_safety_check(dir_name: str = "kompot"):
    try:
        os.makedirs(dir_name)
    except FileExistsError:
        choice = input(f"{dir_name} already exists. Overwrite? [y/n] ")

        if choice.lower() == "y":
            shutil.rmtree(dir_name)
            os.makedirs(dir_name)
        else:
            print("Exiting...")
            exit()
