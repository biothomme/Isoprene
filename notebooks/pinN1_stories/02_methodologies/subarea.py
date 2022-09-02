import geoviews as gv
import xarray as xr

from utils_subareaselection import fraction_nonnan

class SubArea:
    def __init__(self, point:xr.DataArray, array_data:xr.DataArray, length_edge:dict) -> None:
        self.point = point
        self.extract_subarea(array_data, length_edge)
        return
    
    def extract_subarea(self, array_data:xr.DataArray, length_edge:dict) -> None:
        self.area = array_data
        for dim in array_data.dims:
            self.area = self.area.where(
                (self.area[dim] >= self.point[dim]-length_edge[dim]/2) & 
                (self.area[dim] < self.point[dim]+length_edge[dim]/2),
            drop=True)
        return
    
    def check_nonnan_ratio(self) -> float:
        if not hasattr(self, "rnn") : self.rnn = fraction_nonnan(self.area)
        return self.rnn
    
    def check_overlap(self, other) -> bool:
        return any(map(
            lambda dm : len(xr.merge([self.area, other.area])[dm].values) >= len(self.area[dm])*2,
            self.area.dims
        ))
        
    def plot(self, palette="magma", verbose=True, value_frame=None, **kwargs):
        gvds = gv.Dataset(self.frame_area(value_frame))

        gvimage = gvds.to(gv.Image, ['lon', 'lat'], 'data')

        if verbose : fig = gvimage.opts(cmap=palette, **kwargs)
        else : fig = gv.output(gvimage.opts(cmap=palette, **kwargs))
        return fig
    
    def frame_area(self, value_frame):
        if value_frame is None : return self.area
        area_framed = self.area.copy()
        for dim in self.area.dims:
            arrays_dim = {
                dm : area_framed[dm][[0, -1]] if dm == dim
                else area_framed[dm]
                for dm in self.area.dims
            }
            area_framed.loc[arrays_dim] = value_frame
        return area_framed
        
    def set_time(self, time_point) -> None:
        self.time = time_point
        return
    
    def to_dict(self):
        dict_sa = {"fraction_nonnan": self.check_nonnan_ratio().values.item()}
        
        if hasattr(self, "time"):
            dict_sa["time"] = self.time.format("YYYY-MM-DD HH:mm:ss ZZ")
        
        for dim in self.area.dims:
            dict_sa[f"{dim}_min"] = min(self.area[dim].values)
            dict_sa[f"{dim}_max"] = max(self.area[dim].values)
            dict_sa[f"{dim}_center"] = self.point[dim].values.item()
            dict_sa[f"{dim}_card"] = len(self.area[dim].values)
            
        return dict_sa