import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def load_abundance_data(file):
    """
    Carrega o arquivo de abundância com dados taxonômicos e amostrais.
    """
    return pd.read_csv(file)

def calculate_productivity_factors():
    """
    Define as produtividades de cada fazenda e calcula os fatores de ponderação.
    """
    productivity = {
        'F3': 3500,
        'F4': 9500, 
        'F5': 7500,
        'F6': 11000
    }
    
    mean_productivity = np.mean(list(productivity.values()))
    
    productivity_factors = {}
    for farm, prod in productivity.items():
        factor = prod / mean_productivity
        productivity_factors[farm] = factor
        print(f"{farm}: {prod} kg/ha | Fator: {factor:.4f} | Peso: {((factor-1)*100):+.1f}%")
    
    return productivity_factors, mean_productivity

def calculate_species_variation(df):
    """
    Calcula a variação média (Depois - Antes) para cada espécie em cada fazenda.
    """
    taxonomy_cols = ['Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
    sample_cols = [col for col in df.columns if col not in taxonomy_cols]
    
    farms = ['F3', 'F4', 'F5', 'F6']
    results = []
    
    print(f"Processando {len(df)} espécies...")
    
    for idx, (_, row) in enumerate(df.iterrows()):
        if idx > 0 and idx % 100 == 0:
            print(f"  Processadas {idx} espécies...")
            
        species_name = row['Species']
        species_data = {
            'Species': species_name,
            'Phylum': row['Phylum'],
            'Class': row['Class'],
            'Order': row['Order'],
            'Family': row['Family'],
            'Genus': row['Genus']
        }
        
        species_present_somewhere = False  # Flag para verificar se espécie tem dados
        
        for farm in farms:
            # Colunas de cada fazenda (Antes = A, Depois = B)
            antes_cols = [col for col in sample_cols if col.startswith(f'{farm}A')]
            depois_cols = [col for col in sample_cols if col.startswith(f'{farm}B')]
            
            if antes_cols and depois_cols:
                # Média das triplicatas antes e depois
                antes_mean = pd.to_numeric(row[antes_cols], errors='coerce').mean()
                depois_mean = pd.to_numeric(row[depois_cols], errors='coerce').mean()
                
                # Verifica se tem dados válidos
                if not (pd.isna(antes_mean) and pd.isna(depois_mean)):
                    species_present_somewhere = True
                
                # Substitui NaN por 0
                antes_mean = 0 if pd.isna(antes_mean) else antes_mean
                depois_mean = 0 if pd.isna(depois_mean) else depois_mean
                
                # Variação absoluta e relativa
                variation_abs = depois_mean - antes_mean
                
                # Variação relativa (evita divisão por zero)
                if antes_mean > 0:
                    variation_rel = (depois_mean - antes_mean) / antes_mean
                else:
                    # Se antes era 0 e depois > 0, considera como aparecimento (100% de aumento)
                    variation_rel = 1.0 if depois_mean > 0 else 0.0
                
                species_data[f'{farm}_antes_mean'] = antes_mean
                species_data[f'{farm}_depois_mean'] = depois_mean
                species_data[f'{farm}_variation_abs'] = variation_abs
                species_data[f'{farm}_variation_rel'] = variation_rel
                species_data[f'{farm}_present'] = 1 if (antes_mean > 0 or depois_mean > 0) else 0
            else:
                # Espécie não está presente nesta fazenda
                species_data[f'{farm}_antes_mean'] = 0
                species_data[f'{farm}_depois_mean'] = 0
                species_data[f'{farm}_variation_abs'] = 0
                species_data[f'{farm}_variation_rel'] = 0
                species_data[f'{farm}_present'] = 0
        
        # SEMPRE adiciona a espécie, mesmo que não tenha dados em nenhuma fazenda
        results.append(species_data)
    
    print(f"✓ Todas as {len(results)} espécies processadas")
    return pd.DataFrame(results)

def calculate_productivity_weighted_score(variations_df, productivity_factors):
    """
    Calcula o score ponderado pela produtividade para cada espécie.
    """
    farms = ['F3', 'F4', 'F5', 'F6']
    results = []
    
    print(f"Calculando scores para {len(variations_df)} espécies...")
    
    for idx, (_, row) in enumerate(variations_df.iterrows()):
        if idx > 0 and idx % 100 == 0:
            print(f"  Scores calculados para {idx} espécies...")
            
        species_scores = []
        species_weights = []
        farms_with_data = []
        
        for farm in farms:
            # Verifica se a espécie tem dados nesta fazenda (antes ou depois > 0)
            if row[f'{farm}_present'] == 1:
                variation = row[f'{farm}_variation_rel']
                productivity_factor = productivity_factors[farm]
                
                # Score ponderado: variação × fator de produtividade
                weighted_score = variation * productivity_factor
                species_scores.append(weighted_score)
                species_weights.append(productivity_factor)
                farms_with_data.append(farm)
        
        # SEMPRE processa a espécie, mesmo sem dados
        if species_scores:
            # Score final: média ponderada dos scores das fazendas onde a espécie está presente
            final_score = np.average(species_scores, weights=species_weights)
            
            # Estatísticas adicionais
            n_farms_present = len(species_scores)
            max_score = max(species_scores)
            min_score = min(species_scores)
            std_score = np.std(species_scores) if len(species_scores) > 1 else 0
            
        else:
            # Espécie sem dados em nenhuma fazenda
            final_score = 0
            n_farms_present = 0
            max_score = 0
            min_score = 0
            std_score = 0
        
        result = {
            'Species': row['Species'],
            'Phylum': row['Phylum'],
            'Class': row['Class'],
            'Order': row['Order'],
            'Family': row['Family'],
            'Genus': row['Genus'],
            'Productivity_Weighted_Score': final_score,
            'N_Farms_Present': n_farms_present,
            'Max_Farm_Score': max_score,
            'Min_Farm_Score': min_score,
            'Score_Std': std_score,
            'Farms_With_Data': ', '.join(farms_with_data) if farms_with_data else 'None'
        }
        
        # Adiciona os scores individuais por fazenda (SEMPRE, mesmo que NaN)
        for farm in farms:
            if row[f'{farm}_present'] == 1:
                variation = row[f'{farm}_variation_rel']
                weighted_score = variation * productivity_factors[farm]
                result[f'{farm}_Score'] = weighted_score
                result[f'{farm}_Variation_Rel'] = variation
                result[f'{farm}_Antes_Mean'] = row[f'{farm}_antes_mean']
                result[f'{farm}_Depois_Mean'] = row[f'{farm}_depois_mean']
            else:
                result[f'{farm}_Score'] = 0  # Era np.nan, agora é 0
                result[f'{farm}_Variation_Rel'] = 0  # Era np.nan, agora é 0
                result[f'{farm}_Antes_Mean'] = 0
                result[f'{farm}_Depois_Mean'] = 0
        
        results.append(result)
    
    print(f"✓ Scores calculados para todas as {len(results)} espécies")
    return pd.DataFrame(results)

def interpret_results(results_df):
    """
    Interpreta os resultados e adiciona classificações.
    """
    results_df = results_df.copy()
    
    # Classifica o impacto na produtividade
    def classify_impact(score):
        if score > 0.1:
            return "Alto Impacto Positivo"
        elif score > 0.05:
            return "Moderado Impacto Positivo"
        elif score > 0:
            return "Baixo Impacto Positivo"
        elif score > -0.05:
            return "Baixo Impacto Negativo"
        elif score > -0.1:
            return "Moderado Impacto Negativo"
        else:
            return "Alto Impacto Negativo"
    
    results_df['Impact_Classification'] = results_df['Productivity_Weighted_Score'].apply(classify_impact)
    
    # Ordena por score (mais impactantes primeiro)
    results_df = results_df.sort_values('Productivity_Weighted_Score', ascending=False)
    
    return results_df

def generate_summary_stats(results_df):
    """
    Gera estatísticas resumo dos resultados.
    """
    print("\n" + "="*80)
    print("RESUMO ESTATÍSTICO DA ANÁLISE")
    print("="*80)
    
    total_species = len(results_df)
    positive_impact = len(results_df[results_df['Productivity_Weighted_Score'] > 0])
    negative_impact = len(results_df[results_df['Productivity_Weighted_Score'] < 0])
    
    print(f"Total de espécies analisadas: {total_species}")
    print(f"Espécies com impacto positivo: {positive_impact} ({positive_impact/total_species*100:.1f}%)")
    print(f"Espécies com impacto negativo: {negative_impact} ({negative_impact/total_species*100:.1f}%)")
    
    print(f"\nTOP 10 ESPÉCIES COM MAIOR IMPACTO POSITIVO:")
    top_positive = results_df[results_df['Productivity_Weighted_Score'] > 0].head(10)
    if len(top_positive) > 0:
        for i, (_, row) in enumerate(top_positive.iterrows(), 1):
            print(f"{i:2d}. {row['Species'][:50]:<50} | Score: {row['Productivity_Weighted_Score']:+.4f}")
    else:
        print("Nenhuma espécie com impacto positivo encontrada.")
    
    print(f"\nTOP 10 ESPÉCIES COM MAIOR IMPACTO NEGATIVO:")
    negative_species = results_df[results_df['Productivity_Weighted_Score'] < 0]
    if len(negative_species) > 0:
        top_negative = negative_species.tail(10).iloc[::-1]  # Inverte para mostrar os mais negativos primeiro
        for i, (_, row) in enumerate(top_negative.iterrows(), 1):
            print(f"{i:2d}. {row['Species'][:50]:<50} | Score: {row['Productivity_Weighted_Score']:+.4f}")
    else:
        print("Nenhuma espécie com impacto negativo encontrada.")
    
    print(f"\nESPÉCIES SEM DADOS (Score = 0):")
    zero_species = results_df[results_df['Productivity_Weighted_Score'] == 0]
    print(f"Total: {len(zero_species)} espécies")

def main():
    print("Iniciando análise de produtividade ponderada por abundância bacteriana...")
    print("="*80)
    
    # 1. Carrega os dados
    input_file = 'abundance_data.csv'
    try:
        df = load_abundance_data(input_file)
        print(f"✓ Dados carregados: {len(df)} espécies, {len(df.columns)-6} amostras")
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo {input_file} não encontrado!")
        return
    
    # 2. Calcula fatores de produtividade
    print(f"\nCalculando fatores de produtividade:")
    productivity_factors, mean_prod = calculate_productivity_factors()
    print(f"Produtividade média: {mean_prod:.0f} kg/ha")
    
    # 3. Calcula variações das espécies
    print(f"\nCalculando variações de abundância por espécie e fazenda...")
    variations_df = calculate_species_variation(df)
    print(f"✓ Variações calculadas para {len(variations_df)} espécies")
    
    # 4. Calcula scores ponderados
    print(f"\nCalculando scores ponderados pela produtividade...")
    results_df = calculate_productivity_weighted_score(variations_df, productivity_factors)
    print(f"✓ Scores calculados para {len(results_df)} espécies")
    
    # 5. Interpreta resultados
    results_df = interpret_results(results_df)
    
    # 6. Salva resultados COMPLETOS
    output_file = 'productivity_weighted_analysis.csv'
    results_df.to_csv(output_file, index=False)
    print(f"✓ Resultados COMPLETOS salvos em: {output_file}")
    print(f"✓ Todas as {len(results_df)} espécies incluídas no arquivo CSV")
    
    # 7. Gera resumo estatístico (apenas para visualização)
    generate_summary_stats(results_df)
    
    print(f"\n{'='*80}")
    print("ANÁLISE CONCLUÍDA!")
    print(f"Arquivo de saída: {output_file}")
    print("="*80)

if __name__ == '__main__':
    main()