# Big-Data-Filtering-Analysis-Tool
Big Data Filtering &amp; Analysis Tool: A Python-based GUI application for big data analysis using Bloom Filters and the Flajolet-Martin algorithm. Features include CSV file loading, column-wise analytics, visualization, and efficient distinct element counting.

---

## Features

1. **Load and Display CSV Data**:
   - Easily load CSV files and display a sample of data for analysis.
   - Uses `pandas` for data processing and `Treeview` for displaying rows.

2. **Column-wise Analytics**:
   - Select a column and visualize its data distribution via a pie chart.

3. **Efficient Distinct Element Counting**:
   - Estimate the number of unique elements in a dataset using the **Flajolet-Martin algorithm**.

4. **Bloom Filter for Data Filtering**:
   - Use a Bloom Filter to check the presence of elements in the dataset with minimal memory usage.

5. **Graphical User Interface (GUI)**:
   - Built with `Tkinter`, providing an interactive and user-friendly experience.

---

## Core Technologies

1. **Bloom Filter**:
   - Memory-efficient data structure for checking item presence with a low false positive rate.

2. **Flajolet-Martin Algorithm**:
   - A streaming algorithm for estimating distinct elements in big datasets.

3. **Data Visualization**:
   - Pie chart visualization using `matplotlib`.

4. **Pandas**:
   - For handling and processing CSV datasets.

5. **Tkinter**:
   - For building the graphical user interface.

---

## Requirements

### Software Requirements
- Python 3.6 or above
- Libraries:
  - `pandas`
  - `matplotlib`
  - `numpy`
  - `tkinter` (built-in with Python)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository-name/big-data-filtering.git
   cd big-data-filtering
