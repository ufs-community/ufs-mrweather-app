################################################################################
####  Python Script Documentation Block
#
# Script name:       	plot_mrw_cloud_diff.py
# Script description:  	Generates plots of cloud cover from UFS MRW App 
#           Graduate Student Test control, experiment, and difference
#           between control and experiment
#               
#
# Authors:  Sam Ephraim		Org: EPIC Lapenta Intern		Date: 2021-07-02
#           Based off of work from Ben Blake and David Wright
#
# Instructions:		Make sure all the necessary modules can be imported.
#                       Five command line arguments are needed:
#                       1. Cycle date/time in YYYYMMDDHH format
#                       2. Forecast hour in HHH format
#                       3. CTRL_DIR: Control directory
#                          -Postprocessed data should be found in the directory:
#                            CTRL_DIR/run/
#                       4. EXPT_DIR: Experiment directory
#                          -Postprocessed data should be found in the directory:
#                            EXPT_DIR/run/
#                       5. CARTOPY_DIR:  Base directory of cartopy shapefiles
#                          -Shapefiles cannot be directly downloaded to NOAA
#                            machines from the internet, so shapefiles need to
#                            be downloaded if geopolitical boundaries are
#                            desired on the maps.
#                          -File structure should be:
#                            CARTOPY_DIR/shapefiles/natural_earth/cultural/*.shp
#                          -More information regarding files needed to setup
#                            display maps in Cartopy, see SRW App Users' Guide
#                            https://ufs-srweather-app.readthedocs.io/en/ufs-v1.0.0/
#
#                       Plots are saved in the same directory that this script 
#                           is in as YYYYMMDDHH<variable>_<domain>_fHHH.png
#
#                       The variable domains in this script can be set to either
#                           'conus' for a CONUS map or manually adjusted in the 
#                           # Domain section
#
################################################################################
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
matplotlib.use('Agg')
import io
import matplotlib.pyplot as plt
import dateutil.relativedelta, dateutil.parser
from PIL import Image
import numpy as np
import sys
import argparse
import cartopy
import netCDF4 as nc

def ndate(cdate,hours):
   if not isinstance(cdate, str):
     if isinstance(cdate, int):
       cdate=str(cdate)
     else:
       sys.exit('NDATE: Error - input cdate must be string or integer.  Exit!')
   if not isinstance(hours, int):
     if isinstance(hours, str):
       hours=int(hours)
     else:
       sys.exit('NDATE: Error - input delta hour must be a string or integer.  Exit!')

   indate=cdate.strip()
   hh=indate[8:10]
   yyyy=indate[0:4]
   mm=indate[4:6]
   dd=indate[6:8]
   #set date/time field
   parseme=(yyyy+' '+mm+' '+dd+' '+hh)
   datetime_cdate=dateutil.parser.parse(parseme)
   valid=datetime_cdate+dateutil.relativedelta.relativedelta(hours=+hours)
   vyyyy=str(valid.year)
   vm=str(valid.month).zfill(2)
   vd=str(valid.day).zfill(2)
   vh=str(valid.hour).zfill(2)
   return vyyyy+vm+vd+vh
 
    
def clear_plotables(ax,keep_ax_lst,fig):
  #### - step to clear off old plottables but leave the map info - ####
  if len(keep_ax_lst) == 0 :
    print("clear_plotables WARNING keep_ax_lst has length 0. Clearing ALL plottables including map info!")
  cur_ax_children = ax.get_children()[:]
  if len(cur_ax_children) > 0:
    for a in cur_ax_children:
      if a not in keep_ax_lst:
       # if the artist isn't part of the initial set up, remove it
        a.remove()

def compress_and_save(filename):
  #### - compress and save the image - ####
  ram = io.BytesIO()
  plt.savefig(ram, format='png', bbox_inches='tight', dpi=150)
  ram.seek(0)
  im = Image.open(ram)
  im2 = im.convert('RGB')#.convert('P', palette=Image.ADAPTIVE)
  im2.save(filename, format='PNG')

