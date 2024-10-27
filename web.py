import streamlit as st
from config import CHARTS, TIMEFRAMES_TO_SELENIUM_KEY
import requests
# from printer_code import print_two_images,print_image

def print_two_images(path1,path2):
    print(f"Images: {path1}, and {path2} have been saved!")

st.title('Chart Screenshot Tool')

# chart = st.selectbox('Select Chart', ('EUR', 'DXY'))
currencies = list(CHARTS.keys())
timeframe = st.selectbox('Select Timeframe', list(TIMEFRAMES_TO_SELENIUM_KEY.keys()))

if st.button('Capture Screenshot'):
    try:
        screenshot_paths = []
        for chart in currencies:
            response = requests.get(f"http://localhost:8000/capture/{chart}/{timeframe}")
            if response.status_code == 200:
                screenshot_path = response.json()['screenshot_path']
                st.success(f"Screenshot saved at {screenshot_path}")
                screenshot_paths.append(screenshot_path)
                # Here, you could add functionality to display the screenshot or trigger the printing
            else:
                st.error("Failed to capture screenshot")
        if len(screenshot_paths)==2:
            dxy_image = [path for path in screenshot_paths if 'dxy' in path.lower()]
            eur_image = [path for path in screenshot_paths if 'eur' in path.lower()]
            if len(dxy_image) and len(eur_image):
                print_two_images(dxy_image[0],eur_image[0])
    except Exception as e:
        print(f"Some Error Occured: {str(e)}")

