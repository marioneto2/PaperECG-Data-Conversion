# ECG Data Analysis and Plotting with Plotly

The goal is to automate data conversion for training AI models from paper ECG data. Special thanks to the authors, more information about the projects I built this around, please check ["A fully-automated paper ECG digitisation algorithm using deep learning"](https://www.nature.com/articles/s41598-022-25284-1).

This Python script, `plotly_scrap.py`, facilitates the download of ECG data from a dedicated website ("http://ecg-digitisation.hh.med.ic.ac.uk:8050/") and subsequent plotting of the acquired data using the Plotly library.

![example_6by2.jpg](example_6by2.jpg)
*Image extracted from authors website.*

## Dependencies

Ensure the following Python libraries are installed in your environment:

```bash
pip install os pandas plotly selenium
```

## Overview of Script

### Constants

Define the leads of interest in the ECG data using the `LEADS_COLUMNS` constant.

```python
LEADS_COLUMNS = [...]
```

Configure the layout for the final plot using the `LAYOUT_CONFIG` constant.

```python
LAYOUT_CONFIG = {...}
```

### Functions

#### `load_csv_data(file_path)`

Load a local CSV file.

```python
df = load_csv_data(file_path)
```

#### `download_csv_data(url: str, image_file_name: str, download_path: str)`

Utilize Chrome for web scraping to download the CSV file containing the data. The headless option is turned on, running Chrome without a GUI.

```python
download_csv_data(url, image_file_name, download_path)
```

#### `load_or_download_data(url, image_file_name, download_path, csv_file_name)`

Check if a local CSV file exists with the required data. If found, load the local CSV file; otherwise, download the data.

```python
df = load_or_download_data(url, image_file_name, download_path, csv_file_name)
```

#### `plot_data(df)`

Plot the ECG data using Plotly.

```python
plot_data(df)
```

#### `download_and_plot_data(url, image_file_name, download_path, csv_file_name)`

Download the ECG data if not already locally available and then plot the data.

```python
download_and_plot_data(url, image_file_name, download_path, csv_file_name)
```