def closest_index(arr, val):
    arr = abs(arr - val)
    return np.argmin(arr)

def cmap_cloud():
 # Create colormap for 2-m temperature
 # Modified version of the ncl_t2m colormap
    r=np.arange(128, 255)
    g=np.arange(128, 255)
    b=np.arange(128, 255)
    xsize=np.arange(np.size(r))
    r = r/255.
    g = g/255.
    b = b/255.
    red = []
    green = []
    blue = []
    for i in range(len(xsize)):
        xNorm=np.float(i)/(np.float(np.size(r))-1.0)
        red.append([xNorm,r[i],r[i]])
        green.append([xNorm,g[i],g[i]])
        blue.append([xNorm,b[i],b[i]])
    colorDict = {"red":red, "green":green, "blue":blue}
    cmap_cloud = matplotlib.colors.LinearSegmentedColormap('CMAP_CLOUD',colorDict)
    return cmap_cloud


# Start Script ---------------------------------------------------------------

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# Define required positional arguments
parser = argparse.ArgumentParser()
parser.add_argument("Cycle date/time in YYYYMMDDHH format")
parser.add_argument("Forecast hour in HHH")
parser.add_argument("Path to control directory")
parser.add_argument("Path to experiment directory")
parser.add_argument("Path to base directory of cartopy shapefiles")
args = parser.parse_args()

# Read date/time, forecast hour, and directory paths from command line
ymdh = str(sys.argv[1])
ymd = ymdh[0:8]
year = int(ymdh[0:4])
month = int(ymdh[4:6])
day = int(ymdh[6:8])
hour = int(ymdh[8:10])
cyc = str(hour).zfill(2)
print(year, month, day, hour)


EXPT_DIR = str(sys.argv[3]) + '/run'
CTRL_DIR = str(sys.argv[4]) + '/run'
CARTOPY_DIR = str(sys.argv[5])

fhour = str(sys.argv[2])
fhr = int(fhour)

itime = ymdh
vtime = ndate(itime,int(fhr))


datasfc_expt = nc.Dataset(EXPT_DIR + '/sfcf' + fhour + '.nc')
datasfc_ctrl = nc.Dataset(CTRL_DIR + '/sfcf' + fhour + '.nc')

# Get the lats and lons
lats = np.array(datasfc_ctrl['lat'][:])
lons = np.array(datasfc_ctrl['lon'][:])

lat = lats[:,0]
lon = lons[0,:]

cld_ctrl = np.squeeze(datasfc_ctrl['tcdc_aveclm'][:])
cld_expt = np.squeeze(datasfc_expt['tcdc_aveclm'][:])

# Domain
llcrnrlon = -120.5
llcrnrlat = 20
urcrnrlon = -55
urcrnrlat = 49.0
lat_0 = 35.4
lon_0 = -97.6
extent=[llcrnrlon-3,urcrnrlon-6,llcrnrlat-1,urcrnrlat+2]
      
# create figure and axes instances
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])

# Define where Cartopy Maps are located
cartopy.config['data_dir'] = CARTOPY_DIR

back_res='50m'
back_img='on'

# set up the map background with cartopy
myproj=ccrs.LambertConformal(central_longitude=lon_0, central_latitude=lat_0, false_easting=0.0,
                        false_northing=0.0, secant_latitudes=None, standard_parallels=None,
                        globe=None)

ax = plt.axes(projection=myproj)
ax.set_extent(extent)

fline_wd = 0.5  # line width
falpha = 0.3    # transparency

# natural_earth

lakes=cfeature.NaturalEarthFeature('physical','lakes',back_res,
                  edgecolor='blue',facecolor='none',
                  linewidth=fline_wd,alpha=falpha)
coastline=cfeature.NaturalEarthFeature('physical','coastline',
                  back_res,edgecolor='blue',facecolor='none',
                  linewidth=fline_wd,alpha=falpha)
states=cfeature.NaturalEarthFeature('cultural','admin_1_states_provinces',
                  back_res,edgecolor='black',facecolor='none',
                  linewidth=fline_wd,linestyle=':',alpha=falpha)
