# MODE SELECTION
# wide_open: Checks if the photo was taken with the exact f/number given. In this case,
# define the f/number as the minimum for the lens.
# max_open: Checks if the photo was taken with a value below the f/number given

#mode = 'max_open'
mode = 'wide_open'


# CAMERA MAKER AND SYSTEM
# For exemple: for a 'Canon EOS Rebel T5i' the
# maker is 'Canon' and the system is 'EOS'.

camera = {
    'maker'  : 'Canon',
    'system' : 'EOS'
}


# Lenses to check the number of photos that were taken with wide open f/number,
# or in case mode is 'max_open' the ones that were taken with an f/number
# below the defined threshold.
#
# The fields are:
# [ 'Lens', min f/number, number of photos, total of photos ]
#
# The 'lens score' is the number of photos in the user's photostream
# taken with the camera and system defined above and with a focal length
# that is covered by the 'Lens'. Its initial value must always be 0.

lenses = [
    [ 'Canon EF-S 10-18mm f/4.5-5.6 IS STM',       4.5, 0, 0 ],
    [ 'Canon EF-S 18-55mm f/3.5-5.6 IS STM',       3.5, 0, 0 ],
    [ 'Canon EF-S 55-250mm f/4-5.6 IS STM',        4.0, 0, 0 ],
    [ 'Canon EF-S 24mm f/2.8 STM',                 2.8, 0, 0 ],
    [ 'Canon EF 50mm f/1.8 STM',                   1.8, 0, 0 ]
]

# +---------------------------+
# | F STOPS TABLE             |
# +---------------------------+
# |  1/2 stops  |  1/3 stops  |
# +---------------------------+
# |    f/1.0    |    f/1.0    |
# |             |    f/1.1    |
# |    f/1.2    |    f/1.2    |
# |    f/1.4    |    f/1.4    |
# |             |    f/1.6    |
# |    f/1.7    |             |
# |             |    f/1.8    |
# |    f/2.0    |    f/2.0    |
# |             |    f/2.2    |
# |    f/2.4    |             |
# |             |    f/2.5    |
# |    f/2.8    |    f/2.8    |
# |             |    f/3.2    |
# |    f/3.3    |             |
# |             |    f/3.5    |
# |    f/4.0    |    f/4.0    |
# |             |    f/4.5    |
# |    f/4.8    |             |
# |             |    f/5.0    |
# |    f/5.6    |    f/5.6    |
# |             |    f/6.3    |
# |    f/6.7    |             |
# |             |    f/7.1    |
# |    f/8.0    |    f/8.0    |
# +---------------------------+
