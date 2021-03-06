#!/usr/bin/env python

# This example reads a volume dataset, extracts two isosurfaces that
# represent the skin and bone, and then displays them.

import vtk
from parameter_config import dcm_dir, rescale_slope, rescale_intercept


# Create the renderer, the render window, and the interactor. The
# renderer draws into the render window, the interactor enables mouse-
# and keyboard-based interaction with the scene.
aRenderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(aRenderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# The following reader is used to read a series of 2D slices (images)
# that compose the volume.
v16 = vtk.vtkDICOMImageReader()
v16.SetDataByteOrderToLittleEndian()
v16.SetDirectoryName(dcm_dir)

# An isosurface, or contour value of 500 is known to correspond to the
# skin of the patient. Once generated, a vtkPolyDataNormals filter is
# is used to create normals for smooth surface shading during rendering.
# The triangle stripper is used to create triangle strips from the
# isosurface these render much faster on may systems.
skinExtractor = vtk.vtkContourFilter()
skinExtractor.SetInputConnection(v16.GetOutputPort())
skin_contour_values = 500 * rescale_slope + rescale_intercept
skinExtractor.SetValue(0, skin_contour_values)
skinNormals = vtk.vtkPolyDataNormals()
skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
skinNormals.SetFeatureAngle(60.0)
skinStripper = vtk.vtkStripper()
skinStripper.SetInputConnection(skinNormals.GetOutputPort())
skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinStripper.GetOutputPort())
skinMapper.ScalarVisibilityOff()
skin = vtk.vtkActor()
skin.SetMapper(skinMapper)
# skin.GetProperty().SetDiffuseColor(1, .49, .25)
skin.GetProperty().SetDiffuseColor(248/255, 197/255, 183/255)
skin.GetProperty().SetSpecular(.3)
skin.GetProperty().SetSpecularPower(20)

# An isosurface, or contour value of 1150 is known to correspond to the
# bone of the patient. Once generated, a vtkPolyDataNormals filter is
# is used to create normals for smooth surface shading during rendering.
# The triangle stripper is used to create triangle strips from the
# isosurface these render much faster on may systems.
boneExtractor = vtk.vtkContourFilter()
boneExtractor.SetInputConnection(v16.GetOutputPort())
bone_contour_values = 1150 * rescale_slope + rescale_intercept
boneExtractor.SetValue(0, bone_contour_values)
boneNormals = vtk.vtkPolyDataNormals()
boneNormals.SetInputConnection(boneExtractor.GetOutputPort())
boneNormals.SetFeatureAngle(60.0)
boneStripper = vtk.vtkStripper()
boneStripper.SetInputConnection(boneNormals.GetOutputPort())
boneMapper = vtk.vtkPolyDataMapper()
boneMapper.SetInputConnection(boneStripper.GetOutputPort())
boneMapper.ScalarVisibilityOff()
bone = vtk.vtkActor()
bone.SetMapper(boneMapper)
bone.GetProperty().SetDiffuseColor(1, 1, .9412)

# An outline provides context around the data.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(v16.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0, 0, 0)

# It is convenient to create an initial view of the data. The FocalPoint
# and Position form a vector direction. Later on (ResetCamera() method)
# this vector is used to position the camera to look at the data in
# this direction.
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, 1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()

# Actors are added to the renderer. An initial camera view is created.
# The Dolly() method moves the camera towards the FocalPoint,
# thereby enlarging the image.
aRenderer.AddActor(outline)
aRenderer.AddActor(skin)
aRenderer.AddActor(bone)
aRenderer.SetActiveCamera(aCamera)
aRenderer.ResetCamera()
aCamera.Dolly(1.5)

# Set a background color for the renderer and set the size of the
# render window (expressed in pixels).
aRenderer.SetBackground(1, 1, 1)
renWin.SetSize(640, 480)

# Note that when camera movement occurs (as it does in the Dolly()
# method), the clipping planes often need adjusting. Clipping planes
# consist of two planes: near and far along the view direction. The
# near plane clips out objects in front of the plane the far plane
# clips out objects behind the plane. This way only what is drawn
# between the planes is actually rendered.
aRenderer.ResetCameraClippingRange()

# Interact with the data.
iren.Initialize()
renWin.Render()
iren.Start()
