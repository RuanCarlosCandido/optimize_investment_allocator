import pandas as pd
import sys

# Substitua 'sample_data.csv' pelo caminho para o seu arquivo CSV real
csv_file_path = 'sample_data.csv'

def calculate_and_update_contribution(csv_file_path, new_contribution):
    if new_contribution < 0:
        return 0

    df = pd.read_csv(csv_file_path)
    df['ValorInvestido'] = df['ValorInvestido'].astype(float)
    df['ProporcaoIdeal'] = df['ProporcaoIdeal'].astype(float)

    total_current_investment = df['ValorInvestido'].sum()
    print(f"Soma atual dos investimentos: {total_current_investment}")

    total_future_investment = total_current_investment + new_contribution

    # Calcula e atualiza 'Aporte' diretamente
    df['Aporte'] = (total_future_investment * df['ProporcaoIdeal'] - df['ValorInvestido']).apply(lambda x: max(x, 0))

    total_aporte = df['Aporte'].sum()
    if total_aporte > new_contribution:
        correction_factor = new_contribution / total_aporte
        df['Aporte'] = df['Aporte'] * correction_factor

    # Atualiza o arquivo CSV original com os novos valores de 'Aporte'
    df.to_csv(csv_file_path, columns=['Tipo', 'Subtipo', 'ValorInvestido', 'ProporcaoIdeal', 'Aporte'], index=False)
    
    # Imprime a soma dos investimentos após o novo aporte
    print(f"Soma dos investimentos após o novo aporte: {total_future_investment}")

    return df[['Tipo', 'Subtipo', 'ValorInvestido', 'ProporcaoIdeal', 'Aporte']]

if __name__ == "__main__":
    # Verifica se o valor do aporte foi passado como argumento
    if len(sys.argv) != 2:
        print("Erro: O valor do aporte do mês deve ser passado como parâmetro obrigatório.")
        print("Uso: python script.py <valor_aporte>")
        sys.exit(1)
    try:
        new_contribution = float(sys.argv[1])
    except ValueError:
        print("Erro: O valor do aporte deve ser um número.")
        sys.exit(1)

    # Chama a função com o valor do aporte fornecido
    calculate_and_update_contribution(csv_file_path, new_contribution)

    # Imprime o DataFrame atualizado para verificar as mudanças
    updated_df = pd.read_csv(csv_file_path)
    print(updated_df)
