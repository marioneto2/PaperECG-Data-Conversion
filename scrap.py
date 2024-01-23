import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ECGPlotterApp:
    def __init__(self):
        self.file_name = None
        self.download_path = os.path.abspath(os.path.dirname(__file__))
        self.plots_folder = os.path.join(self.download_path, "plots")
        self.leads_columns = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
        self.create_widgets()

    def create_widgets(self):
        self.choose_file()

    def choose_file(self):
        self.file_name = input("Enter the ECG file path (jpg, jpeg, or png): ")
        if os.path.exists(self.file_name):
            print(f"Selected File: {self.file_name}")
            self.plot_ecg()
        else:
            print("File not found. Exiting...")

    def plot_ecg(self):
        if self.file_name:
            download_and_plot_data(self.file_name, self.download_path)
            self.display_plots()

    def display_plots(self):
        # For now, just show the first plot (Lead 'i')
        lead_name = 'i'
        plot_path = os.path.join(self.plots_folder, f"{lead_name}_plot.png")
        self.show_plot(lead_name, plot_path)

    def show_plot(self, lead_name, plot_path=None):
        if plot_path is None:
            plot_path = os.path.join(self.plots_folder, f"{lead_name}_plot.png")

        try:
            df = pd.read_csv(os.path.join(self.download_path, 'digitized_ecg_data.csv'))

            fig = make_subplots(rows=1, cols=1, subplot_titles=[f'Lead {lead_name.upper()}'])
            fig.add_trace(go.Scatter(x=df.index, y=df[lead_name], mode='lines', name=f'Lead {lead_name.upper()}'))

            fig.update_layout(title_text=f'ECG Plot - Lead {lead_name.upper()}',
                              xaxis_title='Index',
                              yaxis_title='Values')

            fig.show()

            print(f"Displaying plot for Lead {lead_name}")
        except FileNotFoundError:
            print(f"Plot for lead {lead_name} not found.")

def download_and_plot_data(file_name, download_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    prefs = {'download.default_directory': download_path}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://ecg-digitisation.hh.med.ic.ac.uk:8050/")

    time.sleep(20)

    file_input = driver.find_element("css selector", 'input[type="file"]')
    file_input.send_keys(os.path.abspath(file_name))

    time.sleep(120)

    download_link = driver.find_element("link text", "Download Digitized ECG")
    download_link.click()

    time.sleep(10)

    driver.quit()

    df = pd.read_csv(os.path.join(download_path, 'digitized_ecg_data.csv'))
    os.makedirs("plots", exist_ok=True)

    for lead in leads_columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df.index, df[lead])
        ax.set_title(lead)
        ax.set_xlabel('Index')
        ax.set_ylabel('Values')

        plt.savefig(f'plots/{lead}_plot.png')
        plt.close()

    print("Plots are saved in the 'plots' folder.")

if __name__ == "__main__":
    app = ECGPlotterApp()
