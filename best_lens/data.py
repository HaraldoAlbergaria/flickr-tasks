# Camera maker and system
# For exemple: for a 'Canon EOS Rebel T5i' the
# maker is 'Canon' and the system is 'EOS'.

camera = {
    'maker'  : 'Canon',
    'system' : 'EOS'
}


# Lenses to be compared to define the best one, based in the history
# of photos taken in the focal length covered by the lenses in the list.
#
# The fields are:
# [ 'Lens', min focal length, max focal length, lens score ]
#
# The 'lens score' is the number of photos in the user's photostream
# taken with the camera and system defined above and with a focal length
# that is covered by the 'Lens'. Its initial value must always be 0.

lenses = [
    [ 'Canon EF-S 10-18mm f/4.5-5.6 IS STM',       10,  18, 0 ],
    [ 'Canon EF-S 18-55mm f/3.5-5.6 IS STM',       18,  55, 0 ],
    [ 'Canon EF-S 55-250mm f/4-5.6 IS STM',        55, 250, 0 ],
    [ 'Canon EF-S 24mm f/2.8 STM',                 24,  24, 0 ],
    [ 'Canon EF 50mm f/1.8 STM',                   50,  50, 0 ]
]
