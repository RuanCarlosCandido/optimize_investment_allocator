import pandas as pd

# Replace 'sample_data.csv' with the path to your actual CSV file
csv_file_path = 'sample_data.csv'

def calculate_and_update_contribution(csv_file_path, new_contribution):
    if new_contribution < 0:
        return 0

    df = pd.read_csv(csv_file_path)
    df['ValorInvestido'] = df['ValorInvestido'].astype(float)
    df['ProporcaoIdeal'] = df['ProporcaoIdeal'].astype(float)

    total_current_investment = df['ValorInvestido'].sum()
    total_future_investment = total_current_investment + new_contribution

    # Directly calculating and updating 'Aporte' without 'AporteCalculado' column
    df['Aporte'] = (total_future_investment * df['ProporcaoIdeal'] - df['ValorInvestido']).apply(lambda x: max(x, 0))

    total_aporte = df['Aporte'].sum()
    if total_aporte > new_contribution:
        correction_factor = new_contribution / total_aporte
        df['Aporte'] = df['Aporte'] * correction_factor

    # Update the original CSV file with the new 'Aporte' values
    df.to_csv(csv_file_path, columns=['Tipo', 'Subtipo', 'ValorInvestido', 'ProporcaoIdeal', 'Aporte'], index=False)

    return df[['Tipo', 'Subtipo', 'ValorInvestido', 'ProporcaoIdeal', 'Aporte']]

# Example usage
new_contribution = 10000
calculate_and_update_contribution(csv_file_path, new_contribution)

# Print the updated DataFrame to verify the changes
updated_df = pd.read_csv(csv_file_path)
print(updated_df)

