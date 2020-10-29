"""
Map Window
Generates the Map class (a tkinter Canvas) and defines map-relevant functions
for plotting shapefiles(s) on a tkinter Canvas

Created on Tue Jan  7 15:11:58 2020
@author: jackreid
"""
import tkinter as tk
import pyproj
from pyproj import _datadir, datadir
import shapefile
import shapely.geometry
import PIL as pil
from PIL import ImageTk, Image, ImageDraw
from PIL import _tkinter_finder
from matplotlib import cm
import matplotlib.colors as colors
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.colorbar as colorbar
import matplotlib.pyplot as plt
from osgeo import gdal,ogr,osr
import array2gif
import numpy as np


class Map(tk.Canvas):
    
    
# =============================================================================
#     Initiating Map
# =============================================================================

    #Define Projections (Only Mercator used at this time)
    projections = {
        'mercator': pyproj.Proj("epsg:3857"),
        'spherical': pyproj.Proj('+proj=ortho +lon_0=28 +lat_0=47')
        }

    
    
    def __init__(self, root, shapefiles, **kwargs):
        """INITIALIZES THE MAP CLASS
    
        Args:
            root (tk parent): base window or frame to make the map canvas a part of
            shapefiles: list of pyshp shapefiles (not filenames!)
            kwargs:
                background_image: image to be used on background of map. Most common image types accepted. Default is none.
                color_range: list of shapefile field names to be used for scaling colors. Default is none.
    
        Returns:
            N/A
        """
        
        if 'window_dimensions' in kwargs:
            temp_dimensions = kwargs.pop('window_dimensions')
            # self.screenwidth = int(round(temp_dimensions[0]*0.54))
            # self.screenheight = int(round(temp_dimensions[1]*0.556))
            self.screenwidth = int(round(temp_dimensions[0]*0.5))
            self.screenheight = int(round(temp_dimensions[1]*0.52))
        else:
            self.screenwidth = int(round(temp_dimensions[0]*0.5))
            self.screenheight = int(round(temp_dimensions[1]*0.52))
        
        super().__init__(root, width=self.screenwidth, height=self.screenheight)
        
        self.bind('<ButtonPress-1>', self.print_coords)

        #Create display defaults
        self.proj = 'mercator'
        self.offset = (0, 0)
        
        #Create initial key bindings (???)
        self.bind('<ButtonPress-3>', lambda e: self.scan_mark(e.x, e.y))
        self.bind('<B3-Motion>', lambda e: self.scan_dragto(e.x, e.y, gain=1))
        
        #Set geographic coordinates and zoom level of map, initialize shapes
        if 'lat_lon_zoom' in kwargs:
            self.lat_lon_zoom = kwargs.pop('lat_lon_zoom')
            self.default_offset, self.default_ratio = self.set_canvas_location(self.lat_lon_zoom[0], self.lat_lon_zoom[1], self.lat_lon_zoom[2])
        else:
            self.default_offset, self.default_ratio = self.set_canvas_location(-43.5765151113451, -22.9969539088035, 0.03)

        #Save the shapefiles
        self.polyimages = []
        self.shapefiles = shapefiles

        #Add background image on map (if selected)
        if 'background_image' in kwargs:
            imagename = kwargs.pop('background_image')
            if imagename != []:
                self.draw_background(imagename)

        #Identify shapefile field name to be used for scaling colors
        if 'color_range' in kwargs:
            self.color_rangename = kwargs.pop('color_range')
        else:
            self.color_rangename = list()
            
        #Ensure that length of color_rangename matches the length of shapefiles
        if len(self.color_rangename) < len(self.shapefiles):
            dif = len(self.shapefiles) - len(self.color_rangename)
            for i in range(0, dif):
                self.color_rangename.append([])
              
        #Identify the longform name for the color metric to be used for the colorbar legend
        if 'color_title' in kwargs:
            self.color_title = kwargs.pop('color_title')
        else:
            self.color_title = []
            
        #Identify any specified visualization parameters
        if 'color_params' in kwargs:
            color_params = kwargs.pop('color_params')
            self.color_min = color_params[0]
            self.color_max = color_params[1]
            self.color_choice = color_params[2]
        else:
            self.color_min = []
            self.color_max = []
            self.color_choice = []
            
        #Identify if zeros should be plotted or considered invalid data
        if 'null_zeros' in kwargs:
            self.null_zeros = kwargs.pop('null_zeros')
        else:
            self.null_zeros = 0
        
        #Draw and Place Map
        self.draw_map(self.shapefiles, color_range=self.color_rangename)
        self.pack(fill='both', expand=1)
    
        
    def draw_background(self, imagename):
        """ADD A GEOTIFF IMAGE TO BACKGROUND OF MAP CANVAS
    
        Args:
            imagename: filepath of geotiff image to be added
    
        Returns:
            N/A
        """
        
        def GetExtent(gt,cols,rows):
            """GENERATE LIST OF CORNER COORDINATES FROM A GEOTRANSFORM
    
            Args:
                @type gt:   C{tuple/list}
                @param gt: geotransform
                @type cols:   C{int}
                @param cols: number of columns in the dataset
                @type rows:   C{int}
                @param rows: number of rows in the dataset
                
            Returns:
                @rtype:    C{[float,...,float]}
                @return:   coordinates of each corner, counter-clockwise from top right corner
            """
            
            ext=[]
            xarr=[0,cols]
            yarr=[0,rows]
        
            for px in xarr:
                for py in yarr:
                    x=gt[0]+(px*gt[1])+(py*gt[2])
                    y=gt[3]+(px*gt[4])+(py*gt[5])
                    ext.append([x,y])
                yarr.reverse()
            return ext

        def ReprojectCoords(coords,src_srs,tgt_srs):
            """REPROJECT A LIST OF X,Y COORDINATES
        
            Args:
                @type geom:     C{tuple/list}
                @param geom:    List of [[x,y],...[x,y]] coordinates
                @type src_srs:  C{osr.SpatialReference}
                @param src_srs: OSR SpatialReference object
                @type tgt_srs:  C{osr.SpatialReference}
                @param tgt_srs: OSR SpatialReference object
        
            Returns:
                @rtype:         C{tuple/list}
                @return:        List of transformed [[x,y],...[x,y]] coordinates
            """
           
            trans_coords=[]
            transform = osr.CoordinateTransformation( src_srs, tgt_srs)
            for x,y in coords:
                x,y,z = transform.TransformPoint(x,y)
                trans_coords.append([x,y])
            return trans_coords
            
        
        #Get Geographic Coordinates of the Corners of the Image
        ds=gdal.Open(imagename)
        gt=ds.GetGeoTransform()
        cols = ds.RasterXSize
        rows = ds.RasterYSize
        ext=GetExtent(gt,cols,rows)
        src_srs=osr.SpatialReference()
        src_srs.ImportFromWkt(ds.GetProjection())
        tgt_srs = src_srs.CloneGeogCS()
        geo_ext=ReprojectCoords(ext,src_srs,tgt_srs) 

        #Calculate Proper Dimensions of Image
        top_left = geo_ext[0]
        top_left_lat = top_left[1]
        top_left_lon = top_left[0]
        bottom_right = geo_ext[2]
        bottom_right_lat = bottom_right[1]
        bottom_right_lon = bottom_right[0]
        tlx, tly = self.to_canvas_coordinates(top_left_lon, top_left_lat)
        brx, bry = self.to_canvas_coordinates(bottom_right_lon, bottom_right_lat)
        new_width = brx - tlx
        new_height = bry - tly

        
        def display(image, display_min, display_max): # copied from Bi Rico
            """CONVERT A 16-BIT LUT TO AN 8-BIT LUT
        
            Args:
                image: 16-bit LUT in np-array form
                display_min: minimum cut-off value for image
                display_max: maximum cut-off value for image
        
            Returns:
                return: 8-bit LUT with cutoffs
            """
            image = np.array(image)
            image.clip(display_min, display_max, out=image)
            image -= display_min
            np.floor_divide(image, (display_max - display_min + 1) / 256,
                            out=image, casting='unsafe')
            return image.astype(np.uint8)

        def lut_display(image, display_min, display_max) :
            """CONVERT A 16-BIT IMAGE TO AN 8-BIT IMAGE USING A LUT
        
            Args:
                image: 16-bit image in np-array form
                display_min: minimum cut-off value for image
                display_max: maximum cut-off value for image
        
            Returns:
                return: 8-bit version of image, with cutoffs
            """
            lut = np.arange(2**16, dtype='uint16')
            lut = display(lut, display_min, display_max)
            return np.take(lut, image)


        #Load Image
        image_array = np.array(gdal.Open(imagename).ReadAsArray())
        
        #Determine if Image is Multiband or Single band
        shape_count = len(image_array.shape)
        
        #Process Image
        if shape_count > 2: #Image is multiband
            image_array = image_array[0:3] #take the BGR bands, omit the NIR band
            image_array = np.dstack((image_array[2],image_array[1],image_array[0])) #Convert BGR to RGB
            
            #Convert from uint16 to uint8 if needed
            display_min = image_array.min()
            display_max = image_array.max()
            if image_array.dtype == np.dtype('uint16'):
                image_array8 = np.array(lut_display(image_array, display_min, display_max))
                
            #make sure that the image is in uint8
            else:
                image_array8 = np.rint(image_array)
                image_array8 = np.nan_to_num(image_array8)
                image_array8 = image_array8.astype(np.uint8)
                
            loaded_image = pil.Image.fromarray(image_array8)
            
        else: #Image is single band
            display_min = image_array.min()
            display_max = image_array.max()
            
            #Convert from uint16 to uint8 if needed
            if image_array.dtype == np.dtype('uint16'):
                image_array8 = np.array(lut_display(image_array, display_min, display_max))
            
            #For single band images, can be left as float64 or uint8
            else:
                image_array8 = image_array
    
            loaded_image = pil.Image.fromarray(image_array8)

        #Resize Image
        loaded_image_resized = loaded_image.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        
        #Place Image in Correct Location
        self.background = ImageTk.PhotoImage(loaded_image_resized)
        self.create_image(tlx,tly,image=self.background,anchor="nw")
        
        
        
        
