# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
# ************************************************************************************

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""


class Object:
    def __init__(self, name):
        self.name = name
        self.trans_values = [0, 0, 0]
        self.rot_values = [0, 0, 0]
        self.scale_values = [1, 1, 1]

    def translate(self, x, y, z):
        self.trans_values = [x, y, z]
        print(f'Translation Values : x = {x} , y = {y} , z = {z}')

    def rotate(self, x, y, z):
        self.rot_values = [x, y, z]
        print(f'Rotation Values : x = {x} , y = {y} , z = {z}')

    def scale(self, x, y, z):
        self.scale_values = [x, y, z]
        print(f'Scale Values : x = {x} , y = {y} , z = {z}')


class Cube(Object):
    def __init__(self, name):
        super().__init__(name)
        self.color_values = [0, 0, 0]

    def color(self, r, g, b):
        self.color_values = [r, g, b]
        print(f'Color Values : R = {r} , G = {g} , B = {b}')

    def print_status(self):
        print('***** STATUS *****')
        print(f'Name: {self.name}')
        print(f'Translation: {self.trans_values}')
        print(f'Rotation: {self.rot_values}')
        print(f'Scale: {self.scale_values}')
        print(f'Color: {self.color_values}')
        print('******************')

    def update_transform(self, type, value):
        x, y, z = value
        transforms = {'translate': self.translate,
                      'rotate': self.rotate,
                      'scale': self.scale}
        if type in transforms:
            return transforms[type](x, y, z)
        else:
            raise ValueError(f'Unknown type: "{type}". Valid types are: "translate", "rotate", "scale".')


##############################################################################################


cube1 = Cube('cube_01')
cube2 = Cube('cube_02')
cube3 = Cube('cube_03')


cube1.translate(1.0, 2.0, 3.0)
cube1.rotate(45.0, 0.0, 90.0)
cube1.scale(1.5, 2.5, 3.5)
cube1.color(255, 0, 0)
cube1.print_status()

cube2.translate(4.0, 5.0, 6.0)
cube2.rotate(30.0, 60.0, 90.0)
cube2.scale(0.5, 1.5, 2.5)
cube2.color(0, 255, 0)
cube2.print_status()

cube3.translate(7.0, 8.0, 9.0)
cube3.rotate(90.0, 45.0, 30.0)
cube3.scale(2.0, 3.0, 4.0)
cube3.color(0, 0, 255)
cube3.print_status()
