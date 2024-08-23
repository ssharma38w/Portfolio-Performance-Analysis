import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the CSV file
file_path= r'C:\Users\shubh\Downloads\DR01540_Global P&L Statement_23_08_2024 (1).csv'  # Replace with your file path
n=1
# Fixed cost analysis
actual_final_profit_after_fixed_cost = 29169.04*n
actual_blocked_funds = 320000*n
start_date = datetime(2024, 4, 1)
end_date = datetime(2024, 8, 22)

# Filter the relevant columns  # Replace with your file path
data = pd.read_csv(file_path)
data = data[data['Realized Profit/Loss  (₹)'] != 0]
data['Realized Profit/Loss  (₹)'] = data['Realized Profit/Loss  (₹)']*n
# Filter the relevant columns
realized_pl = data['Realized Profit/Loss  (₹)']

# Create separate data for profit and loss
profit_data = realized_pl[realized_pl > 0]
loss_data = realized_pl[realized_pl < 0]

# Current stats
accuracy = len(profit_data) / (len(profit_data) + len(loss_data)) * 100
average_profit = profit_data.mean()
average_loss = loss_data.mean()
profit_loss_ratio = -average_profit / average_loss
risk_to_reward = 1/profit_loss_ratio
net_profit = profit_data.sum() + loss_data.sum()

# Total trades and average trades per week calculation
total_days = (end_date - start_date).days
total_weeks = total_days / 7
total_trades = len(realized_pl)
average_trades_per_week = total_trades / total_weeks



total_cost = net_profit - actual_final_profit_after_fixed_cost
average_cost_per_trade = total_cost / total_trades

# Projections till March 31, 2025
weeks_till_march_31_2025 = (datetime(2025, 3, 31) - end_date).days / 7
projected_trades_till_march = total_trades + (weeks_till_march_31_2025 * average_trades_per_week)
projected_profitable_trades = projected_trades_till_march * (accuracy / 100)
projected_losing_trades = projected_trades_till_march * (1 - accuracy / 100)
projected_total_profit = projected_profitable_trades * average_profit
projected_total_loss = projected_losing_trades * average_loss
projected_gross_profit_corrected = projected_total_profit + projected_total_loss
projected_total_cost = projected_trades_till_march * average_cost_per_trade
projected_net_profit_after_cost_corrected = projected_gross_profit_corrected - projected_total_cost

# Return and Annualized Return Calculations
trading_period_days = total_days
actual_return_before_cost = (net_profit / actual_blocked_funds) * 100
actual_return_after_cost = (actual_final_profit_after_fixed_cost / actual_blocked_funds) * 100
annualized_return_before_cost = (1 + net_profit / actual_blocked_funds) ** (365 / trading_period_days) - 1
annualized_return_after_cost = (1 + actual_final_profit_after_fixed_cost / actual_blocked_funds) ** (365 / trading_period_days) - 1

# Step 1: Show the chart with box plots
def plot_box_plots():
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # Box plot for losses
    axes[0].boxplot(loss_data, vert=True, patch_artist=True, boxprops=dict(facecolor="lightcoral"))
    axes[0].set_title('Distribution of Losses', fontsize=14)
    axes[0].set_ylabel('Realized Loss (₹)', fontsize=12)
#     axes[0].text(1, min(loss_data) * 0.75, f'Total Loss: ₹{loss_data.sum():,.2f}\nNumber of Losing Trades: {len(loss_data)}', 
#                  ha='center', color='red', fontsize=12)

    # Box plot for profits
    axes[1].boxplot(profit_data, vert=True, patch_artist=True, boxprops=dict(facecolor="lightgreen"))
    axes[1].set_title('Distribution of Profits', fontsize=14)
    axes[1].set_ylabel('Realized Profit (₹)', fontsize=12)
#     axes[1].text(1, min(profit_data) * 0.75, f'Total Profit: ₹{profit_data.sum():,.2f}\nNumber of Profitable Trades: {len(profit_data)}', 
#                  ha='center', color='green', fontsize=12)

    plt.suptitle(f'Profit and Loss Analysis\n'
                 f'Accuracy: {accuracy:.2f}% | Risk to Reward: {risk_to_reward:.2f} | Profit/Loss Ratio: {profit_loss_ratio:.2f}\n'
                 f'Average Profit: ₹{average_profit:,.2f} | Average Loss: ₹{average_loss:,.2f} | Net Profit: ₹{net_profit:,.2f}\n\n'
                 f'Total Profit: ₹{profit_data.sum():,.2f} | Number of Profitable Trades: {len(profit_data)}\n'
                 f'Total Loss: ₹{loss_data.sum():,.2f} | Number of Losing Trades: {len(loss_data)}',
                 fontsize=16, y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    plt.show()

# Step 2: Chart for profit before and after fixed cost
def plot_profit_comparison():
    labels = ['Profit Before Cost', 'Profit After Cost']
    values = [net_profit, actual_final_profit_after_fixed_cost]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['skyblue', 'orange'])
    plt.ylabel('Profit (₹)')
    plt.title('Comparison of Profit Before and After Fixed Cost')

    # Adding value labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'₹{height:,.2f}', ha='center', va='bottom', fontsize=12)

    plt.show()

# Step 3: Chart for return and annualized return before and after fixed cost
def plot_return_comparison():
    labels = ['Return Before Cost', 'Return After Cost', 'Annualized Return Before Cost', 'Annualized Return After Cost']
    values = [actual_return_before_cost, actual_return_after_cost, annualized_return_before_cost * 100, annualized_return_after_cost * 100]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, values, color=['skyblue', 'orange', 'skyblue', 'orange'])
    plt.ylabel('Percentage (%)')
    plt.title('Comparison of Return and Annualized Return Before and After Fixed Cost')

    # Adding value labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.2f}%', ha='center', va='bottom', fontsize=12)

    plt.show()

# Step 4: Chart for expected earnings before and after fixed cost until March 31, 2025
def plot_expected_earnings_comparison():
    labels = ['Expected Profit Before Cost', 'Expected Profit After Cost']
    values = [projected_gross_profit_corrected, projected_net_profit_after_cost_corrected]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['skyblue', 'orange'])
    plt.ylabel('Profit (₹)')
    plt.title('Expected Earnings Until March 31, 2025 Before and After Fixed Cost')

    # Adding value labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'₹{height:,.2f}', ha='center', va='bottom', fontsize=12)

    plt.show()

# Executing all steps to show the complete analysis

print(round(average_trades_per_week,1),total_trades,round(average_cost_per_trade,2),net_profit-actual_final_profit_after_fixed_cost)
# Step 1: Box plot of profit and loss
plot_box_plots()

# Step 2: Profit before and after fixed cost
plot_profit_comparison()

# Step 3: Return and annualized return before and after fixed cost
plot_return_comparison()

# Step 4: Calculate expected earnings until March 31, 2025
plot_expected_earnings_comparison()
