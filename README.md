# Kompot Radiative Transfer

This small rotutine creates transmission spectra from Kompot output files, using the radative transfer part of TauREx3.
Most things happen automatically in this, but there are some parameters that can be specified in the `parameters.py` file.

## Required input
- `PROJECT_NAME`: Specifies the name of the output folder.
- `THERMAL_PROP`: Fully pathed `ThermalProperties.dat` file.
- `SPECIES_PROP`: Fully pather `species_densities.dat` file.
- `M_PLANET`, `R_PLANET`, and `HOST_RADIUS` are planetary and system parameters in Jupiter and solar units, respectively.
- `WAVE_MIN`, `WAVE_MAX`, and `WAVE_RES`: The wavelength range and resolution to which the transmission spectrum is binned.

## Optional things
Adding the flag `-t` (`--taurex`) will automatically run TauREx3 after making the parameter file. Requires a local TauREx3 installation.


**Note:** Something funky is going on with hot, rocky exoplanets (e.g. some cases Ivan shared with me). BE AWARE!
