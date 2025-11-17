# MORE INTERESTING
# For the TauREx parameter file
GASES               = ["SO2", "H2", "CH4", "H2O", "CO", "CO2", "H2S", "CS2", "OCS"]
M_PLANET            = 1/300
R_PLANET            = 1/11
HOST_RADIUS         = 0.08
HOST_MASS           = 1
HOST_TEMPERATURE    = 2000
WAVE_MIN            = 2
WAVE_MAX            = 5
WAVE_RES            = 500

# LESS INTERESTING
PROJECT_NAME = "Ivan"                                                           # Name of the folder to save the results to
THERMAL_PROP = "/home/simon/Downloads/ThermalProperties.dat"                    # Pathed name of the "ThermalProperties.dat"
SPECIES_PROP = "/home/simon/Downloads/species_densities.dat"                    # Pathed name of the "species.densities.dat"

# HARD-CODED (?)
# Reading the files
TP_SKIPROWS  = 32
SD_SKIPROWS  = 2

# Proper column indices
TP_ALT_COL              = "3"
SD_ALT_COL              = "Altitude_(cm)"
TP_PRESSURE_COL         = "9"
TP_TEMPERATURE_COL      = "8"
TP_TOTAL_ND_COL         = "4"

# Replacement keys for parameter file
REPLACE_KEYS = {
        "planet_mass": M_PLANET,
        "planet_radius": R_PLANET,
        "radius": HOST_RADIUS,
        "mass": HOST_MASS,
        "gases": ", ".join(GASES),
        "wavelength_res": f"{WAVE_MIN}, {WAVE_MAX}, {WAVE_RES}"
    }

###############################################################################
# A WHOLE TAUREX PARAMETER FILE
TAUREX_PARFILE = """
[Global]
xsec_path = /home/simon/Code/TauREx/source/ATMOSPHERE/xsec/exomol
cia_path = /home/simon/Code/TauREx/source/ATMOSPHERE/cia/HITRAN


[Chemistry]
chemistry_type = file
filename = chemistry_profile.dat
gases = N2, H2, H2O, CH4, C2H2, C2H4, CO, CO2, NO2, N2O, HCN

[Temperature]
profile_type = file
filename = pt_profile.dat
temp_col = 0
temp_units = K
press_col = 1
press_units = bar
reverse = True
# By default, assumes whitespace as delimiter


[Pressure]
profile_type = Simple
atm_min_pressure = 1e-7
atm_max_pressure = 1e0
nlayers = 200


[Planet]
planet_type = Simple
planet_mass = 7.08e-5
planet_radius = 0.00314635

[Star]
star_type = blackbody
radius = 0.12
mass = 0.0898
temperature = 2566


[Model]
model_type = transmission

    [[Absorption]]

    [[Rayleigh]]

    [[CIA]]
    cia_pairs = H2-H2,


[Binning]
bin_type = manual
wavelength_res = 1, 12, 100
"""
