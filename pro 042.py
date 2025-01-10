import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def best_district_for_rice_with_random_forest():
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

        # Add anomaly labels based on growth score
        threshold = district_growth['growth_score'].quantile(0.25)  # Set threshold for anomalies (e.g., lower 25%)
        district_growth['anomaly'] = (district_growth['growth_score'] < threshold).astype(int)  # 1 = anomaly, 0 = normal

        # Prepare data for Random Forest
        X = district_growth[['Temperature (°C)', 'Rainfall (mm)', 'Agricultural_Growth_Rate_%']]
        y = district_growth['anomaly']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Random Forest Classifier
        rf_model = RandomForestClassifier(random_state=42)
        rf_model.fit(X_train, y_train)

        # Use the model to classify all districts
        district_growth['predicted_anomaly'] = rf_model.predict(X)

        # Find the best district (normal district with the highest growth score)
        best_district_data = district_growth[district_growth['predicted_anomaly'] == 0]  # Filter normal districts
        best_district = best_district_data['growth_score'].idxmax()
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
    best_district_for_rice_with_random_forest()
