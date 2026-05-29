import pandas as pd
import matplotlib.pyplot as plt

# Used to read the TTC files
codes = pd.read_csv("Code_Descriptions.csv")
delays = pd.read_csv("TTC_Delay_data2025.csv")

# Keep only needed columns
codes = codes[["CODE", "DESCRIPTION"]]

# Rename so both files use the same column name
codes = codes.rename(columns={"CODE": "Code"})

# Main category map
category_map = {
    # Passenger
    "MUIS": "Passenger",
    "MUIRS": "Passenger",
    "MUIE": "Passenger",
    "MUI": "Passenger",
    "MUIR": "Passenger",
    "PUMST": "Passenger",
    "PUMEL": "Passenger",
    "SUAE": "Passenger",
    "SUAP": "Passenger",
    "SUDP": "Passenger",
    "SUUT": "Passenger",
    "SUO": "Passenger",
    "SUPOL": "Passenger",
    "SUSA": "Passenger",
    "SUG": "Passenger",
    "SUROB": "Passenger",
    "SUSP": "Passenger",
    "SUBT": "Passenger",
    "MUPR1": "Passenger",
    "MUD": "Passenger",
    "PUTDN": "Passenger",
    "PUTD": "Passenger",

    # Operational
    "TUNOA": "Operational",
    "TUNIP": "Operational",
    "TUSC": "Operational",
    "TUMVS": "Operational",
    "TUS": "Operational",
    "TUCC": "Operational",
    "TUSUP": "Operational",
    "TUOS": "Operational",
    "TUNCA": "Operational",
    "TUATC": "Operational",
    "TUO": "Operational",
    "TUKEY": "Operational",
    "MUCL": "Operational",
    "PUTOE": "Operational",
    "TUST": "Operational",
    "TUML": "Operational",
    "TUOPO": "Operational",
    "TUUR": "Operational",
    "MUNCA": "Operational",
    "MUNOA": "Operational",
    "MUESA": "Operational",
    "MUTO": "Operational",
    "MUTD": "Operational",
    "MUWEA": "Operational",
    "MUWR": "Operational",
    "MUCP": "Operational",

    # Infrastructure
    "MUSAN": "Infrastructure",
    "EUSC": "Infrastructure",
    "PUTR": "Infrastructure",
    "MUPLC": "Infrastructure",
    "PUOPO": "Infrastructure",
    "PUSTC": "Infrastructure",
    "EUO": "Infrastructure",
    "SUEAS": "Infrastructure",
    "EUBK": "Infrastructure",
    "MUSC": "Infrastructure",
    "MUATC": "Infrastructure",
    "EUBO": "Infrastructure",
    "PUSTS": "Infrastructure",
    "PUMO": "Infrastructure",
    "EUAL": "Infrastructure",
    "EUOPO": "Infrastructure",
    "EUDO": "Infrastructure",
    "EUVE": "Infrastructure",
    "PUTWZ": "Infrastructure",
    "MUDD": "Infrastructure",
    "PUSRA": "Infrastructure",
    "EUPI": "Infrastructure",
    "MUPF": "Infrastructure",
    "PUSAC": "Infrastructure",
    "EUME": "Infrastructure",
    "PUSWZ": "Infrastructure",
    "EUTL": "Infrastructure",
    "EUAC": "Infrastructure",
    "PUSIS": "Infrastructure",
    "PUSNT": "Infrastructure",
    "PUSCR": "Infrastructure",
    "PUSO": "Infrastructure",
    "PUTIJ": "Infrastructure",
    "EULV": "Infrastructure",
    "PUTSM": "Infrastructure",
    "PUTTP": "Infrastructure",
    "PUSI": "Infrastructure",
    "TUSET": "Infrastructure",
    "PUCSC": "Infrastructure",
    "EUTM": "Infrastructure",
    "PUATC": "Infrastructure",
    "EUATC": "Infrastructure",
    "PUEO": "Infrastructure",
    "PUTIS": "Infrastructure",
    "PUSSW": "Infrastructure",
    "MUEC": "Infrastructure",
    "EUYRD": "Infrastructure",
    "EUCA": "Infrastructure",
    "PUCSS": "Infrastructure",
    "MUPLA": "Infrastructure",
    "PUTSC": "Infrastructure",
    "EUHV": "Infrastructure",
    "PUSZC": "Infrastructure",
    "PUSTP": "Infrastructure",
    "MUFS": "Infrastructure",
    "PUSIO": "Infrastructure",
    "PUTTC": "Infrastructure",
    "PUTCD": "Infrastructure",
    "EULT": "Infrastructure",
    "EUVA": "Infrastructure",
    "EUECD": "Infrastructure",
    "EUTR": "Infrastructure",
    "EUTRD": "Infrastructure",
    "EUCO": "Infrastructure",
    "PUDCS": "Infrastructure",
    "PUEME": "Infrastructure",
    "PUCBI": "Infrastructure",
    "PUSCA": "Infrastructure",
    "PUTS": "Infrastructure",
}