# =============================================================================
#     Location Functions
# =============================================================================

    def to_canvas_coordinates(self, longitude, latitude):
        """CONVERT FROM GEOGRAPHICAL COORDINATES TO CANVAS COORDINATES
    
        Args:
            longitude: decimal longitude
            latitude: decimal latitude
    
        Returns:
            canvas x coordinate, canvas y coordinate
        """
        
        px, py = self.projections[self.proj](longitude, latitude)
        return px*self.ratio + self.offset[0], -py*self.ratio + self.offset[1]


    def to_geographical_coordinates(self, x, y):
        """ CONVERT FROM CANVAS COORDINATES TO GEOGRAPHICAL COORDINATES
    
        Args:
            x: canvas x coordinate (such as from a click event)
            y: canvas y coordinate (such as from a click event)
    
        Returns:
            longitude: decimal longitude
            latitude: decimal latitude
        """
        
        px, py = (x - self.offset[0])/self.ratio, (self.offset[1] - y)/self.ratio
        return self.projections[self.proj](px, py, inverse=True)
    
    def print_coords(self, event):
        event.x, event.y = self.canvasx(event.x), self.canvasy(event.y)
        print('Geographic Coordinates')
        print(*self.to_geographical_coordinates(event.x, event.y))
        print('Canvas Coordinates')
        print([event.x, event.y])
        
    def set_canvas_location(self, longitude, latitude, zoomlevel):
        """SET MAP VISUAL LOCATION TO SPECIFIC COORDINATES AND ZOOM LEVEL
    
        Args:
            longitude: decimal longitude
            latitude: decimal latitude
            zoomlevel: Zoom level (higher numbers are more zoomed in. 0.03 is good start for sub-city level areas)
    
        Returns:
            N/A
        """
        #Scale canvas to specified zoom level
        self.ratio = zoomlevel
        
        #Move canvas center to specified coordinates and center in canvas
        locationx, locationy = self.to_canvas_coordinates(longitude, latitude)
        self.offset = (
            self.offset[0] - locationx+self.screenwidth/2,
            self.offset[1] - locationy+self.screenheight/2
            )
              

        
        return self.offset, self.ratio
  

