# MORE INTERESTING
# For the TauREx parameter file
GASES               = ["H2", "CH4", "CO", "CO2", "SO2", "H2O"]
M_PLANET            = 1
R_PLANET            = 1
HOST_RADIUS         = 1
WAVE_MIN            = 1
WAVE_MAX            = 10
WAVE_RES            = 500

# LESS INTERESTING
PROJECT_NAME = "kompot"
THERMAL_PROP = "/PATH/TO/ThermalProperties.dat"
SPECIES_PROP = "/PATH/TO/species_densities.dat"


###############################################################################
# A WHOLE TAUREX PARAMETER FILE
TAUREX_PARFILE = """
[Global]
xsec_path = /home/simon/Code/TauREx/source/ATMOSPHERE/xsec/exomol
cia_path = /home/simon/Code/TauREx/source/ATMOSPHERE/cia/HITRAN


[Chemistry]
chemistry_type = file
filename = chemistry_profile.dat
gases = H2, He

[Temperature]
profile_type = file
filename = pt_profile.dat
temp_col = 0
temp_units = K
press_col = 1
press_units = bar
reverse = True


[Pressure]
profile_type = Simple
atm_min_pressure = 1e-7
atm_max_pressure = 1e0
nlayers = 200


[Planet]
planet_type = Simple
planet_mass = 1.0
planet_radius = 1.0

[Star]
star_type = blackbody
radius = 1.0


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

# NO TOUCHING
# Replacement keys for parameter file
REPLACE_KEYS = {
        "planet_mass": M_PLANET,
        "planet_radius": R_PLANET,
        "radius": HOST_RADIUS,
        "gases": ", ".join(GASES),
        "wavelength_res": f"{WAVE_MIN}, {WAVE_MAX}, {WAVE_RES}"
}
