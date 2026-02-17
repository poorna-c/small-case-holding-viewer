import pandas as pd

def process_portfolio(file_path: str):
    # Load Excel file
    with pd.ExcelFile(file_path) as excel_file:
        required_columns = {"Date Range", "Constituents", "Weightage"}
        df = None
        for sheet in excel_file.sheet_names:
            temp_df = pd.read_excel(excel_file, sheet_name=sheet)
            if required_columns.issubset(temp_df.columns):
                df = temp_df
                break

        if df is None:
            raise ValueError("No worksheet contains required columns")



    # Forward fill Date Range
    df['Date Range'] = df['Date Range'].ffill()

    # Split Start and End Dates
    df[['Start Date', 'End Date']] = df['Date Range'].str.split(" to ", expand=True)

    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])

    df = df.sort_values(['Constituents', 'Start Date'])

    holding_periods = []

    for stock, group in df.groupby('Constituents'):
        group = group.sort_values('Start Date')

        entry = None
        exit_date = None
        prev_end = None

        for _, row in group.iterrows():
            current_start = row['Start Date']
            current_end = row['End Date']

            if entry is None:
                entry = current_start
                exit_date = current_end
                prev_end = current_end
                continue

            # If continuous (next period starts immediately after or overlaps)
            if (current_start - prev_end).days <= 1:
                exit_date = current_end
            else:
                # Close previous holding
                holding_periods.append({
                    "Stock": stock,
                    "Entry": entry,
                    "Exit": exit_date
                })
                entry = current_start
                exit_date = current_end

            prev_end = current_end

        # Append final holding
        holding_periods.append({
            "Stock": stock,
            "Entry": entry,
            "Exit": exit_date
        })

    holding_df = pd.DataFrame(holding_periods)

    # Correct duration calculation
    holding_df['Holding Days'] = (holding_df['Exit'] - holding_df['Entry']).dt.days + 1
    holding_df['Holding Weeks'] = round(holding_df['Holding Days'] / 7, 2)

    return holding_df
