import vtk
import math

def get_screenshot(renWin, filename):
    renWin.Render()
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renWin)
    w2if.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(filename)
    writer.SetInput(w2if.GetOutput())
    writer.Write()
    renWin.Render()


###############################################################################
# setup transform
#
transform = vtk.vtkTransform()
transform.RotateWXYZ(180, 1, 0, 0)
move = [0, 0, 0]
transform.Translate(move)
#transformFilter = vtk.vtkTransformPolyDataFilter()
#transformFilter.SetTransform(transform)

transforms = []
transforms_filter = []

###############################################################################
# read obj file
#
obj_filename = '/mnt/data1/StandardBrain/SB/SB256.obj'
object = vtk.vtkOBJReader()
object.SetFileName(obj_filename)
objectSmoother = vtk.vtkSmoothPolyDataFilter()
objectSmoother.SetInputConnection(object.GetOutputPort())
objectSmoother.SetNumberOfIterations(100)

transforms_filter.append(vtk.vtkTransformPolyDataFilter())
transforms_filter[-1].SetTransform(transform)
transforms_filter[-1].SetInputConnection(objectSmoother.GetOutputPort())
transforms_filter[-1].Update()

objectMapper = vtk.vtkPolyDataMapper()
objectMapper.SetInputConnection(transforms_filter[-1].GetOutputPort())

objectActor = vtk.vtkActor()
objectActor.SetMapper(objectMapper)
#objectActor.GetProperty().SetRepresentationToWireframe();
objectActor.GetProperty().SetColor(0.5, 0.5, 0.5)
objectActor.GetProperty().SetOpacity(0.4)
#objectActor.GetProperty().SetOpacity(1.0)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(transforms_filter[-1].GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(1.0, 0.0, 0.0)
outlineActor.GetProperty().SetOpacity(0.2)
outlineActor.GetProperty().SetLineWidth(5)

line = vtk.vtkLineSource()
line.SetPoint1(0, -50, 0)
line.SetPoint2(100, -50, 0)
line.SetResolution(100)

line_mapper = vtk.vtkPolyDataMapper()
line_mapper.SetInputConnection(line.GetOutputPort())
line_actor = vtk.vtkActor()
line_actor.SetMapper(line_mapper)

###############################################################################
# read second obj file
#
filepos = '/mnt/data1/StandardBrain/SB/LALobj/'
obj_list = ['LAL1.obj','LAL2.obj','LAL3.obj','LAL4.obj','LAL5.obj', 'LAL1_flip.obj', 'LAL2_flip.obj', 'LAL3_flip.obj', 'LAL4_flip.obj', 'LAL5_flip.obj']

lut = vtk.vtkLookupTable()
lut.Build()
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)

objs = []
objs_mapper = []
objs_actor = []
objs_smoother = []
for i, obj_name in enumerate(obj_list):
    objs.append(vtk.vtkOBJReader())
    objs[-1].SetFileName(filepos+obj_name)

    objs_smoother.append(vtk.vtkSmoothPolyDataFilter())
    objs_smoother[-1].SetInputConnection(objs[-1].GetOutputPort())
    objs_smoother[-1].SetNumberOfIterations(50)

    transforms_filter.append(vtk.vtkTransformPolyDataFilter())
    transforms_filter[-1].SetTransform(transform)
    transforms_filter[-1].SetInputConnection(objs_smoother[-1].GetOutputPort())
    transforms_filter[-1].Update()

    objs_mapper.append(vtk.vtkPolyDataMapper())
    objs_mapper[-1].SetInputConnection(transforms_filter[-1].GetOutputPort())
    objs_mapper[-1].SetLookupTable(lut)
    objs_actor.append(vtk.vtkActor())
    objs_actor[-1].SetMapper(objs_mapper[-1])
    rgb = [0.8, 0.8, 0.8]
    #lut.GetColor((i / float(len(obj_list))), rgb)
    objs_actor[-1].GetProperty().SetColor(rgb)
    objs_actor[-1].GetProperty().SetOpacity(0.3)

