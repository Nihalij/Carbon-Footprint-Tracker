import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import os
import subprocess


# Emission Factors

travel_factors = {
    "Car (Petrol)": 0.095,
    "Car (Diesel)": 0.110,
    "Bus": 0.097,
    "Bike": 0.050,
    "Flight": 0.255
}

electricity_map = {"Low(0-100 kWh)": 10, "Medium(101-300 kWh)": 25, "High(300+ kWh)": 40}
diet_map = {"Vegan": 2.89, "Vegetarian": 3.81, "Mixed": 5.63, "High Meat": 7.1}


# Generate Month Data


def generate_month_data():
    start_date = datetime(2025, 10, 1)
    records = []

    for i in range(30):
        date = start_date + timedelta(days=i)
        mode = np.random.choice(list(travel_factors.keys()))
        km = np.random.randint(5, 150)
        elec = np.random.choice(list(electricity_map.keys()))
        diet = np.random.choice(list(diet_map.keys()))
        rec = np.random.choice(["Yes", "No"])

        travel_co2 = round(km * travel_factors[mode], 2)
        electricity_co2 = electricity_map[elec]
        diet_co2 = diet_map[diet]
        total = round(travel_co2 + electricity_co2 + diet_co2, 2)

        if rec == "Yes":
            total = round(total * 0.9, 2)

        records.append([
            date.strftime("%Y-%m-%d"), mode, km, travel_co2,
            elec, electricity_co2, diet, diet_co2, rec, total
        ])

    df = pd.DataFrame(records, columns=[
        "Date", "Travel_Mode", "Travel_km", "Travel_CO2",
        "Electricity_Usage", "Electricity_CO2",
        "Diet_Type", "Diet_CO2", "Recycling", "Total_CO2"
    ])

    df.to_csv("carbon_gui_data.csv", index=False)
    messagebox.showinfo("Dataset Saved", "1 Month Sample Data Generated Successfully!")


# Manual Entry Add

def calculate():
    mode = travel_mode.get()
    km = entry_km.get()
    elec = electricity_level.get()
    diet = diet_type.get()
    rec = recycle_var.get()

    if mode == "" or km == "" or elec == "" or diet == "" or rec == "":
        messagebox.showwarning("Missing Info", "Please fill all fields before saving the entry!")
        return

    try:
        km = float(km)
        if km <= 0:
            messagebox.showwarning("Invalid Input", "Travel distance must be greater than 0!")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Travel distance must be a valid number!")
        return

    travel_co2 = round(km * travel_factors[mode], 2)
    electricity_co2 = electricity_map[elec]
    diet_co2 = diet_map[diet]

    total_co2 = round(travel_co2 + electricity_co2 + diet_co2, 2)
    if rec == "Yes":
        total_co2 = round(total_co2 * 0.9, 2)

    result_label.config(text=f"Total CO₂: {total_co2} kg/day")

    new_entry = pd.DataFrame({
        "Date": [datetime.now().strftime("%Y-%m-%d")],
        "Travel_Mode": [mode],
        "Travel_km": [km],
        "Travel_CO2": [travel_co2],
        "Electricity_Usage": [elec],
        "Electricity_CO2": [electricity_co2],
        "Diet_Type": [diet],
        "Diet_CO2": [diet_co2],
        "Recycling": [rec],
        "Total_CO2": [total_co2]
    })

    try:
        old_df = pd.read_csv("carbon_gui_data.csv")
        df = pd.concat([old_df, new_entry], ignore_index=True)
    except FileNotFoundError:
        df = new_entry

    df.to_csv("carbon_gui_data.csv", index=False)
    messagebox.showinfo("Saved", "Your entry was saved successfully!")

def open_data_file():
    filepath = "carbon_gui_data.csv"   # jaha tumhara data save ho raha hai
    
    if os.path.exists(filepath):
        try:
            subprocess.Popen(['start', filepath], shell=True)  # Windows ke liye
        except Exception as e:
            messagebox.showerror("Error", f"File cannot open: {e}")
    else:
        messagebox.showerror("Error", "File not found!")

# Graphs

