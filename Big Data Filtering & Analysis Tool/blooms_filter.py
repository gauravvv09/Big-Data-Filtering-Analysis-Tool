import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from hashlib import sha256
import numpy as np

class BloomFilter:
    def __init__(self, size):
        self.size = size
        self.bit_array = np.zeros(size, dtype=bool)

    def add(self, item):
        hash1 = self._hash1(item)
        hash2 = self._hash2(item)
        self.bit_array[hash1] = True
        self.bit_array[hash2] = True

    def check(self, item):
        hash1 = self._hash1(item)
        hash2 = self._hash2(item)
        return self.bit_array[hash1] and self.bit_array[hash2]

    def _hash1(self, item):
        return int(sha256(str(item).encode()).hexdigest(), 16) % self.size

    def _hash2(self, item):
        return (self._hash1(item) + 1) % self.size

class BloomFilterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Big Data Filtering & Analysis")
        self.root.geometry("800x600")
        self.root.configure(bg='lightblue')

        # Initialize Bloom Filter and Data
        self.bloom_filter = None
        self.data = None
        self.size = 100  # Size of the Bloom Filter

        # Create GUI Widgets
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Big Data Analytics Project", font=("Arial", 18, "bold"), bg='lightblue')
        title_label.pack(pady=10)

        # Load CSV Button
        self.load_button = tk.Button(self.root, text="Load CSV File", command=self.load_csv, bg='orange', font=("Arial", 12))
        self.load_button.pack(pady=10)

        # Treeview to display data
        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        # Column Selection
        self.column_label = tk.Label(self.root, text="Select Column for Analysis:", bg='lightblue', font=("Arial", 12))
        self.column_label.pack(pady=10)
        self.column_combobox = ttk.Combobox(self.root, state="readonly", font=("Arial", 12))
        self.column_combobox.pack(pady=5)

        # Button to show analytics graph
        self.graph_button = tk.Button(self.root, text="Show Column-wise Analytics", command=self.show_graph, bg='lightcoral', font=("Arial", 12))
        self.graph_button.pack(pady=10)

        # Button to count distinct elements using Flajolet-Martin
        self.distinct_button = tk.Button(self.root, text="Count Distinct Elements (Flajolet-Martin)", command=self.count_distinct_elements, bg='pink', font=("Arial", 12))
        self.distinct_button.pack(pady=10)

        # Button to check presence in Bloom Filter
        self.check_button = tk.Button(self.root, text="Check Item Presence in Bloom Filter", command=self.check_item_presence, bg='lightgreen', font=("Arial", 12))
        self.check_button.pack(pady=10)

        # Button to show trailing elements
        self.trail_button = tk.Button(self.root, text="Show Maximum Trailing Number (Flajolet-Martin)", command=self.show_max_trailing_number, bg='lightblue', font=("Arial", 12))
        self.trail_button.pack(pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)

                # Check if data is empty
                if self.data.empty:
                    messagebox.showwarning("Data Warning", "The loaded CSV file is empty.")
                    return

                # Display a sample of the data
                self.display_data()
                self.populate_columns()

                # Initialize Bloom Filter
                self.bloom_filter = BloomFilter(self.size)
                self.bloom_filter.bit_array.fill(False)  # Reset the Bloom Filter matrix
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def display_data(self):
        # Clear the treeview
        self.tree.delete(*self.tree.get_children())

        # Display a sample of the data for large datasets
        sample_data = self.data.sample(n=min(100, len(self.data)))  # Sample 100 rows or less if data is smaller
        self.tree["column"] = list(sample_data.columns)
        for col in sample_data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Add sampled rows to the treeview
        for index, row in sample_data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def populate_columns(self):
        # Populate the column selection combo box
        self.column_combobox['values'] = list(self.data.columns)
        if self.column_combobox['values']:
            self.column_combobox.current(0)  # Select the first column by default

    def show_graph(self):
        if self.data is not None:
            selected_column = self.column_combobox.get()
            if selected_column:
                column_data = self.data[selected_column].dropna()

                # Count unique values and their frequencies
                counts = column_data.value_counts()

                # Limit the number of categories for pie chart
                if len(counts) > 10:
                    counts = counts[:10]  # Show top 10 categories only

                plt.figure(figsize=(10, 6))
                plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
                plt.title(f"Distribution of '{selected_column}'", fontsize=15)
                plt.axis('equal')  # Equal aspect ratio ensures pie chart is circular
                plt.show()
            else:
                messagebox.showwarning("Selection Error", "Please select a column to analyze.")
        else:
            messagebox.showwarning("Data Error", "No data loaded to analyze.")

    def count_distinct_elements(self):
        if self.data is not None:
            selected_column = self.column_combobox.get()
            if selected_column:
                column_data = self.data[selected_column].dropna().tolist()
                for item in column_data:
                    self.bloom_filter.add(item)  # Add each item to the Bloom Filter

                estimated_distinct_count, max_trailing_number = self.flajolet_martin(column_data)
                messagebox.showinfo("Distinct Count", f"Estimated number of distinct elements in '{selected_column}': {estimated_distinct_count}\nMax Trailing Number: {max_trailing_number}")
            else:
                messagebox.showwarning("Selection Error", "Please select a column to count distinct elements.")
        else:
            messagebox.showwarning("Data Error", "No data loaded to count distinct elements.")

    def flajolet_martin(self, data):
        # Flajolet-Martin algorithm for counting distinct elements
        B = 16  # Number of bits to use
        M = 1 << B  # Size of the bit vector
        bit_vector = [0] * M
        max_trailing_number = 0
        
        for item in data:
            hash_value = int(sha256(str(item).encode()).hexdigest(), 16)
            index = hash_value % M
            trailing_number = self._get_lowest_non_zero_bit(hash_value)
            bit_vector[index] = trailing_number
            max_trailing_number = max(max_trailing_number, trailing_number)

        # Calculate the estimated distinct count
        estimated_distinct_count = 2 ** max(bit_vector)
        return estimated_distinct_count, max_trailing_number

    def _get_lowest_non_zero_bit(self, num):
        # Returns the count of trailing non-zero bits in num
        return (num & -num).bit_length()

    def check_item_presence(self):
        if self.data is not None:
            selected_column = self.column_combobox.get()
            if selected_column:
                items_to_check = self.data[selected_column].dropna().tolist()
                results = [(item, self.bloom_filter.check(item)) for item in items_to_check]

                # Display results
                results_text = "\n".join([f"{item}: {'Present' if present else 'Not Present'}" for item, present in results])
                messagebox.showinfo("Bloom Filter Presence", results_text)
            else:
                messagebox.showwarning("Selection Error", "Please select a column to check presence.")
        else:
            messagebox.showwarning("Data Error", "No data loaded to check presence.")

    def show_max_trailing_number(self):
        if self.data is not None:
            selected_column = self.column_combobox.get()
            if selected_column:
                column_data = self.data[selected_column].dropna().tolist()
                estimated_distinct_count, max_trailing_number = self.flajolet_martin(column_data)
                messagebox.showinfo("Max Trailing Number", f"Max Trailing Number: {max_trailing_number}\nEstimated distinct elements: {estimated_distinct_count}")
            else:
                messagebox.showwarning("Selection Error", "Please select a column to show the max trailing number.")
        else:
            messagebox.showwarning("Data Error", "No data loaded to show the max trailing number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BloomFilterGUI(root)
    root.mainloop()
