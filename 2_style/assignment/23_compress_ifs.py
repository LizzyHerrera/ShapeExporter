# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#**********************************************************************************

def set_color(ctrlList=None, color=None):

    color_mapping = {1: 4,
                     2: 13,
                     3: 25,
                     4: 17,
                     5: 17,
                     6: 15,
                     7: 6,
                     8: 16}

    for ctrlName in ctrlList:
        override_col_attr = ctrlName + 'Shape.overrideColor'
        try:
            mc.setAttr(override_col_attr, color_mapping[color])
        except:
            pass

# EXAMPLE
# set_color(['circle','circle1'], 8)
