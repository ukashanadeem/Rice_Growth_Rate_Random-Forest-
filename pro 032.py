import pandas as pd

def best_district_for_rice():
    # Load the dataset
    file_path = 'combined_district_weather_dataset.csv'
    data = pd.read_csv(file_path)

    # Ensure required columns exist
    required_columns = ['District', 'Temperature (°C)', 'Rainfall (mm)', 'Agricultural_Growth_Rate_%']
    if all(col in data.columns for col in required_columns):
        # Group by district and calculate mean values for relevant factors
        district_growth = data.groupby('District')[['Temperature (°C)', 'Rainfall (mm)', 'Agricultural_Growth_Rate_%']].mean()

        # Normalize each factor and calculate a growth score
        district_growth['growth_score'] = (
            district_growth['Temperature (°C)'].apply(lambda x: (x - data['Temperature (°C)'].min()) / (data['Temperature (°C)'].max() - data['Temperature (°C)'].min())) +
            district_growth['Rainfall (mm)'].apply(lambda x: (x - data['Rainfall (mm)'].min()) / (data['Rainfall (mm)'].max() - data['Rainfall (mm)'].min())) +
            district_growth['Agricultural_Growth_Rate_%'].apply(lambda x: (x - data['Agricultural_Growth_Rate_%'].min()) / (data['Agricultural_Growth_Rate_%'].max() - data['Agricultural_Growth_Rate_%'].min()))
        ) / 3  # Average the scores

        # Find the district with the highest growth score
        best_district = district_growth['growth_score'].idxmax()
        best_score = district_growth.loc[best_district, 'growth_score']

        print("\n-------------------------------------------------------------")
        print(f"Best District for Rice Growth: {best_district}")
        print(f"Growth Score: {best_score:.2f}")
        print("-------------------------------------------------------------")
    else:
        print("\n-------------------------------------------------------------")
        print("Dataset does not contain required columns: District, Temperature (°C), Rainfall (mm), Agricultural_Growth_Rate_%.")
        print("Please ensure the dataset has these columns to perform this analysis.")
        print("-------------------------------------------------------------")

# Call the function to display results
if __name__ == '__main__':
    best_district_for_rice()