# =============================================================================
#     Color Control Functions
# =============================================================================
    
    def colorrange(self, shp, valuename):
        """ IDENTIFY BOUNDS OF DATA TO BE USED FOR SCALING COLORS
    
        Args:
            shp: pyshp shapefile (not a filename!)
            valuename: name of field to be used for color scaling
    
        Returns:
            valuerange: range of values of specified field
            minim: minimum value of specified field
            smallpos: smallest positive value of specified field (if minim is positive, smallpos=minim)
        """
        
        sf = shp
        values = []
        strdict = []
        
        
        #Pull all the appropriate values from each record
        for record in sf.records():
            values.append(record[valuename])
        
        
        #If the values are strings, develop a quantified metric based on the alphabetized unique values
        if type(values[0]) == str:
            values.sort()
            sortedvalues = values
            strdict = {ni: indi for indi, ni in enumerate(set(sortedvalues))}
            values = [strdict[ni] for ni in sortedvalues]
            
        
        #Calculate the range of values, including the smallest positive value
        minim = min(values)
        maxim = max(values)
        valuerange = maxim - minim
        if minim <= 0 and strdict == []:
            values =[]
            for record in sf.records():
                if record[valuename]>0:
                    values.append(record[valuename])
            if values == []:
                smallpos = []
            else:
                smallpos = min(values)
        else:
            smallpos = minim
            
            
        return valuerange, minim, smallpos, strdict
            
            
    def rgb2hex(self,color):
        """CONVERTS A LIST OR TUPLE OF RGB COORDINATES TO A HEX STRING
    
        Args:
            color (list|tuple): the list or tuple of integers (e.g. (127, 127, 127))
    
        Returns:
            str:  the rgb string
        """
        
        return f"#{''.join(f'{hex(c)[2:].upper():0>2}' for c in color)}"
            

