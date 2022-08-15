# Meetings for supervision
Here one can find summaries of meetings.

---
## Meeting 01 <a id="M01"></a>
#### *14th April 2022*
Brief intro to LSMs. There are too many submodels within large LSMs. So important to focus on a smaller bit; e.g. a submodel. Thus, we need to prioritize. First step would be ranking these submodels (e.g. the bits listed by CLM) by (1) importance for policy, (2) connectedness to forests, (3) computational bottleneck and (4) the ease of access of the submodel. Especially point 3 can be split into two different perspectives. (3a) is on the computational load, (3b) or the accuracy in parametrization. These two splits correspond to the 2 main usages of PINNs: (3a) Emulators, which are surrogates for parametric ODE systems and (3b) PINNs for subgrid parametrization that combine large grid models and PINNs for producing more fine scaled analyses.

TODO: make this matrix

MEETING PLAN: weekly 30 min (fixed date thursday or friday TBD).

---
## Meeting 02 <a id="M02"></a>
#### *21st April 2022*
Short meeting with David. Sorry for not sending mail calendar invites. That will be changed for the next meetings.

Decision matrix is still in progress. But criteria scheme was presented.

We discussed the criteria according to notebooks/01_model_exploration/02_submodel_criteria.ipynb . David added an 8th criterion of “Impact of improved model on decisionmakers in climate change issues”.

As the CLM and its 30 submodels include many unrelevant submodels for us, we decided to also consider some “small” LSMs that deal with e.g.

- Vegetation health
- Biomass
- Carbon flux
- Biodiversity
- Land use change

in the ranking.
Also we discussed some important framing questions of the project:

- high resolution of LSMs would be great, because especially owners of small forest areas are numerous but often neglected and unfortunately most of the time suffer from poverty
- it would be cool if it helps to turn a farm into a forest.

Furthermore, we admitted our support for geotorch and that it would need an access to metagenomes.


TODO: make the decision matrix

MEETING PLAN: weekly thursdays 5:30-6:00 pm (with calendar invites)


---
## Meeting 03 <a id="M03"></a>
#### *28th April 2022*
Meeting with Björn and Lucas. Lucas got introduced to the project. Björn pointed out that we want to deal with a key policy decision and that in the PINN appraoch the model is our ground truth. Then one can explore the parameter space.

For fetching the LSMs in a more efficient way, we decided to selectively focus on LSMs that deal with forest restoration / aforestation / deforestation. The CLM submodels should then be explored, if needed.

Furthermore Björn recommended [this paper](https://gmd.copernicus.org/articles/15/1913/2022/) to understand the concept of emulators.

TODO: make the decision matrix



---
## Meeting 04 <a id="M04"></a>
#### *5th May 2022*
Points for discussion:
- Emulator approach (Baker et al. 2022)
    Using sparse gaussian process emulator to model gross primary production emulating JULES
    - Multiple runs of JULES on subset of data with randomized parameters
    - Optimization/training of SGP emulators tuning parameters (+ testing with seperate subset)
    - Running emulator on total dataset
    - Explore influence of model parameters
    What we can learn? As model parameters are not well understood in LSMs, we could use such emulators to find out importance of such.
    Also they show that we can make a lot of final parameter assumptions to split our submodel from others.
- LSMs or VDMs?
    Land surface models are focussing on global processes and their dynamics. For forest restoration they have secondary value, as a deeper understanding of vegetation processes is needed. Vegetation dynamical models (VDM) focus on such, but more feel like computer games
    One very fancy but questionable approach by Pirk et al.
- Problems of LSMs / VDMs (Hanbury-Brown, et al., 2022, Fisher and Koven 2020, Blyth, et al., 2021)
    - Modularity of models (implementation of boundary of submodels)
    - Modeling organism traits:
        - Empirical
        - Optimization
        - Agent competition
    - Processes of contageousness/adjacency (fire, pests, ...)
    - VDM specific: reproductive allocation, dispersal geography
- Got feedback on Master thesis with Fabien, 2 weeks break of LSMs for finishing would be amazing


It was an informative meeting with Björn and Lucas. We went through the points of discussion.
1) We decided against VDMs because of the lack of dealing with performance issues, as such are often dealing with only small ranges. 
2) So back to the LSMs, it seems to be the best to focus on the most established models. These are probably in the area of carbon flux, so maybe GPP or something related. Here it would be interesting to implement [RPC scenarios](https://tntcat.iiasa.ac.at/RcpDb/dsd?Action=htmlpage&page=welcome#rcpinfo) into the model input.
3) Against what I said, Gaussian Processes are not really simple, but hard to implement and very powerful tools in probabilistic computation. Limitation are large sets of parameters.
4) Björn recommended [a review on machine learning in LSMs](https://www.mdpi.com/2673-4834/2/1/11/htm#B55-earth-02-00011) as well as a paragraph of another one (see screenshot in slack).
5) Break for thesis finishing was approved - back on 20th of May.

