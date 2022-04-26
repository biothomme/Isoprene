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









