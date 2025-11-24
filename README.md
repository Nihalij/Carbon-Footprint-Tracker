🌿 Carbon Footprint Tracker (Python Tkinter GUI)
"Track your carbon footprint and take a step toward a greener planet." 🌿

A desktop application built using **Python Tkinter** that calculates and tracks a user's daily **carbon footprint** based on travel, electricity usage, diet, and recycling habits.  
The project also generates visual graphs and stores data in a CSV file for long-term analysis.

 👉Features:

✔ Manual Entry System

- Enter travel mode & distance  
- Select electricity usage range  
- Choose diet type  
- Select recycling preference  
- Automatic CO₂ calculation  

✔ Auto Dataset Generator

- Generates **1 month of sample data**
- Uses random values (travel, diet, electricity)
- Saves as `carbon_gui_data.csv`

✔ Graphs & Data Visualization

- **Line Chart** – CO₂ trend over time  
- **Pie Chart** – Contribution comparison  
- **Bar Graph** – Total emissions by category  
- **Heatmap** – Correlation between factors  

✔ CSV File Support

- Saves all entries in CSV  
- Loads previous data  
- One-click button to open data file  

 ✔ GUI Design
 
- Background image  
- Modern Combobox inputs  
- Buttons with custom colors  
- Clean & user-friendly layout  


👉Technologies Used:

- **Python**
- **Tkinter (GUI)**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Seaborn**
- **Pillow (Image handling)**

👉Floder structure:
 Carbon-Footprint-Tracker-GUI/

│

├── main.py # Full Tkinter application

├── carbon_gui_data.csv # Auto-generated dataset

├── assets/

│ └── bg.jpg # GUI background image

│

├── requirements.txt # Required libraries

└── README.md # Repository description

👉Project Objective:

The goal of this project is to:
- Create awareness about carbon emissions  
- Track daily activities contributing to CO₂  
- Provide users with visual insights  
- Encourage eco-friendly habits  


👉Possible Future Enhancements:

- Login system for multiple users  
- Export monthly report as PDF  
- Light/Dark UI theme  
- Cloud storage support  
- Mobile app version  