TODO: make the decision matrix for GPP LSMs. read the papers

MEETING PLAN: next meeting 26th of May


---
## Meeting 05 <a id="M05"></a>
#### *26th May 2022*
**Points for discussion:**

Refresh: subselection of LSMs with policy importance probably best in GPP models


- Progress last week
    - read papers on deep learning in (land surface) modelling
    - investigated on RCP emission scenarios and digged into data opportunities
    - "assembled idea"
    
    
1) Paper insights
    - Flux sites can be "multiplied" using ML
    - Model intercomparisons can be used to constrain uncertainty of hardly describable processes
    - Neural operators are successful emulators of geospatial dynamics
2) RCP scenarios
    - policy relevant emission and land use change simulations
    - 4 independent pathways characterized by their radiative forcing level in the year 2100
    - Modeled parameters: black carbon, organic carbon, $CH_4$, Sulfur, $NO_x$, volatile organic compounds, $CO$, $CO_2$ and $NH_3$, etc., as well as the radiative forcing of the atmosphere.
    - Data available here: [RCP Database](https://tntcat.iiasa.ac.at/RcpDb/dsd?Action=htmlpage&page=download)
3) Back to the CliMA Land model <a id="M05_climaland"></a>
    - After looking on the code, it seems wonderful (though it is refactured) as it is designed in a modular way, such that submodels / subdynamics can be exchanged by others easily. Thus, finetuning and altering it seems to be easy. Also, for GPP it seems to be a model that considers a lot of importnat fluxes within the plants, that usually are neglected. More details on plant processes are summarized by the CliMA Land crew ([Wang, Frankenberg, 2022](https://doi.org/10.5194/bg-2022-96)).
    - Open source
    - Modular + transparent
    - Vibrant community
    - Currently refactored
4) Data for GPP models
    - GPP models need a source for canopy height. Therefore the [new map](https://nlang.users.earthengine.app/view/global-canopy-height-2020) by Lang, et al. (2022) could be used, as it is available.
5) Time for a proposal
    - Building an emulator for CliMA Land v0.1
    - Trying different trainings with/without [constraining uncertainty](../../notebooks/pinN1_stories/02_methodologies/01_deep_learning_lsm.ipynb#paper2).
    - Parameter exploration of CliMA Land
        - Advantage of modularity
        - Submodels can be altered
        - Thus, emulator should be modularly defined
    - RCP simulation output (e.g. emssions) should be included in emulator features
    - Emulator could be used for webapp like [En-ROADS](https://en-roads.climateinteractive.org/scenario.html?v=22.5.0) regarding temperature increase
        - RCP scenarios
        - Different aspects (magnitude, region, ...) of global afforestation (using [Bastin, et al. (2019)](https://doi.org/10.1126/science.aax0848))
        - Accounting for feedback effects like $CO_2$ fertilization
6) APPENDIX 1: Instance model [Expert-N](https://expert-n.uni-hohenheim.de/en)
    - Recommended by Marco Körner (contacted by Björn)
    - Well documented open code model (written in C?!)
    - Pretty extensive and modular
    - Designed to model Nitrogen turnover in soils with plant interaction
    - Documentation could be good source for equations on soil processes 

Meeting was postponed due to conferences. Instead it happened on May 31st, 2:15-3:00 CEST.

Meeting felt very good, and myself challenged to describe the summarized papers. I learnt, that recent papers in computer science can be tricky - not reproduced... David explained [MODIS data](https://lpdaac.usgs.gov/products/mod17a3hgfv061/) a bit, as well as the importance of looking for the actual physical source the datasets are based on (e.g. LAI). Resolution of 10 km x 10 km is very high in climate models. Probably the same can be said for LSMs. 

The question raised, if and to which extend are LSMs spatio-temporal?
So, before really discussing the proposal we decided on doing something similar: trying to run the CliMA Land model for a simple dataset. To get a feeling, we can vary one parameter e.g. $CO_2$ concentration or ratiative forcing and check how the output changes.

One problem, that may come up is the need for performance. Thus, I will contact Mette Lille as my course coordinator if we can get some caccess to Uppmax for it.

As last point, the briefly mentioned Expert-N model could also be a good attempt (maybe later) as it is very extensive but too computatnionally demanding. We should keep it in mind.


TODO: 
	- Try to run the CliMA Land model with simple parameter changes
	- Find out to which extend CliMA land is spatio temporal
	- Find out if we can get Uppmax access

GAVE UP: making decision matrix for published models. Too extensive.

MEETING PLAN: next meeting 9th of June (2nd of June if neccessary)


---
## Meeting 06 <a id="M06"></a>
#### *9th June 2022*
**Points for discussion:**

Refresh: One of the most relevant parameters in LSMs for policy (here, climate) is GPP, the uptake of anorganic carbon by plants. Thus, we focus on it with our emulator. Due to its high detail and implementation we decided to start of with the CliMA Land v0.1 model, which allows to predict GPP given environmental parameters. To start off, it was important to understand the dimensionality of the model and get a feeling of its behaviour.


- Progress last week
    - Trying a vanilla trial of CliMA Land simulation
    - Investigated on its dimensionality
    - Organized UPPMAX access (Part 1 of 2)
    

1) CliMA Land does not have communication between grid cells implemented - as many LSMs:
<details style="background-color:#eeeeee"><summary>We can read in <a href="https://doi.org/10.1029/2018MS001453">Fisher, Koven (2020)</a></summary>
<img src="./figures/01_lsm_subgrids.png"> <img src="./figures/02_lsm_no_diffusion.png"> </img></details>

- Still, as one can model the grid cells oneself an implementation of communicating grid cells would be possible.
- Nonetheless, diffusion and adjacency are important processes in macroecology.


2) [Ran CliMA Land](../../notebooks/pinN1_stories/03_test_models/01_clima_land_vanilla.ipynb) on single grid cell following tutorial.
<details style="background-color:#eeeeee"><summary>Here is a sketch of the global model with detail on one grid cell for GPP modeling:</summary>
<img src="./figures/03_clima_gpp_summary.jpg"> </img></details>

  - Single run needs 7-8 min
  - Needs input parameters on any timestep of the simulation
  - Varied $CO_2$ concentration (fixed value) and saw correlation with GPP
  - Need to investigate negative GPP for biological meaning

3) UPPMAX compute project will probably be approved. Storage (more than 128 GB) project is questionable but we will see... Thanks to Mette Lillie for help. I have a meeting on Tuesday to discuss the further steps.


Meeting with David and Björn. We discussed the trial of the CliMA Land model and were pretty surprised of its temporal independence. Also, my Supervisors were curious of how the model input can be given by other CliMA models. Therefore, I should make a dependency graph.

David mentioned "Auxiliary Supervision" and that LSMs and AI could learn from each other (e.g. about how to build models like Lego).

TODO:
- Find out more about negative GPP in a biological sense
- Visualize the dependency graph of the model (which input can we get from which CliMA models, etc.?)
- Check temporal dependency of model states from previous one (e.g. by shuffling input)

MEETING PLAN: next meeting 16th of June



---
## Meeting 07 <a id="M07"></a>
#### *23rd June 2022*
As I was not ready with the tasks on 16th of June, the meeting was skipped.

**Points for discussion:**

Refresh: We are working with the CliMA Land model to simulate GPP by vegetation. This model has many details of the plants physiology. It was time to find out more about the models complexity and data availability.

- Progress last week
    - Checking temporal dependency of vanilla trial of CliMA Land simulation
    - Checking negative GPP for biological meaning
    - Understanding the bigger picture of CliMA models
    - Investigating data sources for CliMA Land model (preferrably from other CliMA models)
    - Moved to UPPMAX for computation

1) The vanilla trial is [temporally independent](../../notebooks/pinN1_stories/03_test_models/01_clima_land_vanilla.ipynb#tmc). It could be parallelized but it would make sense to just work with a more complex implementation that is temporally dependent - e.g. $CO_2$ as input and output.


2) Biologically, there could be negative NPP, which is the difference between GPP and respiration. Respiration is the active use of higher organic compounds by plants for maintainance/growth metabolism. This could in some situations overcome the carbon fixation by photosynthesis and thus lead to negative NPP. But, what about negative GPP? If one enters the code of CliMA Land, one can see that the values are a result of a negative photosynthesis rate. This is not possible and thus biologically meaningless. We report it as a bug in the specific photosynthesis rates, e.g. [productlimited.jl](https://github.com/CliMA/Land/blob/41f90baa90c5b8e761fdcce5005eebde2f42b26b/src/Photosynthesis/photosynthesis/productlimited.jl) or [rubiscolimited.jl](https://github.com/CliMA/Land/blob/41f90baa90c5b8e761fdcce5005eebde2f42b26b/src/Photosynthesis/photosynthesis/rubiscolimited.jl). 

3) CliMA provides a diverse set of packages that should allow a new earth system modeling framework. Its strength is open access, the soild dynamic and geometric core. On this, several global process models are set. Also the framework involves couplers between process boundaries and libraries for output of different runs. The global process models (usually on grids) base on smaller independent models that can be run on single cells/columns. Another important feature of CliMA is the implementation of solutions with the dogma "calibrate > emulate > sample", which also modular and extendable.

4) The data for the CliMA land model can be used like in the trial (mostly ERA5) or from other CliMA models and thrid party publications. I summarized possibilities in a data table that will be added here after the meeting:
<details style="background-color:#eeeeee"><summary>Data sources could be:</summary>
    <table>
	<thead>
		<tr>
			<th>parameter</th>
			<th>reference</th>
			<th>CliMA model</th>
			<th>simulation necessary</th>
			<th>assumed accessibility</th>
			<th>alternatives</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Plant variables</td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>leaf area index (LAI)</td>
			<td>yuanReprocessingMODISLeaf2011</td>
			<td>GriddingMachine.jl</td>
			<td>no</td>
			<td>easy</td>
			<td>GLOBMAP LAI from https://doi.org/10.1029/2012JG002084</td>
		</tr>
		<tr>
			<td>Vcmax</td>
			<td>smithGlobalPhotosyntheticCapacity2019</td>
			<td>GriddingMachine.jl</td>
			<td>no</td>
			<td>easy</td>
			<td></td>
		</tr>
		<tr>
			<td>Chlorophyll</td>
			<td>croftGlobalDistributionLeaf2020</td>
			<td>-</td>
			<td>no</td>
			<td>medium</td>
			<td>-</td>
		</tr>
		<tr>
			<td>clumping factor</td>
			<td>braghiereUnderestimationGlobalPhotosynthesis2019</td>
			<td>GriddingMachine.jl</td>
			<td>no</td>
			<td>easy</td>
			<td>use other global maps of CI. A review is in fangCanopyClumpingIndex2021</td>
		</tr>
		<tr>
			<td>plant functional type</td>
			<td></td>
			<td>GriddingMachine.jl</td>
			<td>no</td>
			<td>easy</td>
			<td>TODO</td>
		</tr>
		<tr>
			<td>Atmospheric parameters</td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>atmospheric CO2</td>
			<td>OCO-2, RCP output</td>
			<td>-</td>
			<td>no</td>
			<td>medium</td>
			<td>recursive from the output of last time step; ERA5</td>
		</tr>
		<tr>
			<td>wind at 10 m in u (u10)</td>
			<td>-</td>
			<td>ClimateMachine.jl/Atmos</td>
			<td>yes</td>
			<td>medium</td>
			<td>ERA5</td>
		</tr>
		<tr>
			<td>wind at 10 m in v (v10)</td>
			<td>-</td>
			<td>ClimateMachine.jl/Atmos</td>
			<td>yes</td>
			<td>medium</td>
			<td>ERA5</td>
		</tr>
		<tr>
			<td>sun angles</td>
			<td>-</td>
			<td>Insolation.jl</td>
			<td>yes</td>
			<td>easy</td>
			<td>internal implementation</td>
		</tr>
		<tr>
			<td>surface atmosphere pressure</td>
			<td>-</td>
			<td>ClimateMachine.jl/Land</td>
			<td>yes</td>
			<td>tricky</td>
			<td>ERA5/GrddingMachine.jl</td>
		</tr>
		<tr>
			<td>wind (from u10 and v10)</td>
			<td>-</td>
			<td>ClimateMachine.jl/Atmos</td>
			<td>yes</td>
			<td>medium</td>
			<td>ERA5</td>
		</tr>
		<tr>
			<td>diffuse radiation</td>
			<td>ERA5</td>
			<td>-</td>
			<td>no</td>
			<td>medium</td>
			<td></td>
		</tr>
		<tr>
			<td>direct radiation</td>
			<td>ERA5</td>
			<td>-</td>
			<td>no</td>
			<td>medium</td>
			<td></td>
		</tr>
		<tr>
			<td>vapor pressure deficit</td>
			<td>jiangEstimationSoilEvaporation2019</td>
			<td>-</td>
			<td>no</td>
			<td>medium</td>
			<td>ERA5</td>
		</tr>
		<tr>
			<td>Soil and surface parameters</td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>dew point temperature at 2 m deep (d2m)</td>
			<td>-</td>
			<td>ClimateMachine.jl/Land</td>
			<td>yes</td>
			<td>tricky</td>
			<td>ERA5</td>
		</tr>
		<tr>
			<td>temperature at 2 m deep (t2m)</td>
			<td>-</td>
			<td>ClimateMachine.jl/Land</td>
			<td>yes</td>
			<td>tricky</td>
			<td>ERA5</td>
		</tr>
		<tr>
			<td>soil evaporation and vegetation transpiration (evavt)</td>
			<td>jiangEstimationSoilEvaporation2019</td>
			<td>-</td>
			<td>no</td>
			<td>medium</td>
			<td>ERA5</td>
		</tr>
		<tr>
			<td>mean surface direct short wave radiation flux</td>
			<td>ERA5</td>
			<td>-</td>
			<td>no</td>
			<td>medium</td>
			<td></td>
		</tr>
		<tr>
			<td>mean surface downward short wave radiation flux</td>
			<td>ERA5</td>
			<td>-</td>
			<td>no</td>
			<td>medium</td>
			<td></td>
		</tr>
		<tr>
			<td>skin temperature</td>
			<td>-</td>
			<td>ClimateMachine.jl/Land</td>
			<td>yes</td>
			<td>tricky</td>
			<td>ERA5/GrddingMachine.jl</td>
		</tr>
		<tr>
			<td>soil temperatures at 4 levels</td>
			<td>-</td>
			<td>ClimateMachine.jl/Land</td>
			<td>yes</td>
			<td>tricky</td>
			<td>ERA5/GrddingMachine.jl</td>
		</tr>
		<tr>
			<td>volumetric soil water layer at 4 levels</td>
			<td>-</td>
			<td>ClimateMachine.jl/Land</td>
			<td>yes</td>
			<td>tricky</td>
			<td>ERA5/GrddingMachine.jl</td>
		</tr>
		<tr>
			<td>Others</td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>float type day of the year</td>
			<td>-</td>
			<td>-</td>
			<td>-</td>
			<td>-</td>
			<td>-</td>
		</tr>
	</tbody>
</table>
</details>
    

5) On cluster now.