# First pass using exact code matches
codes["Category"] = codes["Code"].map(category_map)

# Backup catch function
def catch_category(description):
    if pd.isna(description):
        return "Other"

    desc = description.lower()

    passenger_words = [
        "customer", "patron", "assault", "robbery", "suspicious",
        "bomb threat", "injured/ill", "medical", "unauthorized",
        "police", "graffiti"
    ]
    operational_words = [
        "operator", "collector", "transportation", "supervisory",
        "tower controller", "schedule", "crew"
    ]
    infrastructure_words = [
        "signal", "track", "rail", "power", "electrical", "door",
        "equipment", "vehicle", "radio", "scada", "brakes", "couplers",
        "propulsion", "trainline", "lighting", "voltage", "switch"
    ]

    if any(word in desc for word in passenger_words):
        return "Passenger"
    elif any(word in desc for word in operational_words):
        return "Operational"
    elif any(word in desc for word in infrastructure_words):
        return "Infrastructure"
    else:
        return "Other"

# Fill missing categories with backup catcher
codes["Category"] = codes["Category"].fillna(
    codes["DESCRIPTION"].apply(catch_category)
)

# Merge categories into full TTC delay dataset
df = delays.merge(codes, on="Code", how="left")

# Check first few rows
print(df[["Code", "DESCRIPTION", "Category"]].head(20))

# Category totals
print("\nCategory counts:")
print(df["Category"].value_counts())

# Remaining uncategorized codes
others = df[df["Category"] == "Other"][["Code", "DESCRIPTION"]].drop_duplicates()
print("\nStill in Other:")
print(others.to_string(index=False))

# Summary stats
category_counts = df["Category"].value_counts()
category_minutes = df.groupby("Category")["Min Delay"].sum()
category_avg = df.groupby("Category")["Min Delay"].mean()

print("\nDelay incidents by category:")
print(category_counts)

print("\nTotal delay minutes by category:")
print(category_minutes)

print("\nAverage delay minutes by category:")
print(category_avg)

# Export summaries
category_counts.to_csv("category_counts.csv")
category_minutes.to_csv("category_minutes.csv")
category_avg.to_csv("category_average_minutes.csv")

# Chart 1
category_counts.plot(kind="bar")
plt.title("Number of TTC Delay Incidents by Category")
plt.xlabel("Category")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("delay_counts_by_category.png")
plt.show()

# Chart 2
category_minutes.plot(kind="bar")
plt.title("Total TTC Delay Minutes by Category")
plt.xlabel("Category")
plt.ylabel("Total Delay Minutes")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("delay_minutes_by_category.png")
plt.show()

# Chart 3
category_avg.plot(kind="bar")
plt.title("Average TTC Delay Minutes by Category")
plt.xlabel("Category")
plt.ylabel("Average Delay Minutes")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("average_delay_by_category.png")
plt.show()

# ----------------------------
# Passenger deeper analysis
# ----------------------------

# Passenger-only data
passenger_df = df[df["Category"] == "Passenger"].copy()

# Summarize passenger codes
passenger_summary = (
    passenger_df.groupby(["Code", "DESCRIPTION"])
    .agg(
        incidents=("Code", "size"),
        total_delay=("Min Delay", "sum"),
        avg_delay=("Min Delay", "mean")
    )
    .reset_index()
)

