import os
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

LEADS_COLUMNS = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']

LAYOUT_CONFIG = {
    'title': 'ECG Leads',
    'xaxis_title': 'Index',
    'yaxis_title': 'Values',
    'updatemenus': [{
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate',
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate',
                                  'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate',
            },
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top',
    }],
    'sliders': [{
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {'font': {'size': 20}, 'prefix': 'Lead:', 'visible': True, 'xanchor': 'right'},
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
    }],
}


def load_csv_data(file_path):
    df = pd.read_csv(file_path)
    print(f"Using existing CSV file: {file_path}")
    return df


def download_csv_data(url: str, image_file_name: str, download_path: str) -> Optional[pd.DataFrame]:
    print(f"CSV file not found. Performing web scraping...")

    # Use Chrome for web scraping
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--window-size=1920,1080")
    chromeOptions.add_argument('--start-maximized')
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--ignore-certificate-errors')
    chromeOptions.add_argument('--allow-running-insecure-content')
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    # Set download directory for Chrome
    chromeOptions.add_experimental_option('prefs', {'download.default_directory': download_path})
    driver = webdriver.Chrome(options=chromeOptions)
    driver.get(url)
    try:
        time.sleep(65)
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input.send_keys(os.path.abspath(image_file_name))
    except NoSuchElementException:
        print("No such element: Unable to locate 'Select Files' link.")
        driver.quit()
        return None
    try:
        time.sleep(60)
        element = driver.find_element(By.LINK_TEXT, 'Download Digitized ECG')
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element.click()
        time.sleep(10)
    except Exception as e:
        print(f"Exception occurred: {e}")
        driver.quit()
        return None
    try:
        time.sleep(5)
        driver.quit()
        return pd.read_csv(os.path.join(download_path, 'digitized_ecg_data.csv'))
    except FileNotFoundError:
        print("File not found: 'digitized_ecg_data.csv'")
        return None


def load_or_download_data(url, image_file_name, download_path, csv_file_name):
    csv_file_path = os.path.join(os.getcwd(), csv_file_name)
    if os.path.isfile(csv_file_path):
        return load_csv_data(csv_file_path)
    else:
        return download_csv_data(url, image_file_name, download_path)


def plot_data(df):
    fig = go.Figure()
    for lead in LEADS_COLUMNS:
        fig.add_trace(go.Scatter(x=df.index, y=df[lead], mode='lines', name=lead))
    fig.update_layout(**LAYOUT_CONFIG)
    frames = [go.Frame(data=[go.Scatter(x=df.index, y=df[lead], mode='lines')], name=lead) for lead in LEADS_COLUMNS]
    fig.frames = frames
    pio.write_html(fig, file='plots/ecg_leads.html')
    print("Interactive ECG Leads plot saved as 'plots/ecg_leads.html'.")


def download_and_plot_data(url, image_file_name, download_path, csv_file_name):
    df = load_or_download_data(url, image_file_name, download_path, csv_file_name)
    plot_data(df)


if __name__ == "__main__":
    url = "http://ecg-digitisation.hh.med.ic.ac.uk:8050/"
    image_file_name = "example_6by2.jpg"  # here enter your image file name
    download_path = os.path.dirname(os.path.abspath(__file__))
    download_and_plot_data(url, image_file_name, download_path, 'digitized_ecg_data.csv')
