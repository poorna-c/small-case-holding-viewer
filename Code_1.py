import pandas as pd

# Load excel
df = pd.read_excel("portfolio.xlsx")

# Forward fill Date Range column
df['Date Range'] = df['Date Range'].ffill()

# Extract start date
df['Start Date'] = df['Date Range'].str.split(" to ").str[0]
df['Start Date'] = pd.to_datetime(df['Start Date'])

# Sort
df = df.sort_values(['Constituents', 'Start Date'])


holding_periods = []

for stock, group in df.groupby('Constituents'):
    group = group.sort_values('Start Date')
    dates = group['Start Date'].unique()

    entry = dates[0]
    prev_date = dates[0]

    for current_date in dates[1:]:
        if (current_date - prev_date).days > 7:
            # Exit detected
            holding_periods.append({
                "Stock": stock,
                "Entry": entry,
                "Exit": prev_date
            })
            entry = current_date

        prev_date = current_date

    # Final exit
    holding_periods.append({
        "Stock": stock,
        "Entry": entry,
        "Exit": prev_date
    })

holding_df = pd.DataFrame(holding_periods)

holding_df['Holding Days'] = (holding_df['Exit'] - holding_df['Entry']).dt.days
holding_df['Holding Weeks'] = holding_df['Holding Days'] / 7

import plotly.express as px

fig = px.timeline(
    holding_df,
    x_start="Entry",
    x_end="Exit",
    y="Stock",
    color="Stock"
)

fig.update_yaxes(autorange="reversed")
fig.show()
