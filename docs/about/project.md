# The Project

## What is Marine Energy Resource Characterization?

The United States has an estimated **2,300 TWh/yr** of technically available marine energy from waves, tides, ocean currents, and thermal gradients, which is roughly 57% of U.S. electricity generation [@general_kilcher2021_marine]. But potential on paper is not the same as a deployable resource. Before a wave energy converter or tidal turbine can be sited, financed, and built, developers need to know what conditions at that location actually look like: how fast currents run, how often extreme events occur, and how much energy is available across seasons and years.

Gathering that knowledge purely from field measurements is not practical. Instruments at a single mooring record one point in space, and deploying sensors across every candidate site along thousands of miles of U.S. coastline is too expensive and logistically infeasible.

**Resource characterization solves this problem through hindcast modeling.** A small number of high-quality field observations (current meters, wave buoys, tide gauges) are used to configure and validate high-resolution numerical ocean models. These models are then run across decades and large spatial domains, producing a continuous, spatially complete record of past ocean conditions. The result is a clean, consistent dataset that fills in the gaps both spatially, covering areas where no instrument was ever deployed, and temporally, providing uninterrupted records across years or decades where field campaigns lasted only weeks or months.

## Why It Matters: De-Risking Marine Energy Deployment

Uncertainty is the primary barrier to marine energy investment. Developers, financiers, and regulators all need answers to the same basic questions before committing to a project:

- **Economic viability**: Is there enough energy at this site to generate power at a competitive cost over a project lifetime? What does the seasonal and year-to-year variability look like?
- **Device durability**: What are the extreme loads a device must survive? How often do high-energy sea states or peak tidal velocities occur?
- **Site context**: How does this site compare to others? Are there depth, directional, or timing characteristics that favor or complicate deployment?

Hindcast datasets help answer each of these questions. By providing decades of reconstructed ocean conditions at high spatial resolution, they allow developers to characterize a site before any equipment is deployed, identify good locations across a region, design devices to match real load conditions, and support environmental review, all at a fraction of the cost of a field campaign.

## Data Products

The datasets produced by this project are made available at three levels, each designed to match a different stage of project development and a different type of user.

Reconnaissance level products are time-averaged summaries of wave and tidal conditions mapped across U.S. waters. These are accessible through the [Marine Energy Atlas](https://maps.nlr.gov/marine-energy-atlas) and are designed for investors, policymakers, regional energy planners, and the general public who need to understand where resources exist and how they compare across regions, without needing to work with raw data.

Site feasibility products provide programmatic access to the underlying hindcast time-series at specific coordinates. Marine energy developers, researchers, and coastal communities can pull current velocity, wave height, power density, and related variables for a site of interest using MHKiT ([Python](https://mhkit-software.github.io/MHKiT/WPTO_hindcast_example.html), [MATLAB](https://mhkit-software.github.io/MHKiT/mhkit-matlab/WPTO_hindcast_example.html)) [@general_fao2025_mhkit_python; @general_simms2025_mhkit_matlab] for wave data or the [us-marine-energy-resource Python library](https://github.com/US-Marine-Energy-Resource/us-marine-energy-resource-python) for tidal data. This level supports resource screening, preliminary energy calculations, and site-to-site comparison.

Spatiotemporal analysis products provide the full hindcast datasets covering complete spatial domains and multi-decade time spans. These are freely available through AWS S3 (wave: `s3://wpto-pds-us-wave` [@general_yang2020_wave_hindcast], tidal: `s3://marine-energy-data/us-tidal/` [@general_yang2025_tidal_hindcast]) and are intended for large-scale site optimization, device design studies, machine learning applications, and IEC-compliant resource assessments. Formal dataset citations are maintained through the [Marine and Hydrokinetic Data Repository (MHKDR)](https://mhkdr.openei.org).

## Standards

All datasets are developed with reference to the following standards and conventions:

- **[IEC TS 62600 Marine Energy Standards](https://www.iec.ch/dyn/www/f?p=103:7:::::FSP_ORG_ID:1316)**: International standards for tidal and wave energy resource assessment
- **[CF Conventions](https://cfconventions.org)**: Climate and Forecast metadata conventions for interoperability
- **[ACDD](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3)**: Attribute Convention for Data Discovery

## License

This software is licensed under the BSD 3-Clause License.

Copyright 2025 Alliance for Energy Innovation, LLC

This software was developed at least in part by Alliance for Energy Innovation, LLC ("Alliance") under Contract No. DE-AC36-08GO28308 with the U.S. Department of Energy and the U.S. Government retains for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in the software to reproduce, prepare derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so.

## References

<div class="bibliography"></div>

--8<-- "docs/_general_cite_widget.md"