TODO: Contact the CliMA Land authors and start assembling the dataset.


MEETING PLAN: next meeting 7th of July

---
## Meeting 08 <a id="M08"></a>
#### *7th July 2022*
As I was not ready with the tasks on 30th of June, the meeting was skipped.

**Points for discussion:**

Refresh: We are trying to assemble the data for CliMA Land runs.

- Progress last week
    - Checking how chlorophyl is proxied by remote sensing - radiative transfer of different wavelengths
    - Building constructor for non-vanilla model
    - Checked data availability
    - Checked availability of GPP "ground truth" sites (FLUXNET - eddy cov)
    - Baaaaaaah, Julia versions on LMOD, conda and CliMA land
    - Problem with implementing the plant functionl types - vanilla uses default grass but does not seem appropriate. New versions a bit complex... Concerns on CliMA Land are increasing.
    
Most of the data [is available](../../notebooks/pinN1_stories/02_methodologies/03_sources_for_clima_land.ipynb) using `GriddingMachine.jl`. The question is - where do we want to run it? Suggestions?
My idea: 20 flux sites, 20 random places.

Decision: We finally decided to go with the CliMA Land model to develop a protoype for neural operator based emulators on LSMs - regardless of the bugs.

TODO:
- Get data gridded and model ready
- Contact authors for meeting about topic
- Look at the CCAI symposium
- Ask David about meeting and job

