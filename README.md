# SD_UI
User Interface and Simulation Platform for a System Dynamics Model
Part of the Vida Decision Support System for COVID-19
Managed by the Space Enabled Research Group at the Massachusetts Institute of Technology
For more information on the Vida project, see https://www.media.mit.edu/projects/vida-decision-support-system/overview/

For questions, please contact Jack Reid at jackreid@mit.edu

This project utilizes numerous different, primarily public government data sources from around the world. For more information on the data, its sources, 
and how it is formated in this repository, see SD_UI/Data/Data_Header_Explanation.txt and SD_UI/Data/Data_Descriptions.xlsx. For information on the 
permitted uses of this data, please see the original source for that data.

The license for this code is currently under discussion. This README will be updated when it has been determined.

SD_UI_v1_5.py is the primary python script that runs the user interface.
SDlib_v1_v4.py is a package defining the underlying system dyanmics model.
MapWindow_v4.py is a package defining the visualization of shapefiles and their associated data in the user interface.
translations.csv serves as a lookup table to translate text in the user interface.
Context_Status_tracker.txt notes the current development status of each context area (i.e. each application location) of the user interface.
The Data folder contains all of the data using by the user interface. See Data/Data_Header_Explanation.txt for more details.
The Auxilary Files contains various scripts used by the developers to process data and conduct other actions. These are not directly used by SD_UI_v1_5.py.

