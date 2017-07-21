import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
from EditorLib.EditUtil import EditUtil

#
# DataProbe3D
#

class DataProbe3D(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "DataProbe3D" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Jason Kai (Robarts Research Institute), Saeed Bakhshmand (CSTAR), Hossein Rejali (Robarts Research Institute), Brian Wang (Western University), Serene Abu-Sardanah (University of Waterloo)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It contains code for a dataprobe for the 3D viewer. Currently, mainly used for testing purposes.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.

Many thanks to the experts available during Slicer Week Western for their support and guidance with developing the module. 
""" # replace with organization, grant and thanks.

#
# DataProbe3DWidget
#

class DataProbe3DWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Run Code"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Run")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    pass

  def onApplyButton(self):
    logic = DataProbe3DLogic()
    logic.run()

#
# DataProbe3DLogic
#

class DataProbe3DLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def reportInfo(self, ras, val=None):
      lm = slicer.app.layoutManager()
      w = lm.threeDWidget(0)
      threeDview = w.threeDView()
      ca = threeDview.cornerAnnotation()

      ca.SetText(vtk.vtkCornerAnnotation.UpperLeft, 'R: ' + str(ras[0]) + '\nA: ' + str(ras[1]) + '\nS: ' + str(ras[2]))

      if val is not None:
        ca.SetText(vtk.vtkCornerAnnotation.UpperRight, 'Value: ' + str(val))
      else:
        ca.SetText(vtk.vtkCornerAnnotation.UpperRight, '')

      ca.GetTextProperty().SetColor(1,1,0)
      threeDview.forceRender()

  def volumeInfo(self, volumeNode, ras):
      rasH = [ras[0], ras[1], ras[2], 1]

      RAStoIJK = vtk.vtkMatrix4x4()
      
      imageData = volumeNode.GetImageData()
      volumeNode.GetRASToIJKMatrix(RAStoIJK)
      ijkH = RAStoIJK.MultiplyPoint(rasH)

      val = imageData.GetScalarComponentAsDouble(int(round(ijkH[0])), int(round(ijkH[1])), int(round(ijkH[2])), 0)

      return val

  def onMouseEvent(self, observer, eventid):
      ras = [0.0, 0.0, 0.0]
      ras = slicer.util.getNode('Crosshair').GetCrosshairRAS()

      compositeNode = EditUtil.getCompositeNode()
      bgID = compositeNode.GetBackgroundVolumeID()

      if bgID == None:
        self.reportInfo(ras)
        return
      else:
        volumeNode = slicer.mrmlScene.GetNodeByID(bgID)
	val = self.volumeInfo(volumeNode, ras)          
        self.reportInfo(ras, val)

  def run(self):
    """
    Run the actual algorithm
    """
    crosshairNode = slicer.util.getNode('Crosshair')
    crosshairNode.SetCrosshairMode(2) # Turn on crosshair by default
    crosshairNode.AddObserver(slicer.vtkMRMLCrosshairNode.CursorPositionModifiedEvent,  self.onMouseEvent)


class DataProbe3DTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py

  NOTE: Test case does not currently work
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_DataProbe3D1()

  def test_DataProbe3D1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = DataProbe3DLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
