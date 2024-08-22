import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = r'C:\Users\shubh\Downloads\^NSEI (1).csv'
df = pd.read_csv(file_path)

# Convert the Date column to datetime format and filter for Thursdays
df['Date'] = pd.to_datetime(df['Date'])
df_thursday = df[df['Date'].dt.day_name() == 'Thursday'].copy()

# Calculate absolute return, 10-period rolling standard deviation, and average
df_thursday['Abs_Return'] = df_thursday['Close'].pct_change().abs() * 100
df_thursday['Std_Dev'] = df_thursday['Abs_Return'].rolling(window=10).std()
df_thursday['Avg_Abs_Return'] = df_thursday['Abs_Return'].rolling(window=10).mean()

# Calculate the average ± 1 and 2 standard deviations
df_thursday['Avg_Abs_Return ± 1 Std_Dev'] = df_thursday['Avg_Abs_Return'] + df_thursday['Std_Dev']
df_thursday['Avg_Abs_Return ± 2 Std_Dev'] = df_thursday['Avg_Abs_Return'] + 2 * df_thursday['Std_Dev']
df_thursday['Avg_Abs_Return - 1 Std_Dev'] = df_thursday['Avg_Abs_Return'] - df_thursday['Std_Dev']
df_thursday['Avg_Abs_Return - 2 Std_Dev'] = df_thursday['Avg_Abs_Return'] - 2 * df_thursday['Std_Dev']

# Calculate the Close price range based on 1 and 2 Std Dev
df_thursday['+1 Std_Dev Range'] = df_thursday['Close'] * (1 + df_thursday['Std_Dev'] / 100)
df_thursday['-1 Std_Dev Range'] = df_thursday['Close'] * (1 - df_thursday['Std_Dev'] / 100)
df_thursday['+2 Std_Dev Range'] = df_thursday['Close'] * (1 + 2 * df_thursday['Std_Dev'] / 100)
df_thursday['-2 Std_Dev Range'] = df_thursday['Close'] * (1 - 2 * df_thursday['Std_Dev'] / 100)

# Add next week's close price and categorize based on Std Dev range
df_thursday['Next_Week_Close'] = df_thursday['Close'].shift(-1)
df_thursday['Check'] = df_thursday.apply(
    lambda row: 1 if row['-1 Std_Dev Range'] <= row['Next_Week_Close'] <= row['+1 Std_Dev Range'] 
    else 2 if row['-2 Std_Dev Range'] <= row['Next_Week_Close'] <= row['+2 Std_Dev Range'] 
    else False, axis=1
)

# Remove the first 10 rows and reset index
df_thursday_filtered = df_thursday.iloc[10:].reset_index(drop=True)

# Keep only relevant columns
final_columns = ['Date', 'Close', 'Abs_Return', 'Std_Dev', 'Avg_Abs_Return',
                 'Avg_Abs_Return ± 1 Std_Dev', 'Avg_Abs_Return ± 2 Std_Dev',
                 'Avg_Abs_Return - 1 Std_Dev', 'Avg_Abs_Return - 2 Std_Dev',
                 '+1 Std_Dev Range', '-1 Std_Dev Range', '+2 Std_Dev Range',
                 '-2 Std_Dev Range', 'Next_Week_Close', 'Check']

df_thursday_filtered = df_thursday_filtered[final_columns]

# Plot 1: Cumulative Success Rate Over Time
df_thursday_filtered['Cumulative_Success'] = (df_thursday_filtered['Check'] != False).cumsum()
df_thursday_filtered['Cumulative_Count'] = range(1, len(df_thursday_filtered) + 1)
df_thursday_filtered['Cumulative_Success_Rate'] = (df_thursday_filtered['Cumulative_Success'] / df_thursday_filtered['Cumulative_Count']) * 100

# Plot 2: Yearly Success Rate
df_thursday_filtered['Year'] = df_thursday_filtered['Date'].dt.year
yearly_success = df_thursday_filtered.groupby('Year')['Check'].apply(lambda x: (x != False).mean() * 100)

plt.figure(figsize=(12, 6))
yearly_success.plot(kind='bar', color='skyblue')
plt.xlabel('Year')
plt.ylabel('Success Rate (%)')
plt.title('Yearly Success Rate')
plt.grid(axis='y')
plt.show()

# Calculate upcoming week's range
last_row = df_thursday_filtered.iloc[-1]
upcoming_week_range = {
    "+1 Std Dev Range": last_row['+1 Std_Dev Range'],
    "-1 Std Dev Range": last_row['-1 Std_Dev Range'],
    "+2 Std Dev Range": last_row['+2 Std_Dev Range'],
    "-2 Std Dev Range": last_row['-2 Std_Dev Range'],
}

upcoming_week_range