borders=cfeature.NaturalEarthFeature('cultural','admin_0_countries',
                  back_res,edgecolor='red',facecolor='none',
                  linewidth=fline_wd,alpha=falpha)

# All lat lons are earth relative, so setup the associated projection correct for that data
transform = ccrs.PlateCarree()

# high-resolution background images
if back_img=='on':
    img = plt.imread(CARTOPY_DIR+'/raster_files/NE1_50M_SR_W.tif')
    ax.imshow(img, origin='upper', transform=transform)

#  ax.add_feature(land)
ax.add_feature(lakes)
ax.add_feature(states)
ax.add_feature(borders)
ax.add_feature(coastline)

# Map/figure has been set up here, save axes instances for use again later
keep_ax_lst = ax.get_children()[:]

dom = 'CONUS'
#################################
  # Plot Cloud Cover Control
#################################
print(('Working on control cloud cover for '+dom))

# Clear off old plottables but keep all the map info
clear_plotables(ax,keep_ax_lst,fig)

units = '%'
clevs = np.linspace(10,100,10)
cm = cmap_cloud()
norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)

cs_1 = plt.pcolormesh(lon,lat,cld_ctrl,transform=transform,cmap=cm,norm=norm)
cs_1.cmap.set_under('white',alpha=0.)
cs_1.cmap.set_over('white')
cbar1 = plt.colorbar(cs_1,orientation='horizontal',pad=0.05,shrink=0.6,ticks=[10,20,30,40,50,60,70,80,90,100],extend='both')
cbar1.set_label('Cloud Cover (%)',fontsize=8)
cbar1.ax.tick_params(labelsize=8)
ax.text(.5,1.03,'UFS MRW Control Cloud Cover ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))

compress_and_save(ymdh + 'cloud_ctr_'+dom+'_f'+fhour+'.png')

#################################
  # Plot Cloud Cover Experiment
#################################
print(('Working on experiment cloud cover for '+dom))

# Clear off old plottables but keep all the map info
cbar1.remove()
clear_plotables(ax,keep_ax_lst,fig)

units = '%'
clevs = np.linspace(10,100,10)
cm = cmap_cloud()
norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)

cs_1 = plt.pcolormesh(lon,lat,cld_expt,transform=transform,cmap=cm,norm=norm)
cs_1.cmap.set_under('white',alpha=0.)
cs_1.cmap.set_over('white')
cbar1 = plt.colorbar(cs_1,orientation='horizontal',pad=0.05,shrink=0.6,ticks=[10,20,30,40,50,60,70,80,90,100],extend='both')
cbar1.set_label('Cloud Cover (%)',fontsize=8)
cbar1.ax.tick_params(labelsize=8)
ax.text(.5,1.03,'UFS MRW Experiment Cloud Cover ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))

compress_and_save(ymdh + 'cloud_exp_'+dom+'_f'+fhour+'.png')

#################################
  # Plot Cloud Cover Difference
#################################

diff = cld_expt-cld_ctrl

print(('Working on cloud cover difference for '+dom))

# Clear off old plottables but keep all the map info
cbar1.remove()
clear_plotables(ax,keep_ax_lst,fig)

units = '%'
clevs = np.linspace(-20,20,10)
cm = plt.cm.bwr
norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)

cs_1 = plt.pcolormesh(lon,lat,diff,transform=transform,cmap=cm,norm=norm)
cs_1.cmap.set_under('blue')
cs_1.cmap.set_over('red')
cbar1 = plt.colorbar(cs_1,orientation='horizontal',pad=0.05,shrink=0.6,ticks=[-20,-25,-10,-5,0,5,10,15,20],extend='both')
cbar1.set_label('Cloud Cover (%)',fontsize=8)
cbar1.ax.tick_params(labelsize=8)
ax.text(.5,1.03,'UFS MRW Cloud Cover Change (Experiment-Control) ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))

compress_and_save(ymdh + 'cloud_diff_'+dom+'_f'+fhour+'.png')
