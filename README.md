# Paleogeographic Reconstruction of Oil and Gas Reservoirs

The following scripts recalculate and plot present day oil and gas reservoir data into a paleographic setting using as basis rotation models and features (for this case continental block features). The Pygplates library provides a sound way to achieve this (see documentation: http://www.gplates.org/docs/pygplates/index.html), also, several resources are found on https://www.earthbyte.org/category/resources/, where researchers upload their reconstruction models.

For the Cenozoic and Early Paleozoic Eras the reconstruction model after Matthews & others (2016) was used and for the Neoproterozoic Era the model after Merdith & others (2017). For the Late Paleozoic no reconstruction was made because there are no important reservoirs from this age but also because there's no good reconstruction model data yet. Lastly, the used reservoir data is found on: https://worldmap.harvard.edu/data/geonode:giant_oil_and_gas_fields_of_the_world_co_yxz. 

When running global.py a directory containing two shapefiles is created in a "reconstructions" parent directory: one of them contains the continental blocks rotated for a particular period and the other the reconstructed reservoir data for that same age span. Reservoirs are grouped by periods and each reservoir group is then further categorised by estimated ultimate recovery (EUR MMBO) and lithology. The plotting.py script then plots a map using these shapefiles and the pertinent classification.

### Prerequisites

Download Pygplates library on: https://sourceforge.net/projects/gplates/files/pygplates/beta-revision-12/ and move the directory to the same working directory. Make sure to edit accordingly line 8 on the global.py script by adding the correct path depending on the downloaded version.

Also make sure you have installed all other third libraries needed to run the scripts. The interpreter should give you a heads up otherwise.

## Acknowledgments

* This kind of visualisations gives insight into oil & gas provinces’ provenance as well as a big general picture that could allow estimations of possible, not yet discovered, reservoirs.
* These visualisations are also a great educational tool to couple reconstructions with current data, since this reservoir data can be classified in a myriad of ways.
