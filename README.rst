# dataprobe3d
===============

DataProbe3D was developed as a part of the Slicer Project Week Western
<http://wiki.imaging.robarts.ca/index.php/Main_Page>

About
-----

DataProbe3D initial development is loosely based off of the existing Slicer data probe 
and makes use of existing Slicer libraries. The probe makes use of the crosshair available 
in both the 3D view and the slice views. Using an existing 3D model and the crosshair, RAS 
is returned to the user in the upper left corner of the 3D view. If there is a volume loaded 
in the background layer of the slice view, scalar metrics are extracted fm this layer and 
returned to the user in the upper right corner.

Contributors
-------------
Jason Kai, Saeed Bakhshmand, Hossein Rejali, Brian Wang, Serene Abu-Sardanah
KhanLab, Robarts Research Institute, Western University and
CSTAR, London Health Sciences Centre, Western University

.. topic:: **Thanks**
    * The experts present at Slicer Week Western for their support and guidance in the 
      development of this tool
    * The developer (Steve Pieper) and contributers of the existing Slicer dataprobe.
    * The organizing committee of Slicer Project Week Western for providing an environment which
      made the development possible.
