# package imports
from typing import Any
import arrow
import csv
from datetime import date, timedelta
import geoviews as gv
import numpy as np
import os
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
            dm: np.abs(np.subtract(
                    *self.data[dm].values[[self.card[dm], 0]]
            )) for dm in self.dims
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
        
        # sometimes the subareas are not fitting the expected cardinalities
        for dim in subarea.area.dims:
            if len(subarea.area[dim].values) != self.card[dim]:
                return self.draw_subarea()
        return subarea
    
    def draw_subareas(self, n_redraw=10000, n_prune=5, n_subareas=100,
                      file_csv=None, **kwargs) -> list:
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
            else:
                self.subareas.append(subarea)
                if file_csv is not None:
                    self.to_csv(file_csv, subarea=subarea, **kwargs)
        return self.subareas
    
    def prune_subareas(self, n_prune) -> None:
        for i in range(n_prune):
            idx = np.random.randint(len(self.subareas))
            sa_pruned = self.subareas.pop(idx)
        return
    
    def plot(self, palette="magma", verbose=False) -> Any:
        gvds = gv.Dataset(self.data)

        gvimage = gvds.to(gv.Image, list(self.dims).sort(reverse=True), self.data.name)

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


    def to_csv(self, file_out, subarea=None, force=False, append=True):
        if os.path.exists(file_out) and not force and not (
            append and subarea is None) : return

        # we store the filename to allow continuous writing
        if not hasattr(self, "csv"):
            self.csv = file_out
            self.handle = open(self.csv, "w" if (force or not append) else "a")

        if not hasattr(self, "writer"):
            self.writer = None

        if self.csv != file_out and self.writer is not None:
            self.csv = file_out
            self.handle = open(self.csv, "w" if (force or not append) else "a")


        if subarea is None:
            for dict_sa in map(lambda x : x.to_dict(), self.subareas):
                if self.writer is None:
                    self.writer = csv.DictWriter(
                        self.handle, fieldnames=dict_sa.keys())
                    self.writer.writeheader()
                self.writer.writerow(dict_sa)
        else:
            dict_sa = subarea.to_dict()
            if self.writer is None or self.csv != file_out:
                self.writer = csv.DictWriter(
                    self.handle, fieldnames=dict_sa.keys())
                self.writer.writeheader()
            self.writer.writerow(dict_sa)
            self.handle.flush()
        return
            
        
        
class TemporalSubAreaSelector(SubAreaSelector):
    def __init__(self, array_data: xr.DataArray, dict_dimcard: dict,
                 date_start:str, date_end:str, time_step:timedelta,
                 ratio_nonan: float=0.5) -> None:
        super().__init__(array_data, dict_dimcard, ratio_nonan)
        
        self.sa_temp = []
        
        self.start = arrow.get(date_start)
        self.end = arrow.get(date_end)
        self.step = time_step
        
    def draw_subareas(self, time_nooverlap:timedelta, file_csv=None, **kwargs) -> dict:
        n_nooverlap = time_nooverlap.total_seconds() / self.step.total_seconds()
        time_current = self.start
        c = 1
        while time_current <= self.end:
            # if enough time passed we remove elemtents from list that should
            # not spatially overlap
            if len(self.sa_temp) > n_nooverlap:
                self.sa_temp.pop(0)
            
            # we look for a subarea
            subarea = None
            while subarea is None:
                sa = self.draw_subarea()
                if all(map(sa.check_overlap, self.sa_temp)):
                    subarea = sa
                
            
            print(f"We have {c} subareas.")
            # each subarea we find, we step forward in time...
            subarea.set_time(time_current)
            self.sa_temp.append(subarea)
            if file_csv is not None:
                self.to_csv(file_csv, subarea=subarea, **kwargs)
            else : self.subareas.append(subarea)
            time_current += self.step
            c += 1
        return self.subareas