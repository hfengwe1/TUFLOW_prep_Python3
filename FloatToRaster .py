# Name: FloatToRaster_Ex_02.py
# Description: Converts a file of binary floating-point values representing 
#    raster data to a raster dataset.

# Import system modules
import os, sys
import arcpy
import shutil

arcpy.env.overwriteOutput = False
def flt_to_tif(run_number,NAME):  # NAME: "location_channel type, e.g. T5_1
    end_time = input("End Time(2 hrs) -> ") or "2"
    mapOutputInterval = input("Map Output Interval(600 s) -> ") or "600"
    map_time_step_min = int(mapOutputInterval)/60

    for i in range(run_number):                 # for each run
        run = "{0:0=3d}".format(i+1)            # index of the run
## Create a "hydraulic performance folder in each run folder
        tif_path = os.path.abspath("output_folder/" + NAME + "_tuflow/results/"
                       + run +"/hydraulic_perofrmance")
        try:
            os.mkdir(tif_path)              
        except FileExistsError:
            print('Directory not created.')
            
#BSS: shear stress, d: depth, h: water level, n: Manning's n           
        for h in {'_BSS_', '_d_', '_h_', '_n_'}:    
## create the path variable of the .flt files

            flt_path = os.path.abspath("output_folder/" + NAME + "_tuflow/results/"
                                       + run +"/grids/")
## calculate the number of maps created each hour
            maps_no_hr = int(60/map_time_step_min)
            for j in range(int(end_time)):         # each hour
                hr = "{0:0=3d}".format(j)
                for k in range(maps_no_hr):        # within each hour
## create filename variable for the .flt and .tif
                    minute = "{0:0=2d}".format(int(k*map_time_step_min))                
                    flt_name = NAME + h + hr + '_' + minute + '.flt'
                    print(flt_name)
                    input_name = os.path.abspath(flt_path +"/" + flt_name)
                    tif_name = NAME + h + hr + '_' + minute + '.tif'
                    output_name = os.path.abspath(flt_path + "/" + tif_name)
# Execute FloatToRaster
                    try:
                        arcpy.FloatToRaster_conversion(input_name, output_name)
                    except arcpy.ExecuteError:
                        print(arcpy.GetMessages())
                      
#                    arcpy.FloatToRaster_conversion(input_name, output_name)
## create the filename variable for the last map and convert it to .tif
            flt_name = NAME + h + "{0:0=3d}".format(end_time) + '_' + '00' + '.flt'
            print(flt_name)
            input_name = os.path.abspath(flt_path +"/" + flt_name)
            tif_name = NAME + h + "{0:0=3d}".format(end_time) + '_' + '00' + '.tif'
            output_name = os.path.abspath(flt_path + "/" + tif_name)                
            arcpy.FloatToRaster_conversion(input_name, output_name)
## copy the last .tif to the "hydraulic performacne" folder
            h_p_name = os.path.abspath(tif_path +"/" + NAME + h + '.tif')
            shutil.copy2(output_name, h_p_name)
            
            
