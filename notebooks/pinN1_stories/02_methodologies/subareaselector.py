# package imports
from typing import Any
import geoviews as gv
import numpy as np
import xarray as xr

# local imports
from subarea import SubArea

class SubAreaSelector:
    """ SubAreaSelector

    _extended_summary_
    """
    def __init__(self, array_data:xr.DataArray, dict_dimcard:dict, ratio_nonan:float=.5) -> None:
        """__init__ SubAreaSelector

        _extended_summary_

        Args:
            array_data (xr.DataArray): _description_
            dict_dimcard (dict): _description_
            ratio_nonan (float, optional): _description_. Defaults to .5.
        """
        self.data = array_data
        self.subareas = []
        
        # we want to ensure that the cardinality dictionary
        # provides the same dimensions as the data
        assert all(map(lambda x : x in dict_dimcard.keys(), array_data.dims))
        
        self.dims = self.data.dims
        self.card = dict_dimcard
        
        self.rnn = ratio_nonan
        
        # the data array has a boundary frame that does not 
        # allow full subarea selection
        self.get_core()
        
        # also for perfomrance reason we compute
        # the lengths of the dimensional edges
        self.get_length_edges()
        return
    
    def get_core(self) -> None:
        self.core = self.data
        for dim in self.dims:
            self.core = self.core.isel(
                {dim: slice(self.card[dim]-1, -self.card[dim])}
                )
        return
    
    def get_length_edges(self) -> None:
        self.edges = {
            dm: np.subtract(
                    *self.data[dm].values[[self.card[dm], 0]]
            ) for dm in self.dims
        }
        return

    def draw_point(self, only_core=True, avoid_nan=True) -> xr.DataArray:
        if only_core : array_data = self.core
        else : array_data = self.data
        
        p = {dm: np.random.choice(array_data[dm]) for dm in self.dims}
        point = array_data.loc[p]
        
        if avoid_nan and np.isnan(point):
            return self.draw_point(only_core=only_core)
        else : return point

    def draw_subarea(self, apply_nan_thresh=True):
        point = self.draw_point()
        subarea = SubArea(point, self.data, self.edges)
        if apply_nan_thresh and subarea.check_nonnan_ratio() < self.rnn:
            return self.draw_subarea()
        return subarea
    
    def draw_subareas(self, n_redraw=10000, n_prune=5, n_subareas=100) -> list:
        while len(self.subareas) < n_subareas:
            count_redraw = 0
            subarea = None
            while count_redraw < n_redraw and subarea is None:
                sa = self.draw_subarea()
                if all(map(sa.check_overlap, self.subareas)):
                    subarea = sa
                count_redraw += 1
                
            print(f"We have {len(self.subareas)} subareas.")
            if subarea is None : self.prune_subareas(n_prune)
            else : self.subareas.append(subarea)
        return self.subareas
    
    def prune_subareas(self, n_prune) -> None:
        for i in range(n_prune):
            idx = np.random.randint(len(self.subareas))
            sa_pruned = self.subareas.pop(idx)
        return
    
    def plot(self, palette="magma", verbose=False) -> Any:
        gvds = gv.Dataset(self.data)

        gvimage = gvds.to(gv.Image, ['lon', 'lat'], 'data')

        fig_dims = {"height": 800, "width": 1200}
        if verbose:
            fig = gvimage.opts(
                cmap=palette, colorbar=True, **fig_dims) * gv.feature.coastline
        else:
            fig = gv.output(
                gvimage.opts(cmap=palette, colorbar=True, **fig_dims) *
                    gv.feature.coastline)
        return fig
    
    def plot_subareas(self, palette_base="magma", palette_subareas="viridis"):
        fig = self.plot(palette=palette_base, verbose=True)
        for subarea in self.subareas:
            fig *= subarea.plot(palette=palette_subareas, verbose=True,
                                value_frame=np.max(self.data))
        return gv.output(fig)
        