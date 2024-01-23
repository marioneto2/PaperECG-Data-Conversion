import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
import time
import os

class ECGPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ECG Plotter")
        self.root.geometry("1200x600")

        self.file_name = None
        self.download_path = os.path.abspath(os.path.dirname(__file__))
        self.plots_folder = os.path.join(self.download_path, "plots")

        self.create_widgets()

    def create_widgets(self):
        self.file_label = tk.Label(self.root, text="Select ECG File:")
        self.file_label.pack(pady=10)

        self.file_button = tk.Button(self.root, text="Choose File", command=self.choose_file)
        self.file_button.pack(pady=10)

        self.plot_button = tk.Button(self.root, text="Plot ECG", command=self.plot_ecg)
        self.plot_button.pack(pady=10)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

        # Example buttons for different leads
        leads_columns = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']

        for lead in leads_columns:
            lead_button = tk.Button(self.root, text=f"Lead {lead.upper()}", command=lambda l=lead: self.show_plot(l))
            lead_button.pack(pady=5)

    def choose_file(self):
        self.file_name = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.file_name:
            print(f"Selected File: {self.file_name}")

    def plot_ecg(self):
        if self.file_name:
            download_and_plot_data(url, self.file_name, self.download_path)
            self.display_plots()

    def display_plots(self):
        # Code to display plots
        # For now, just show the first plot (Lead 'i')
        lead_name = 'i'
        plot_path = os.path.join(self.plots_folder, f"{lead_name}_plot.png")
        self.show_plot(lead_name, plot_path)

    def show_plot(self, lead_name, plot_path=None):  # Update method signature
        if plot_path is None:
            # If plot_path is not provided, generate it based on lead_name
            plot_path = os.path.join(self.plots_folder, f"{lead_name}_plot.png")

        try:
            plot_image = Image.open(plot_path)
            tk_image = ImageTk.PhotoImage(plot_image)

            # Update the image label to display the new plot
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image

            print(f"Displaying plot for Lead {lead_name}")
        except FileNotFoundError:
            print(f"Plot for lead {lead_name} not found.")

def download_and_plot_data(url, file_name, download_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    prefs = {'download.default_directory': download_path}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    time.sleep(20)

    file_input = driver.find_element("css selector", 'input[type="file"]')
    file_input.send_keys(os.path.abspath(file_name))

    time.sleep(120)

    download_link = driver.find_element("link text", "Download Digitized ECG")
    download_link.click()

    time.sleep(10)

    driver.quit()

    df = pd.read_csv(os.path.join(download_path, 'digitized_ecg_data.csv'))
    leads_columns = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']

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
    url = "http://ecg-digitisation.hh.med.ic.ac.uk:8050/"

    root = tk.Tk()
    app = ECGPlotterApp(root)
    root.mainloop()
