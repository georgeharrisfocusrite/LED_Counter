import streamlit as st
from pathlib import Path

from classes import Image


def load_image(path, caption=None, channels='BGR'):
    width = 800
    return st.image(path, caption=caption, width=width, use_column_width=False, clamp=False, channels=channels, format='JPEG')

def build_ui(images):
    st.sidebar.title('Show Images')
    for im in images:
        if st.sidebar.checkbox(im.caption, value=im.show):
            load_image(im.image, caption=im.caption, channels=im.channels)

def sliders():
    st.sidebar.title('Variables')
    slider_values = {
        'scale': st.sidebar.slider('image scale', 0.01, 1.0, 1.0),
        'blur': st.sidebar.slider('blur', 2, 40, 2, step=2) - 1,
        'thresh': st.sidebar.slider('low brightness threshold', 1, 254, 140)
        }
    return slider_values

def result(images):
    image = images[0]
    gray = image.grayed
    blur = gray.blurred
    blobs = blur.countleds
    expected = 512
    detected = blobs
    st.write(f"{detected} LEDs were detected.")
    if detected != expected:
        if detected > expected:
            st.write('FAIL: Too many blobs detected, check for glare')
        else:
            st.write('FAIL: Too few blobs, check for broken LEDs')
    else:
        st.write('PASS!')
        st.balloons()



def dropdown(path):
    path.mkdir(parents=True, exist_ok=True)
    names = [file.name for file in path.iterdir()]
    st.sidebar.title('Images')
    chosen = st.sidebar.selectbox('Choose Image', names)
    x = path / chosen
    return( x.as_posix() )

# Draw a title and some text to the app:
'''
# LED Detection

'''

slider_values = sliders()



# load image
image = Image( image_path=dropdown(Path('images')), thresh=slider_values['thresh'], scale=slider_values['scale'], blur=slider_values['blur'] )

images = [image, image.grayed, image.grayed.blurred, image.grayed.blurred.masked]

result(images)

build_ui(images)