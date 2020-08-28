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


class Map(tk.Canvas):
    
    
# =============================================================================
#     Initiating Map
# =============================================================================

    #Define Projections (Only Mercator used at this time)
    projections = {
        'mercator': pyproj.Proj(init="epsg:3857"),
        'spherical': pyproj.Proj('+proj=ortho +lon_0=28 +lat_0=47')
        }

    screenwidth, screenheight = 1000, 600
    
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
        
        super().__init__(root, width=self.screenwidth, height=self.screenheight)
        # super().__init__(root, width=root.winfo_width(), height=root.winfo_height())

        #Create display defaults
        self.proj = 'mercator'
        self.ratio = 1
        self.offset = (0, 0)
        
        
        #Create initial key bindings (???)
        self.bind('<ButtonPress-3>', lambda e: self.scan_mark(e.x, e.y))
        self.bind('<B3-Motion>', lambda e: self.scan_dragto(e.x, e.y, gain=1))
        
        
        #Set geographic coordinates and zoom level of map, initialize shapes
        if 'lat_lon_zoom' in kwargs:
            lat_lon_zoom = kwargs.pop('lat_lon_zoom')
            self.default_offset, self.default_ratio = self.set_canvas_location(lat_lon_zoom[0], lat_lon_zoom[1], lat_lon_zoom[2])
        else:
            self.default_offset, self.default_ratio = self.set_canvas_location(-43.5765151113451, -22.9969539088035, 0.03)


        self.polyimages = []
        self.shapefiles = shapefiles


        #Add background image on map (if selected)
        if 'background_image' in kwargs:
            imagename = kwargs.pop('background_image')
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
            
        if 'null_zeros' in kwargs:
            self.null_zeros = kwargs.pop('null_zeros')
        else:
            self.null_zeros = 0
        
        
        #Draw and Place Map
        self.draw_map(self.shapefiles, color_range=self.color_rangename)
        self.pack(fill='both', expand=1)
        
        
        
    def draw_background(self, imagename):
        
        #Insert background image
        load = pil.Image.open(imagename)
        scaling = self.ratio/0.03
        load = load.resize((int(1300*scaling), int(800*scaling)), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(load)
        xcord, ycord = self.to_canvas_coordinates(-43.6555, -22.981)
        self.create_image(xcord,ycord,image=self.background,anchor="center")
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
    
    
    def set_canvas_location(self, longitude, latitude, zoomlevel):
        """SET MAP VISUAL LOCATION TO SPECIFIC COORDINATES AND ZOOM LEVEL
    
        Args:
            longitude: decimal longitude
            latitude: decimal latitude
            zoomlevel: Zoom level (higher numbers are more zoomed in. 0.03 is good start for sub-city level areas)
    
        Returns:
            N/A
        """
        #Move canvas center to specified coordinates
        locationx, locationy = self.to_canvas_coordinates(longitude, latitude)
        self.move('all', -locationx, -locationy)
        self.offset = (
            self.offset[0] - locationx,
            self.offset[1] - locationy
        )
        
        
        #Scale canvas to specified zoom level
        width, height = 943.0, 471.0
        self.scale('all', width, height, zoomlevel, zoomlevel)
        self.configure(scrollregion=self.bbox('all'))
        self.ratio *= float(zoomlevel)
        self.offset = (
            self.offset[0]*zoomlevel + width*(1 - zoomlevel),
            self.offset[1]*zoomlevel + height*(1 - zoomlevel)
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
        print(minim)
        print(maxim)
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
            colormap = cm.get_cmap('Reds', 48)
            norm = colors.Normalize(minim, minim+valuerange)
        
        
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
                            alpha = 0
                            
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
    sf = shapefile.Reader('/home/jackreid/Google Drive/School/Research/Space Enabled/Code/Decisions/Data/Chile/Shapefiles/chl_admbnda_adm1_bcn2018.shp')
    # py_giss = Map(root_window, [sf],
                  # background_image='./map.jpg', color_range=['POP'])
    py_giss = Map(root_window, [sf])
    root_window.mainloop()
