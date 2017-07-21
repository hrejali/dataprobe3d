cmake_minimum_required(VERSION 2.8.9)

project(DataProbe3D)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/DataProbe3D")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Jason Kai (Robarts Research Institute), Saeed Bakhshmand  (CSTAR), Hossein Rejali (Robarts Resaerch Institue), Brian Wang (Western University), Serene Abu-Sardanah (University of Waterloo)")
set(EXTENSION_DESCRIPTION "An extension for a data probe for the 3D viewer.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/DataProbe3D.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/DataProbe3D/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(DataProbe3D)
add_subdirectory(DataProbe3DActual)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
