# Calibrated data
Delayed mode files
Delayed mode profile files are the same as the real time profile files, except their file names on the GDACs all contain a “D” before the WMO number (e.g. D5900400_001.nc, BD5904179_001.nc). These profile files contain delayed mode adjusted data, which are recorded in the variable <PARAM>_ADJUSTED. The variable DATA_MODE will record ‘D’. Two other variables are also filled in delayed mode, which are <PARAM>_ADJUSTED_QC and <PARAM>_ADJUSTED_ERROR, which record the delayed mode quality control flags and the delayed mode adjustment uncertainty.

Core Argo delayed mode files are available 1 – 2 years after a profile is taken; sometimes earlier. These have been subjected to detailed scrutiny by oceanographic experts and the adjusted salinity has been estimated by comparison with high quality ship-based CTD data and Argo climatologies using the process described by Wong et al, 2003; Böhme and Send, 2005; Owens and Wong, 2009; Cabanes et al, 2016.

For BGC parameters, delayed mode files can be available within 5 – 6 cycles after deployment.  This is because the BGC sensors often return data that are out of calibration, but early adjustment methodologies exist that can significantly improve their accuracy.  Additional delayed mode quality control occurs when a longer record of float data is available.

To learn more about delayed mode quality control, read the papers on the methods linked above or see the ADMT documentation page for core Argo and BGC-Argo quality control documentation.


For each parameter, there are two variables associated with it:  a raw version and an adjusted version.  The raw version can be found in the “PARAM” variable (e.g. TEMP, PRES, DOXY) and the adjusted version can be found in the “PARAM_ADJUSTED” variable (e.g. TEMP_ADJUSTED, PRES_ADJUSTED, DOXY_ADJUSTED).

## Quality Control flags

|QCflag|Meaning|Real time description|Adjusted description|
|:----:|:-----:|:-------------------:|:------------------:|
|0 |No QC performed|No QC performed|XX|
|1 |Good data|All real time QC tests passed|XX|
|2 |Probably good data|	Probably good|XX|
|3 |Bad data that are potentially correctable|Test 15 or Test 16 or Test 17 failed and all other real-time QC tests passed. These  data are not to be used without scientific correction. A flag ‘3’ may be assigned by an operator during additional visual QC for bad |data that may be corrected in delayed mode.|XX|
|4 |Bad data|Data have failed one or more of the real-time QC tests, excluding Test 16. A flag ‘4’ may be assigned by an operator during additional visual QC for bad data that are not correctable.|XX|
|5 |Value changed|Value changed|XX|
|6 |Not currently used |Not currently used|XX|
|7 |Not currently used |Not currently used|XX|
|8 |Estimated |Estimated value (interpolated, extrapolated or other estimation)|XX|
|9 |Missing value|Missing value|XX|

### Example

import numpy as np
import netCDF4
import xarray as xr

import cartopy.crs as ccrs
import cartopy

import matplotlib as mpl
import matplotlib.cm as cm
from matplotlib import pyplot as plt
%matplotlib inline

qcmap = mpl.colors.ListedColormap(['#000000' , '#31FC03' , '#ADFC03' , '#FCBA03' ,'#FC1C03',
                                   '#324CA8' , '#000000' , '#000000' , '#B22CC9', '#000000'])
def colorbar_qc(cmap, **kwargs):
    """Adjust colorbar ticks with discrete colors for QC flags"""
    ncolors = 10
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable, **kwargs)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(range(ncolors))
    return colorbar

iwmo=6900768
file=f"/Users/pvb/Dropbox/Oceanografia/Data/Argo/Floats/{iwmo}/{iwmo}_prof.nc"
prof = xr.open_dataset(file)

All data, with any of the QC flags

fig, ax = plt.subplots(figsize=(15,8))
sc = ax.scatter(prof.PSAL,prof.TEMP,c=prof.CYCLE_NUMBER+pres*0)
cbar=fig.colorbar(sc,ax=ax)
ax.set_title(f"{iwmo}")
ax.grid()

psal=prof.PSAL.where(prof.PSAL_QC.values.astype(float) == 2)
temp=prof.TEMP.where(prof.PSAL_QC.values.astype(float) == 2)

fig, ax = plt.subplots(figsize=(15,8))
sc = ax.scatter(psal,temp,c=prof.CYCLE_NUMBER+pres*0)
cbar=fig.colorbar(sc,ax=ax)
ax.set_title(f"{iwmo}")
ax.grid()
psal

fig, ax = plt.subplots(figsize=(15,8))
sc = ax.scatter(prof.CYCLE_NUMBER+pres*0, 
                prof.PRES, 
                c=prof.PSAL_QC, vmin=0, vmax=9, cmap=qcmap, s=5)
colorbar_qc(qcmap, ax=ax)
ax.set_title(f"{iwmo}")
ax.grid()
ax.set_ylim(0,2000)
ax.invert_yaxis()   

prof.PSAL[90,:]

fig, ax = plt.subplots(figsize=(15,8)) 
scRT = ax.plot(prof.PSAL, prof.TEMP, 'ro', markersize=5)
scAD = ax.plot(prof.PSAL_ADJUSTED, prof.TEMP_ADJUSTED, 'bo',markersize=5)
ax.set_title(f"{iwmo}")
ax.grid()

fig, ax = plt.subplots(figsize=(15,8))
sc = ax.scatter(prof.CYCLE_NUMBER+pres*0, 
                prof.PRES_ADJUSTED, 
                c=prof.PSAL_ADJUSTED_QC, vmin=0, vmax=9, cmap=qcmap, s=5)
colorbar_qc(qcmap, ax=ax)
ax.set_title(f"{iwmo}")
ax.grid()
ax.set_ylim(0,2000)
ax.invert_yaxis()   

