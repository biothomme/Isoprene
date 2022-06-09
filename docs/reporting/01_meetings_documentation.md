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