MEETING PLAN: 
- Is it possible to skip Aug 4th (help field work lapland), Sep 15th, Sep 22nd (both 10 days dhamma))?
- May have a job from 1st of November
- Next meeting 14th of July

---
## Meeting 09 <a id="M09"></a>
#### *20th July 2022*
Because of some time event clashes, we postponed the meeting from 14th to 20th of July.

**Points for discussion:**

Refresh: We decided to build a prototype neural operator based emulator on CliMA Land - regardless of some flaws.

- Progress last week
    - Started to build constructor for [a less vanilla model](../../notebooks/pinN1_stories/03_test_models/02_clima_land_grownup.ipynb)
    - Downloaded [most of the data](../../notebooks/pinN1_stories/02_methodologies/03_sources_for_clima_land.ipynb) (except of ERA5, which is too large right now)
    - Implemented [regridding of NetCDF files](../../notebooks/pinN1_stories/02_methodologies/04_regrid_clima_land_data.ipynb) flexible to tile sizes and operations

- Questions:
    - Why does multithreading not work? Do you have recommedations of good multithreading basic reads/etc.?
    - How should we grid the dataset?
    - Do you have suggestions how to write the paper for CCAI symposium?

- Plans for next steps:
    - Downlaod ERA5 data using `cdsapi`
    - Regrid the datasets
    - Refine the model
    - Write a part of the paper until 29th July of CCAI symposium

The plans seemed to align common interests and we decided to try it on 180°x360° resolution as done in [Wang, Frankenberg, 2022](https://doi.org/10.5194/bg-2022-96).

TODO:
- Write the paper on [overleaf](https://www.overleaf.com/2512245737rwqrbmsttbfw)
- Then continue to work on the dataset preparation.



