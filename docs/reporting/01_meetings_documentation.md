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