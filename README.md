# Vida Modeling
User Interface and Simulation Platform for a System Dynamics Model
Part of the Vida Decision Support System for COVID-19
Managed by the Space Enabled Research Group at the Massachusetts Institute of Technology
For more information on the Vida project, see https://www.media.mit.edu/projects/vida-decision-support-system/overview/

For questions, please contact Jack Reid at jackreid@mit.edu

This project utilizes numerous different, primarily public government data sources from around the world. For more information on the data, its sources,
and how it is formated in this repository, see SD_UI/Data/Data_Header_Explanation.txt and SD_UI/Data/Data_Descriptions.xlsx. For information on the
permitted uses of this data, please see the original source for that data.

The license for this code is available in the [LICENSE file](https://github.com/mitmedialab/Vida_Modeling/blob/master/LICENSE).

SD_UI_v1_5.py is the primary python script that runs the user interface.
SDlib_v1_v4.py is a package defining the underlying system dyanmics model.
MapWindow_v4.py is a package defining the visualization of shapefiles and their associated data in the user interface.
translations.csv serves as a lookup table to translate text in the user interface.
Context_Status_tracker.txt notes the current development status of each context area (i.e. each application location) of the user interface.
The Data folder contains all of the data using by the user interface. See Data/Data_Header_Explanation.txt for more details.
The Auxilary Files contains various scripts used by the developers to process data and conduct other actions. These are not directly used by SD_UI_v1_5.py.

# How to Use Vida / Installation
There are two primary ways to use Vida. The first is to download or clone this repository and to run it in Python 3. This can be done by running:   
```
  $ git clone git@github.com:your_name_here/geemap.git   
```
Note that various dependencies are required to run Vida in Python. These dependencies are listed in the following section.

The other way is through the use of an executable. The Vida team can generate these for certain operating systems. If you are interested in an executable, please email jackreid@mit.edu to request one. Make sure to include the operating system that you use.

# Dependencies
- array2gif
- csv
- gdal
- tkinter
- matplotlib
- numpy
- pillow
- pyproj
- pyshp
- screeninfo
- shapely

# License / Copying / Forking
You are welcome to take this code and create your own version. Perhaps you have custom needs or you have proprietary data that don't want to make public. That's fine. See the [license page](https://github.com/mitmedialab/Vida_Modeling/blob/master/LICENSE) for more details on legality and restrictions. If you do make improvements to the code that you think would be useful to others, however, I encourage you to contribute them to the public version. You can see more details on this in the following section.

# Contributing
Contributions are welcome from all. Feel free to report issues, implement fixes/features, and participate in general. Make sure to check out the [code of conduct](https://github.com/mitmedialab/Vida_Modeling/blob/master/CODE_OF_CONDUCT.md) beforehand. There are a variety of ways that you can contribute and some of them are listed here. If you are new to python or github, see the following section for information on how to get started.

## Submit Ideas for New Features, Report Bugs, and Send Feedback
If you have ideas for new features or want to report bugs, you can do this over at: https://github.com/mitmedialab/Vida_Modeling/issues

In either case, please make sure to include as much details as possible.

## Implement Features and Fix bugs
Take a look through the listed Github issues for things that need addressing then go right ahead and submit a pull request. The Vida team will review it and merge it.

## Write Documentation
It's always a struggle to keep documentation up to date with the state of the code. Feel free to update things or even just point out vague or out-of-date documents.

# Getting Started with GitHub
First off, if you are new to git entirely, I suggest you take a look at *Pro Git* by Scott Chacon and Ben Straub. It is freely available online at https://git-scm.com/book/en/v2

With that out of the way, here are the steps for contributing on Github

1. Make a GitHub account if you don't already have one.
2. Fork the Vida repo to your github account. This can be done by clicking the **Fork** button on the top right of this page.
3. Clone your fork to your local computer:   
    ```
    $ git clone git@github.com:your_name_here/Vida_Modeling.git
    ```
4. Make a virtual environment and install Vida into it. If you have virtualenvwrapper installed, this can be done by: 
    ```  
    $ mkvirtualenv Vida_Modeling   
    $ cd Vida_Modeling/   
    $ python setup.py develop 
    ```
5. Create a branch for local development:  
    ``` 
    $ git checkout -b name-of-your-branch
    ```
6. Once your done with your changes, commit them and push the branch back to GitHub:   
    ```
    $ git add .   
    $ git commit -m "Description of the changes that you made"   
    $ git push origin name-of-your-branch   
    ```
7. Submit a pull request through the GitHub website. You can see more details on how to do this here: https://guides.github.com/activities/hello-world/