# Preventability score
# 3 = high preventability, 2 = medium, 1 = low
preventability_map = {
    "SUDP": 3,    # Disorderly patron
    "SUUT": 3,    # Unauthorized at track level
    "MUD": 3,     # Passenger door problem
    "SUG": 2,     # Graffiti
    "PUTD": 2,    # Debris at track level - controllable
    "SUSP": 2,    # Suspicious package
    "SUO": 2,     # Security other
    "SUAP": 2,    # Assault / patron involved
    "SUAE": 2,    # Assault / employee involved
    "SUPOL": 1,   # Held by police
    "MUI": 1,     # Injured/ill customer on train transported
    "MUIR": 1,    # Injured/ill customer on train aid refused
    "MUIS": 1,    # Injured/ill customer in station transported
    "MUIRS": 1,   # Injured/ill customer in station aid refused
    "PUMST": 1,   # Passenger assistance/stairway
    "PUMEL": 1,   # Escalator/elevator related
    "MUPR1": 1,   # Train in contact with person
    "SUROB": 1,   # Robbery
    "SUSA": 1,    # Sexual assault
    "SUBT": 1,    # Bomb threat
    "PUTDN": 1,   # Debris at track level - not controllable
    "MUIE": 1     # Injured employee
}

passenger_summary["Preventability"] = passenger_summary["Code"].map(preventability_map).fillna(1)

# Save table
passenger_summary.to_csv("passenger_priority_matrix.csv", index=False)

print("\nPassenger code summary:")
print(passenger_summary.sort_values("total_delay", ascending=False).to_string(index=False))


# Chart 4: Top passenger delay codes by total delay minutes
# Chart 4: Top passenger delay codes by total delay minutes
top_passenger = passenger_summary.sort_values("total_delay", ascending=False).head(10).copy()

label_map_bar = {
    "SUDP": "SUDP - Disorderly patron",
    "MUIR": "MUIR - Ill/injured customer, aid refused",
    "SUUT": "SUUT - Unauthorized at track level",
    "MUI": "MUI - Ill/injured customer, transported",
    "SUO": "SUO - Security other",
    "SUAP": "SUAP - Assault / patron involved",
    "MUPR1": "MUPR1 - Train in contact with person",
    "SUPOL": "SUPOL - Held by police",
    "MUD": "MUD - Passenger door problem",
    "SUAE": "SUAE - Assault / employee involved"
}

top_passenger["Label"] = top_passenger["Code"].map(label_map_bar).fillna(top_passenger["Code"])

plt.figure(figsize=(10, 6))
plt.barh(top_passenger["Label"], top_passenger["total_delay"])
plt.title("Top Passenger Delay Codes by Total Delay Minutes")
plt.xlabel("Total Delay Minutes")
plt.ylabel("Passenger Delay Type")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top_passenger_delay_codes.png")
plt.show()

# Chart 5: Cleaner priority matrix using top passenger codes only
top_priority = passenger_summary.sort_values("total_delay", ascending=False).head(10).copy()

label_map = {
    "SUDP": "Disorderly patron",
    "SUUT": "Unauthorized at track level",
    "MUIR": "Ill/injured customer, aid refused",
    "MUI": "Ill/injured customer, transported",
    "SUO": "Security incident - other",
    "SUAP": "Assault - patron involved",
    "SUAE": "Assault - employee involved",
    "MUPR1": "Train in contact with person",
    "SUPOL": "Held by police",
    "MUD": "Passenger door problem"
}

top_priority["ShortLabel"] = top_priority["Code"].map(label_map).fillna(top_priority["Code"])

plt.figure(figsize=(10, 6))
plt.scatter(
    top_priority["Preventability"],
    top_priority["total_delay"],
    s=top_priority["incidents"] * 0.4,
    alpha=0.7
)

for _, row in top_priority.iterrows():
    plt.text(
        row["Preventability"] + 0.03,
        row["total_delay"],
        row["ShortLabel"],
        fontsize=9
    )

plt.title("Top Passenger Delay Codes: Preventability vs Total Delay Minutes")
plt.xlabel("Preventability Score (1 = Low, 3 = High)")
plt.ylabel("Total Delay Minutes")
plt.xticks([1, 2, 3], ["Low", "Medium", "High"])
plt.tight_layout()
plt.savefig("passenger_priority_matrix_clean.png")
plt.show()