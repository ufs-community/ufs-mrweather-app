#!/usr/bin/env python3
################################################################################
####  Python Script Documentation Block
#
# Script name:       	plot_mrw.py
# Script description:  	Generates plots of several output variables from UFS 
#           MRW App Graduate Student Test
#
# Authors:  Sam Ephraim		Org: EPIC Lapenta Intern		Date: 2021-07-06
#           Based off of work from Ben Blake and David Wright
#
# Instructions:		Make sure all the necessary modules can be imported.
#                       Five command line arguments are needed:
#                       1. Cycle date/time in YYYYMMDDHH format
#                       2. Start forecast hour in HHH format
#                       3. End forecast hour in HHH format
#                       4. CARTOPY_DIR:  Base directory of cartopy shapefiles
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
#
################################################################################

#-------------Import modules --------------------------#
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
matplotlib.use('Agg')
import io
import matplotlib.pyplot as plt
import dateutil.relativedelta, dateutil.parser
from PIL import Image
import numpy as np
import time,sys
import argparse
import cartopy
import netCDF4 as nc

# Create the frames
def make_gif(product, imgs):
    frames = []
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(product + '.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=300, loop=0)


def cmap_q2m():
 # Create colormap for 2-m dew point temperature
    r=np.array([255,179,96,128,0, 0,  51, 0,  0,  0,  133,51, 70, 0,  128,128,180])
    g=np.array([255,179,96,128,92,128,153,155,155,255,162,102,70, 0,  0,  0,  0])
    b=np.array([255,179,96,0,  0, 0,  102,155,255,255,255,255,255,128,255,128,128])
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
    cmap_q2m_coltbl = matplotlib.colors.LinearSegmentedColormap('CMAP_Q2M_COLTBL',colorDict)
    cmap_q2m_coltbl.set_over(color='deeppink')
    return cmap_q2m_coltbl


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
    
    
def rotate_wind(true_lat,lov_lon,earth_lons,uin,vin,proj,inverse=False):
  #  Rotate winds from LCC relative to earth relative (or vice-versa if inverse==true)
  #   This routine is vectorized and *should* work on any size 2D vg and ug arrays.
  #   Program will quit if dimensions are too large.
  #
  # Input args:
  #  true_lat = True latitidue for LCC projection (single value in degrees)
  #  lov_lon  = The LOV value from grib (e.g. - -95.0) (single value in degrees)
  #              Grib doc says: "Lov = orientation of the grid; i.e. the east longitude value of
  #                              the meridian which is parallel to the Y-axis (or columns of the grid)
  #                              along which latitude increases as the Y-coordinate increases (the
  #                              orientation longitude may or may not appear on a particular grid).
  #
  #  earth_lons = Earth relative longitudes (can be an array, in degrees)
  #  uin, vin     = Input winds to rotate
  #
  # Returns:
  #  uout, vout = Output, rotated winds
  #-----------------------------------------------------------------------------------------------------

  # Get size and length of input u winds, if not 2d, raise an error
  q=np.shape(uin)
  ndims=len(q)
  if ndims > 2:
    # Raise error and quit!
    raise SystemExit("Input winds for rotation have greater than 2 dimensions!")
  if lov_lon > 0.: lov_lon=lov_lon-360.
  dtr=np.pi/180.0             # Degrees to radians

  if not isinstance(inverse, bool):
    raise TypeError("**kwarg inverse must be of type bool.")

  # Compute rotation constant which is also
  # known as the Lambert cone constant.  In the case
  # of a polar stereographic projection, this is one.
  # See the following pdf for excellent documentation
  # http://www.dtcenter.org/met/users/docs/write_ups/velocity.pdf
  if proj.lower()=='lcc':
    rotcon_p=np.sin(true_lat*dtr)
  elif proj.lower() in ['stere','spstere', 'npstere']:
    rotcon_p=1.0
  else:
    raise SystemExit("Unsupported map projection: "+proj.lower()+" for wind rotation.")

  angles = rotcon_p*(earth_lons-lov_lon)*dtr
  sinx2 = np.sin(angles)
  cosx2 = np.cos(angles)

  # Steps below are elementwise products, not matrix mutliplies
  if inverse==False:
    # Return the earth relative winds
    uout = cosx2*uin+sinx2*vin
    vout =-sinx2*uin+cosx2*vin
  elif inverse==True:
    # Return the grid relative winds
    uout = cosx2*uin-sinx2*vin
    vout = sinx2*uin+cosx2*vin

  return uout,vout

def binary_search(arr, low, high, x):
    # Check base case
    # print(low)
    # print(high)
    # print(x)
    if abs(high-low) < 2:
        return high
    #print(arr)
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return low


def closest_convert_index(lats, lons, tile_coors):
    index_map = np.empty((np.size(lons),np.size(lats)))
    tile_lat, tile_lon, tile_ind = zip(*tile_coors)
    tile_lat_list = list(tile_lat)
    
    for lonind, x in enumerate(lons):
        for latind, y in enumerate(lats):
            min_dist = 10000000000000
            min_ind = -1
            print(lonind,latind)
            
            
            
            low_ind = binary_search(tile_lat_list,0,len(tile_lat)-1,y-0.5)
            high_ind = binary_search(tile_lat_list,low_ind,len(tile_lat)-1,y+0.5)
            
            prospects = tile_coors[low_ind:high_ind]
            
            
            
            for point in prospects:
                
                dist = (point[0]-y)**2 + (point[1] - x)**2
                if dist < min_dist:
                    min_dist = dist
                    min_ind = point[2]
            
            index_map[lonind,latind] = min_ind
    return index_map
            
   
def fill_data(data, frame):
    output = np.zeros(np.asarray(frame.shape))
    for i, row in enumerate(frame):
        for j, ind in enumerate(row):
            print(i)
            print(ind)
            output[i,j] = data[int(ind)]
        
    return output

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
parser.add_argument("Forecast start hour in HHH")
parser.add_argument("Forecast end hour in HHH")
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



CARTOPY_DIR = str(sys.argv[4])

fhour = str(sys.argv[2])
fhr = int(fhour)

end_hour = int(str(sys.argv[3]))

itime = ymdh
vtime = ndate(itime,int(fhr))



datasfc = nc.Dataset('sfcf000.nc')
datatile1 = nc.Dataset('atmos_4xdaily.tile1.nc')
datatile2 = nc.Dataset('atmos_4xdaily.tile2.nc')
datatile3 = nc.Dataset('atmos_4xdaily.tile3.nc')
datatile4 = nc.Dataset('atmos_4xdaily.tile4.nc')
datatile5 = nc.Dataset('atmos_4xdaily.tile5.nc')
datatile6 = nc.Dataset('atmos_4xdaily.tile6.nc')



    


# Get the lats and lons
lats = np.array(datasfc['lat'][:])
lons = np.array(datasfc['lon'][:])



coor_tile1 = nc.Dataset('grid_spec.tile1.nc')

lats_tile1 = np.array(coor_tile1['grid_latt'][:])
lons_tile1 = np.array(coor_tile1['grid_lont'][:])

coor_tile2 = nc.Dataset('grid_spec.tile2.nc')

lats_tile2 = np.array(coor_tile2['grid_latt'][:])
lons_tile2 = np.array(coor_tile2['grid_lont'][:])

coor_tile3 = nc.Dataset('grid_spec.tile3.nc')

lats_tile3 = np.array(coor_tile3['grid_latt'][:])
lons_tile3 = np.array(coor_tile3['grid_lont'][:])

coor_tile4 = nc.Dataset('grid_spec.tile4.nc')

lats_tile4 = np.array(coor_tile4['grid_latt'][:])
lons_tile4 = np.array(coor_tile4['grid_lont'][:])

coor_tile5 = nc.Dataset('grid_spec.tile5.nc')

lats_tile5 = np.array(coor_tile5['grid_latt'][:])
lons_tile5 = np.array(coor_tile5['grid_lont'][:])

coor_tile6 = nc.Dataset('grid_spec.tile6.nc')

lats_tile6 = np.array(coor_tile6['grid_latt'][:])
lons_tile6 = np.array(coor_tile6['grid_lont'][:])

lat_tiles = np.concatenate((np.ravel(lats_tile1), np.ravel(lats_tile2),
                            np.ravel(lats_tile3), np.ravel(lats_tile4),
                            np.ravel(lats_tile5), np.ravel(lats_tile6)))

lon_tiles = np.concatenate((np.ravel(lons_tile1), np.ravel(lons_tile2),
                            np.ravel(lons_tile3), np.ravel(lons_tile4),
                            np.ravel(lons_tile5), np.ravel(lons_tile6)))

ind = np.arange(0,np.size(lat_tiles))
coor_tiles = list(zip(lat_tiles, lon_tiles, ind))
coor_tiles.sort()


lat = lats[:,0]
lon = lons[0,:]

#convert_map = closest_convert_index(lat, lon, coor_tiles)
#convert_map = np.rot90(convert_map, k=1, axes=(0,1))
#convert_map = np.flipud(convert_map)
#convert_map = mp.fliplr(convert_map)



domains=['conus']    # Other option is 'regional'

temp_img = []
wnd_img = []
qpf_img = []
cld_img = []
###################################################
# Read in all variables and calculate differences #
###################################################
while fhr <= end_hour:
    if fhr < 10:
        hrtxt = '00' + str(fhr)
    elif fhr < 100:
        hrtxt = '0' + str(fhr)
    else:
        hrtxt = str(fhr)
    t1a = time.perf_counter()
    fhour = hrtxt
    
    #dataatm = nc.Dataset('atmf'+hrtxt+'.nc')
    datasfc = nc.Dataset('sfcf'+hrtxt+'.nc')
    # Sea level pressure
    # time_ind = np.floor(fhr/6) #11
    
    # slp_tile1 = np.array(datatile1['slp'][time_ind,:,:])
    # slp_tile2 = np.array(datatile2['slp'][time_ind,:,:])
    # slp_tile3 = np.array(datatile3['slp'][time_ind,:,:])
    # slp_tile4 = np.array(datatile4['slp'][time_ind,:,:])
    # slp_tile5 = np.array(datatile5['slp'][time_ind,:,:])
    # slp_tile6 = np.array(datatile6['slp'][time_ind,:,:])
    
    # slp_all_tiles =  np.concatenate((np.ravel(slp_tile1), np.ravel(slp_tile2),
    #                             np.ravel(slp_tile3), np.ravel(slp_tile4),
    #                             np.ravel(slp_tile5), np.ravel(slp_tile6)))
    
    # slp = fill_data(slp_all_tiles, convert_map)
    
    # slpsmooth = ndimage.filters.gaussian_filter(slp, 0.5)#13.78)
    
    
    
    # 2-m temperature
    tmp2m = np.squeeze(datasfc['tmp2m'][:])
    tmp2m = (tmp2m - 273.15)*1.8 + 32.0
    

    
    # 10-m wind speed
    uwind = np.squeeze(datasfc['ugrd10m'][:]) * 1.94384
    vwind = np.squeeze(datasfc['vgrd10m'][:]) * 1.94384
    # Rotate winds from grid relative to Earth relative
    uwind, vwind = rotate_wind(lat[0],lon[0],lon,uwind,vwind,'lcc',inverse=False)
    wspd10m = np.sqrt(uwind**2 + vwind**2)
    

   # QPF
    qpf_tot = np.zeros((192, 384))
    qpf = np.squeeze(datasfc['prate_ave'][:]) *60*60/25.4
    if fhr <=12:
        qpf_tot += qpf
    else: 
        qpf_tot += 3*qpf
        
        
    cld = np.squeeze(datasfc['tcdc_aveclm'][:])
  
    t2a = time.perf_counter()
    t3a = round(t2a-t1a, 3)
    print(("%.3f seconds to read all messages") % t3a)
    
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
    
    #   # set up the map background with cartopy
    myproj=ccrs.LambertConformal(central_longitude=lon_0, central_latitude=lat_0, false_easting=0.0,
                            false_northing=0.0, secant_latitudes=None, standard_parallels=None,
                            globe=None)
    
    ax = plt.axes(projection=myproj)
    ax.set_extent(extent)
    
    fline_wd = 0.5  # line width
    falpha = 0.3    # transparency
    
      # natural_earth
    #  land=cfeature.NaturalEarthFeature('physical','land',back_res,
    #                    edgecolor='face',facecolor=cfeature.COLORS['land'],
    #                    alpha=falpha)
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
    
    #   # All lat lons are earth relative, so setup the associated projection correct for that data
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
    
    
    ################################
      # Plot SLP
    ################################
    # t1 = time.perf_counter()
    dom = 'CONUS'
    # # print(('Working on slp for '+dom))
    
    # units = 'mb'
    # clevs = [976,980,984,988,992,996,1000,1004,1008,1012,1016,1020,1024,1028,1032,1036,1040,1044,1048,1052]
    # clevsdif = [-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12]
    
    # cm = plt.cm.Spectral_r
    # norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)
    
    
    
    # cs1_a = plt.pcolormesh(lon,lat,slp,transform=transform,cmap=cm,norm=norm)
    # cbar1 = plt.colorbar(cs1_a,orientation='horizontal',pad=0.05,shrink=0.6,extend='both')
    # cbar1.set_label(units,fontsize=8)
    # cbar1.ax.tick_params(labelsize=8)
    # cs1_b = plt.contour(lon,lat,slpsmooth,np.arange(940,1060,4),colors='black',linewidths=1.25,transform=transform)
    # plt.clabel(cs1_b,np.arange(940,1060,4),inline=1,fmt='%d',fontsize=8)
    # ax.text(.5,1.03,'UFS MRW SLP ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))
    
    # #compress_and_save(EXPT_DIR+'/'+ymdh+'/postprd/slp_'+dom+'_f'+fhour+'.png')
    # compress_and_save(EXPT_DIR+'/test.png')
    # t2 = time.perf_counter()
    # t3 = round(t2-t1, 3)
    # print(('%.3f seconds to plot slp for: '+dom) % t3)
    
    
    #################################
      # Plot 2-m T
    #################################
    t1 = time.perf_counter()
    print(('Working on t2m for '+dom))
    
    # Clear off old plottables but keep all the map info
    # cbar1.remove()
    # clear_plotables(ax,keep_ax_lst,fig)
    
    units = '\xb0''F'
    clevs = np.linspace(-16,134,51)
    cm = plt.cm.Spectral_r #cmap_t2m()
    norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)
    
    cs_1 = plt.pcolormesh(lon,lat,tmp2m,transform=transform,cmap=cm,norm=norm)
    cs_1.cmap.set_under('white')
    cs_1.cmap.set_over('white')
    cbar1 = plt.colorbar(cs_1,orientation='horizontal',pad=0.05,shrink=0.6,ticks=[-16,-4,8,20,32,44,56,68,80,92,104,116,128],extend='both')
    cbar1.set_label(units,fontsize=8)
    cbar1.ax.tick_params(labelsize=8)
    fname = ymdh + 'tmp2m_'+dom+'_f'+fhour+'.png'
    ax.text(.5,1.03,'UFS MRW 2-m Temperature ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))
    
    compress_and_save(fname)
    t2 = time.perf_counter()
    t3 = round(t2-t1, 3)
    print(('%.3f seconds to plot 2mt for: '+dom) % t3)
    
    if fhr <= 12:
        temp_img.append(fname)
    else:
        temp_img.append(fname)
        temp_img.append(fname)
        temp_img.append(fname)
    
    #################################
      # Plot 10-m WSPD
    #################################
    t1 = time.perf_counter()
    print(('Working on 10mwspd for '+dom))
      
    # Clear off old plottables but keep all the map info
    cbar1.remove()
    clear_plotables(ax,keep_ax_lst,fig)
      
    units = 'kts'
  
    skip = int(np.floor(len(lon)/150))
    print('skipping every '+str(skip)+' grid points to plot')
    barblength = 5
      
    clevs = [5,10,15,20,25,30,35,40,45,50,55,60]
    colorlist = ['turquoise','dodgerblue','blue','#FFF68F','#E3CF57','peru','brown','crimson','red','fuchsia','DarkViolet']
    cm = matplotlib.colors.ListedColormap(colorlist)
    norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)
      
    cs_1 = plt.pcolormesh(lon,lat,wspd10m,transform=transform,cmap=cm,vmin=5,norm=norm)
    cs_1.cmap.set_under('white',alpha=0.)
    cs_1.cmap.set_over('black')
    cbar1 = plt.colorbar(cs_1,orientation='horizontal',pad=0.05,shrink=0.6,ticks=clevs,extend='max')
    cbar1.set_label(units,fontsize=8)
    cbar1.ax.tick_params(labelsize=8)
    

    fname = ymdh + '10mwind_'+dom+'_f'+fhour+'.png'
    
    plt.barbs(lons[::skip,::skip],lats[::skip,::skip],uwind[::skip,::skip],vwind[::skip,::skip],length=barblength,linewidth=0.5,color='black',transform=transform)
    ax.text(.5,1.03,'UFS MRW 10-m Winds ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))
      
    
    compress_and_save(fname)
    t2 = time.perf_counter()
    t3 = round(t2-t1, 3)
    print(('%.3f seconds to plot 10mwspd for: '+dom) % t3)
    
    if fhr <= 12:
        wnd_img.append(fname)
    else:
        wnd_img.append(fname)
        wnd_img.append(fname)
        wnd_img.append(fname)

    
    #################################
      # Plot Hourly QPF
    #################################
    if (fhr > 0):		# Do not make total QPF plot for forecast hour 0
      t1 = time.perf_counter()
      print(('Working on total qpf for '+dom))
    
    # Clear off old plottables but keep all the map info
      cbar1.remove()
      clear_plotables(ax,keep_ax_lst,fig)
    
      units = 'in'
      clevs = [0.01,0.1,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.5,3,4,5,7,10,15,20]
      clevsdif = [-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3]
      colorlist = ['chartreuse','limegreen','green','blue','dodgerblue','deepskyblue','cyan','mediumpurple','mediumorchid','darkmagenta','darkred','crimson','orangered','darkorange','goldenrod','gold','yellow']
      cm = matplotlib.colors.ListedColormap(colorlist)
      norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)
    
      cs_1 = plt.pcolormesh(lon,lat,qpf,transform=transform,cmap=cm,vmin=0.01,norm=norm)
      cs_1.cmap.set_under('white',alpha=0.)
      cs_1.cmap.set_over('pink')
      cbar1 = plt.colorbar(cs_1,orientation='horizontal',pad=0.05,shrink=0.6,ticks=clevs,extend='max')
      cbar1.set_label(units,fontsize=8)
      cbar1.ax.set_xticklabels(clevs)
      cbar1.ax.tick_params(labelsize=8)
      
      fname = ymdh + 'qpfhr_'+dom+'_f'+fhour+'.png'
      ax.text(.5,1.03,'UFS MRW Hourly Accumulated Precipitation ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))
    
      compress_and_save(fname)
      t2 = time.perf_counter()
      t3 = round(t2-t1, 3)
      print(('%.3f seconds to plot total qpf for: '+dom) % t3)
      
      if fhr <= 12:
         qpf_img.append(fname)
      else:
         qpf_img.append(fname)
         qpf_img.append(fname)
         qpf_img.append(fname)
      
      #################################
      # Plot Clouds
      #################################
      
      print(('Working on cloud cover for '+dom))

      # Clear off old plottables but keep all the map info
      cbar1.remove()
      clear_plotables(ax,keep_ax_lst,fig)
    
      units = '%'
      clevs = np.linspace(10,100,10)
      cm = cmap_cloud()
      norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)
    
      cs_1 = plt.pcolormesh(lon,lat,cld,transform=transform,cmap=cm,norm=norm)
      cs_1.cmap.set_under('white',alpha=0.)
      cs_1.cmap.set_over('white')
      cbar1 = plt.colorbar(cs_1,orientation='horizontal',pad=0.05,shrink=0.6,ticks=[10,20,30,40,50,60,70,80,90,100],extend='both')
      cbar1.set_label('Cloud Cover (%)',fontsize=8)
      cbar1.ax.tick_params(labelsize=8)
      fname = ymdh + 'cloud_'+dom+'_f'+fhour+'.png'
      ax.text(.5,1.03,'UFS MRW Cloud Cover ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))
    
      compress_and_save(fname)
      
      if fhr <= 12:
         cld_img.append(fname)
      else:
         cld_img.append(fname)
         cld_img.append(fname)
         cld_img.append(fname)
      
    #################################
    # Plot Total QPF
    #################################
    if (fhr > 0):		# Do not make total QPF plot for forecast hour 0
        t1 = time.perf_counter()
        print(('Working on total qpf for '+dom))
      
        # Clear off old plottables but keep all the map info
        cbar1.remove()
        clear_plotables(ax,keep_ax_lst,fig)
      
        units = 'in'
        clevs = [0.01,0.1,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.5,3,4,5,7,10,15,20]
        clevsdif = [-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3]
        colorlist = ['chartreuse','limegreen','green','blue','dodgerblue','deepskyblue','cyan','mediumpurple','mediumorchid','darkmagenta','darkred','crimson','orangered','darkorange','goldenrod','gold','yellow']
        cm = matplotlib.colors.ListedColormap(colorlist)
        norm = matplotlib.colors.BoundaryNorm(clevs, cm.N)
      
        cs_1 = plt.pcolormesh(lon,lat,qpf_tot,transform=transform,cmap=cm,vmin=0.01,norm=norm)
        cs_1.cmap.set_under('white',alpha=0.)
        cs_1.cmap.set_over('pink')
        cbar1 = plt.colorbar(cs_1,orientation='horizontal',pad=0.05,shrink=0.6,ticks=clevs,extend='max')
        cbar1.set_label(units,fontsize=8)
        cbar1.ax.set_xticklabels(clevs)
        cbar1.ax.tick_params(labelsize=8)
        ax.text(.5,1.03,'UFS MRW '+fhour+'-hr Accumulated Precipitation ('+units+') \n initialized: '+itime+' valid: '+vtime + ' (f'+fhour+')',horizontalalignment='center',fontsize=8,transform=ax.transAxes,bbox=dict(facecolor='white',alpha=0.85,boxstyle='square,pad=0.2'))
      
        compress_and_save('testqpf.png')
        t2 = time.perf_counter()
        t3 = round(t2-t1, 3)
        print(('%.3f seconds to plot total qpf for: '+dom) % t3)
      
    if fhr < 12:
        fhr += 1
    else:
        fhr += 3
    
    
make_gif('tmp', temp_img)
make_gif('wnd', wnd_img)
make_gif('cld', cld_img)
make_gif('qpf', qpf_img)