# =============================================================================
#    Drawing Functions
# =============================================================================
   
    def draw_map(self, shapefiles, **kwargs):
        """DRAWS THE MAP USED THE SPECIFIED SHAPEFILE. EACH SHAPE IS AN IMAGE.
        
        Args:
            shapefile: list of shapefiles (currently only uses the first entry)
            kwargs:
                color_range: list of field names to be used fro color scaling (currently only uses the first entry)
    
        Returns:
            N/A            
        """
        
        #Clear canvas, fill with water, read in shapefile
        self.delete('land', 'water')
        self.draw_water()
        sf = shapefiles[0]


        #Create colormap and norm for us in color scaling
        if 'color_range' in kwargs:
            color_range = kwargs.pop('color_range')
            color_name = color_range[0]
        if color_name != []:
            valuerange, minim, smallpos, strdict = self.colorrange(sf, color_name)
            if self.color_min:
                minim = self.color_min
            if self.color_max:
                maxim = self.color_max
            else:
                maxim = minim + valuerange
            
            if self.color_choice:
                colormap = cm.get_cmap(self.color_choice) #if colors were pre-specified
            elif minim < 0 and smallpos == []: #if data is entirely negative
                colormap = cm.get_cmap('autumn', 48)
            elif minim < 0 and smallpos != []: #if data is partially negative and partially positive
                colormap = cm.get_cmap('RdYlGn', 48)
            else:  #if data is entirely positive
                colormap = cm.get_cmap('YlOrRd', 48)
                
            norm = colors.Normalize(minim, maxim)
        
        
        #Draw each shape in shapefile
        for shaperec in sf.iterShapeRecords():
            
            
            # convert shapefile geometries into shapely geometries
            # to extract the polygons of a multipolygon
            polygon = shapely.geometry.shape(shaperec.shape)
            if polygon.geom_type == 'Polygon':
                polygon = [polygon]
            for land in polygon:
                coordinates = sum((self.to_canvas_coordinates(*c) for c in land.exterior.coords), ())
                
                
                #Set appropriate color
                if color_name != []:
                    value = shaperec.record[color_name]
                    
                    if strdict != []:
                        value = strdict[value]
                    normvalue = norm(value)
                    fill1 = colormap(normvalue)[0:3]
                    fill = [int(x*255) for x in fill1]
                    alpha = 0.5
                    if self.null_zeros == 1:
                        if value == 0:
                            fill = self.winfo_rgb('black')
                            alpha = 0.3                         
                else:
                    fill = self.winfo_rgb('green')
                    alpha = 0
                    
                
                #Add the image to the list of images
                newimage = self.draw_polygon(coordinates, fill=fill, alpha=alpha)
                self.polyimages.append(newimage)
                
                
        #Add Colorbar to map in bottom left corner
        if color_name != []:    
            plt.ioff()
            fig = plt.figure(figsize=(2, 8))
            ax1 = fig.add_axes([0.05, 0.01, 0.5, 0.95])
            canvas = FigureCanvas(fig)
            cb1 = colorbar.ColorbarBase(ax1, cmap=colormap,
                                    norm=norm,
                                    orientation='vertical')
            if self.color_title != []:
                cb1.set_label(self.color_title)
            else:
                cb1.set_label(color_name)
            
            canvas.draw() 
            s, (width, height) = canvas.print_to_buffer()
            im = Image.frombytes("RGBA", (width, height), s)
            im = im.resize((2*65, 8*65), Image.ANTIALIAS)
            self.colorimage = ImageTk.PhotoImage(im)
            self.create_image(0,self.screenheight,image=self.colorimage,anchor='sw')
            plt.close(fig)
            del(canvas)
            del(s)
                
            
    def draw_polygon(self, coordinates, **kwargs):       
        """DRAWS A POLYGON AS AN IMAGE TO ALLOW FOR ALPHA-LEVELS
    
        Args:
            coordinates: list of coordinates defining vertices of the polygon
            kwargs:
                fill: RGB vector to be used for fill color. Default is green.
                alpha: 0-to-1 value for level of transparency (0 is invisible, 1 is opaque). Only affects fill, not outline. Default is 1
                outline: string description of color (e.g. 'green'). Default is red.
    
        Returns:
            newimage: A Tk image of the specified polygon, tagged as land
        """
        
        
        #Pull inputs and, in their absence, select the defaults
        if 'fill' in kwargs:
            fill = tuple(kwargs.pop('fill'))
        else:
             fill = 'green'
             fill = self.winfo_rgb(fill)
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
        else:
            alpha = 1
            alpha = int(alpha*255)
        if 'outline' in kwargs:
            outline = kwargs.pop('outline')
            outline = self.winfo_rgb(outline)
        else:
            outline = 'red'
            outline = self.winfo_rgb(outline)
        fill = fill + (alpha,)  
        
        
        #Creat the new shape
        poly = Image.new('RGBA', (1300,800))
        pdraw = ImageDraw.Draw(poly)
        pdraw.polygon(coordinates,
                  fill,outline=outline)
        newimage = (ImageTk.PhotoImage(poly))
        self.create_image(1,1, image=newimage, anchor='nw', tags=('land',))
        return newimage
    

    def addshapes(self, sf, **kwargs):
        """ADD ADDITIONAL SHAPES TO MAP, AS TK POLYGONS (NOT IMAGES)
    
        Args:
            sf: pyshp shapefile (not a filename!)
            kwargs:
                outline: string description of color (e.g. 'black'). Default is black
                color_range: name of field to be used for color scaling. Default is a constant orange color.
    
        Returns:
            N/A
        """
        
        
        #Select the outline color
        if 'outline' in kwargs:
            outline = kwargs.pop('outline')
        else:
            outline = 'black'
            
            
        #Define colormap
        if 'color_range' in kwargs:
            color_name = kwargs.pop('color_range')
        if color_name != []:
            valuerange, minim, smallpos, strdict = self.colorrange(sf, color_name)
            colormap = cm.get_cmap('RdYlGn', 48)
            norm = colors.Normalize(minim, minim+valuerange)
        
        
        #Select the longform title for use on the colorbar
        if 'color_title' in kwargs:
            colortitle = kwargs.pop('color_title')
        else:
            colortitle = []
        
        
        #Draw each shape as canvas polygon
        for shaperec in sf.iterShapeRecords():
            
            
            # convert shapefile geometries into shapely geometries
            # to extract the polygons of a multipolygon
            polygon = shaperec.shape
            polygon = shapely.geometry.shape(polygon)
            
            
            #Assign color to each shape based on colornorm
            if color_name != []:
                value = shaperec.record[color_name]
                if strdict != []:
                    value = strdict[value]
                normvalue = norm(value)
                fill1 = colormap(normvalue)[0:3]
                fill = [int(x*255) for x in fill1]
                fill = self.rgb2hex(fill)
            else:
                fill = 'orange'
                
                
            #Create the shape
            if polygon.geom_type == 'Polygon':
                polygon = [polygon]
            for land in polygon:
                self.create_polygon(
                    sum((self.to_canvas_coordinates(*c) for c in land.exterior.coords), ()),
                    fill=fill,
                    outline=outline,
                    tags=('land',)
                    )
                
                
        #Add Colorbar to map in bottom left corner
        if color_name != []:    
            plt.ioff()
            fig = plt.figure(figsize=(2, 8))
            ax1 = fig.add_axes([0.05, 0.01, 0.5, 0.95])
            canvas = FigureCanvas(fig)
            cb1 = colorbar.ColorbarBase(ax1, cmap=colormap,
                                    norm=norm,
                                    orientation='vertical')
            
            if colortitle != []:
                cb1.set_label(colortitle)
            else:
                cb1.set_label(color_name)
                
            canvas.draw() 
            s, (width, height) = canvas.print_to_buffer()
            im = Image.frombytes("RGBA", (width, height), s)
            im = im.resize((2*65, 8*65), Image.ANTIALIAS)
            self.colorimage2 = ImageTk.PhotoImage(im)
            self.create_image(2*65,self.screenheight,image=self.colorimage2,anchor='sw')
            plt.close(fig)
            del(canvas)
            del(s)
                

    def draw_water(self):
        """FILLS CANVAS WITH BLUE WHERE SHAPES DO NOT COVER
    
        Args:
            N/A
    
        Returns:
            N/A
        """
        
        x0, y0 = self.to_canvas_coordinates(-180, 84)
        x1, y1 = self.to_canvas_coordinates(180, -84)
        self.water_id = self.create_rectangle(
            x1, y1, x0, y0,
            outline='black',
            fill = '',
            tags=('water',)
        )
            
       
# =============================================================================
#    Main Script
# =============================================================================

if str.__eq__(__name__, '__main__'):
    root_window = tk.Tk()
    root_window.title('MapWindow')
    sf = shapefile.Reader('/home/jackreid/Documents/School/Research/Space Enabled/Code/Decisions/Data/Rio de Janeiro/Shapefiles/geographic_data.shp')



    py_giss = Map(root_window, [sf],
                  lat_lon_zoom= [-43.162396, -22.916935, 0.01],
                  background_image = './Data/Rio de Janeiro/test.tif')
    root_window.mainloop()
