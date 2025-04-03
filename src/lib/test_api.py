# import xarray as xr
# import matplotlib.pyplot as plt
# from meteofetch import Arpege01
# def test():
#     dim = "points"
#     coords = ["Paris", "Edimbourg"]
#     x = xr.DataArray([2.33, -3.18], dims=dim)
#     y = xr.DataArray([48.9, 55.95], dims=dim)

#     datasets = Arpege01.get_latest_forecast(paquet="SP1", variables="t2m")

#     plt.figure(figsize=(8, 3))
#     datasets["t2m"].sel(lon=x, lat=y, method="nearest").assign_coords(
#         {dim: coords}
#     ).plot.line(x="time")
    