neuronpos = '/mnt/data1/StandardBrain/highres/'
neuron_list = ['0004.obj', '0004flip.obj', 
               '0005.obj', '0005flip.obj', 
               '0008.obj', '0008flip.obj', 
               '0009.obj', '0009flip.obj', 
               '0012.obj', '0012flip.obj', 
               '0017.obj', '0017flip.obj', 
               '0019.obj', '0019flip.obj',
               '0021.obj', '0021flip.obj',
               '0655.obj', '0655flip.obj',
               '0661.obj', '0661flip.obj', 
               '0663.obj', '0663flip.obj', 
               '0664.obj', '0664flip.obj', 
               '0965.obj', '0965flip.obj', 
               '0969.obj', '0969flip.obj', 
               '0970.obj', '0970flip.obj', 
               '0973.obj', '0973flip.obj', 
               '0984.obj', '0984flip.obj', 
               '0986.obj', '0986flip.obj', 
               '9999.obj', '9999flip.obj', 
]
#neuron_list = []
#neuron_list = ['0970.obj']
neurons = []
neurons_mapper = []
neurons_actor = []
neurons_smoother = []
for i, neuron_name in enumerate(neuron_list):
    neurons.append(vtk.vtkOBJReader())
    neurons[-1].SetFileName(neuronpos+neuron_name)

    neurons_smoother.append(vtk.vtkSmoothPolyDataFilter())
    neurons_smoother[-1].SetInputConnection(neurons[-1].GetOutputPort())
    neurons_smoother[-1].SetNumberOfIterations(50)

    transforms_filter.append(vtk.vtkTransformPolyDataFilter())
    transforms_filter[-1].SetTransform(transform)
    transforms_filter[-1].SetInputConnection(neurons_smoother[-1].GetOutputPort())
    transforms_filter[-1].Update()

    neurons_mapper.append(vtk.vtkPolyDataMapper())
    neurons_mapper[-1].SetInputConnection(transforms_filter[-1].GetOutputPort())
    neurons_mapper[-1].SetLookupTable(lut)
    neurons_actor.append(vtk.vtkActor())
    neurons_actor[-1].SetMapper(neurons_mapper[-1])
    rgb = [0.0, 0.0, 0.0]
    lut.GetColor( ((len(neuron_list) - i) / float(len(neuron_list))), rgb)
    neurons_actor[-1].GetProperty().SetColor(rgb)
    #neurons_actor[-1].GetProperty().SetColor(0.6, 0.2, 0.4)
    if i%2 == 0:
        neurons_actor[-1].GetProperty().SetOpacity(1)
    else:
        neurons_actor[-1].GetProperty().SetOpacity(0.2)
    neurons_actor[-1].GetProperty().SetOpacity(1.0)

###############################################################################
# draw axis
#
axesActor = vtk.vtkAxesActor()


###############################################################################
# prepare rendering
#
'''
dist = 3000
camera = vtk.vtkCamera()
camera.SetPosition(512, -500, dist)
camera.SetFocalPoint(512, -500, 0)
camera.ComputeViewPlaneNormal()
camera.SetParallelProjection(1)
'''
ren = vtk.vtkRenderer()

ren.AddActor(objectActor)
#ren.AddActor(outlineActor)
#ren.AddActor(line_actor)
#ren.AddActor(scalar_bar)

for actor in objs_actor:
    ren.AddActor(actor)
for actor in neurons_actor:
    ren.AddActor(actor)

#ren.AddActor(axesActor)
ren.SetBackground(.0, .0, .0)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('Silkmoth Brain Viewer')
renWin.SetSize(2000, 1200)


iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()

#ren.SetActiveCamera(camera)
#ren.ResetCamera()


'''
num_images = 120
camera = ren.GetActiveCamera()
ren.ResetCamera()
#camera.ParallelProjectionOn()
camera.SetClippingRange(1.0, 10000)
camera.Zoom(1)

for i in range(num_images):
    get_screenshot(renWin, 'screenshot'+str(i)+'.png')
    camera.Azimuth(360./num_images)
    #ren.ResetCamera()
'''

iren.Start()