def show_Line():
    df = pd.read_csv("carbon_gui_data.csv")
    plt.figure(figsize=(9, 5))
    sns.lineplot(x="Date", y="Total_CO2", data=df, marker="o", color="green")
    plt.title("CO₂ Emission Trend", fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Total CO₂ Emission")
    plt.xticks(rotation=45)
    plt.grid(":")
    plt.tight_layout()
    plt.show()

def show_pie():
    df = pd.read_csv("carbon_gui_data.csv")

    labels = ["Travel", "Electricity", "Diet"]
    values = [
        df["Travel_CO2"].sum(),
        df["Electricity_CO2"].sum(),
        df["Diet_CO2"].sum()
    ]

    colors = sns.color_palette("Set2")
    explode = [0.1, 0, 0]

    plt.figure(figsize=(8, 6))
    plt.pie(values, labels=labels, colors=colors,
            autopct="%1.1f%%", explode=explode, shadow=True)
    plt.title("Combined CO₂ Contribution", fontweight="bold")
    plt.show()

def show_Heatmap():
    df = pd.read_csv("carbon_gui_data.csv")
    heat_df = df[["Diet_CO2", "Travel_CO2", "Electricity_CO2", "Total_CO2"]]

    plt.figure(figsize=(6, 4))
    sns.heatmap(heat_df.corr(), annot=True, cmap="Greens", linewidths=0.5)
    plt.title("CO₂ Emission Correlation Heatmap")
    plt.tight_layout()
    plt.show()

def show_bar():
    df = pd.read_csv("carbon_gui_data.csv")

    labels = ["Travel", "Electricity", "Diet"]
    values = [
        df["Travel_CO2"].sum(),
        df["Electricity_CO2"].sum(),
        df["Diet_CO2"].sum()
    ]

    plt.figure(figsize=(8, 6))
    colors = sns.color_palette("Set2")
    plt.bar(labels, values, color=colors, edgecolor="black")
    plt.title("Combined CO₂ Contribution", fontweight="bold")
    plt.xlabel("Sources of CO₂ Emission")
    plt.ylabel("Total CO₂ Emission (kg)")
    plt.grid(":")
    plt.tight_layout()
    plt.show()

def show_graph():
    choice = diff_graphs.get()

    if choice == "Line Graph":
        show_Line()
    elif choice == "Pie Chart":
        show_pie()
    elif choice == "Bar Graph":
        show_bar()
    elif choice == "Heatmap":
        show_Heatmap()
    else:
        messagebox.showwarning("Warning", "Please select a valid graph")

# GUI Design

root = tk.Tk()
root.title("Carbon Footprint Tracker")
root.geometry("800x600")
root.config(bg="#a0dbb8")

# Background Image
img_path = Image.open(r"C:\Users\aadis\Downloads\WhatsApp Image 2025-11-20 at 09.28.13_55c210f0.jpg")
img_path = img_path.resize((800, 700))
img = ImageTk.PhotoImage(img_path)

bg_img = tk.Label(root, image=img)
bg_img.place(x=0, y=0, relwidth=1, relheight=1)
bg_img.lower()

title = tk.Label(root, text="EcoStep", font=("Verdana", 20),bg ="#1d8f4c",fg="#000000")
title.pack(pady=10)

frame = tk.Frame(root, bg="#f6fcf2")
frame.pack(pady=5)

# Input Widgets
tk.Label(frame, text="Travel Mode", bg="#f6fcf2").grid(row=0, column=0, pady=5, sticky="w")
travel_mode = ttk.Combobox(frame, values=list(travel_factors.keys()))
travel_mode.grid(row=0, column=1)

tk.Label(frame, text="Travel Distance (km)", bg="#f6fcf2").grid(row=1, column=0, pady=5, sticky="w")
entry_km = tk.Entry(frame)
entry_km.grid(row=1, column=1)

tk.Label(frame, text="Electricity Usage", bg="#f6fcf2").grid(row=2, column=0, pady=5, sticky="w")
electricity_level = ttk.Combobox(frame, values=list(electricity_map.keys()))
electricity_level.grid(row=2, column=1)

tk.Label(frame, text="Diet Type", bg="#f6fcf2").grid(row=3, column=0, pady=5, sticky="w")
diet_type = ttk.Combobox(frame, values=list(diet_map.keys()))
diet_type.grid(row=3, column=1)

tk.Label(frame, text="Do you recycle?", bg="#f6fcf2").grid(row=4, column=0, pady=5, sticky="w")
recycle_var = ttk.Combobox(frame, values=["Yes", "No"])
recycle_var.grid(row=4, column=1)

tk.Label(frame, text="Graph", bg="#f6fcf2").grid(row=5, column=0, pady=5, sticky="w")
diff_graphs = ttk.Combobox(frame, values=["Line Graph", "Pie Chart", "Bar Graph", "Heatmap"])
diff_graphs.grid(row=5, column=1)

# Buttons
tk.Button(root, text="Generate 1 Month Data", command=generate_month_data,
          bg="#1d8f4c", fg="white", width=18).pack(pady=10)

tk.Button(root, text="Add My Entry", command=calculate,
          bg="#1d8f4c", fg="white", width=18).pack(pady=5)

tk.Button(root, text="Graphs", command=show_graph,
          bg="#1d8f4c", fg="white", width=18).pack(pady=10)
tk.Button(root, text="Open Data File", command=open_data_file, bg="#1d8f4c",fg="white").pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 13, "bold"),
                        bg="#eafaf1", fg="#0c6e3e")
result_label.pack(pady=10)

root.mainloop()
