import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = r'C:\Users\shubh\Downloads\pnl_15_08_2024.csv'
pnl_data = pd.read_csv(file_path)

# Remove the Unrealized Profit/Loss column
pnl_data_filtered = pnl_data.drop(columns=['Unrealized Profit/Loss  (₹)'])
# Separate profits and losses
profits = pnl_data_filtered[pnl_data_filtered['Realized Profit/Loss  (₹)'] > 0]['Realized Profit/Loss  (₹)']
losses = pnl_data_filtered[pnl_data_filtered['Realized Profit/Loss  (₹)'] < 0]['Realized Profit/Loss  (₹)']

# Calculate key statistics
total_profit = profits.sum()
total_loss = losses.sum()
total_profit_trades = len(profits)
total_loss_trades = len(losses)
total_trades = len(pnl_data_filtered)

# Correctly calculate accuracy
correct_accuracy = total_profit_trades / (total_profit_trades + total_loss_trades)

# Average profit and loss
average_profit_recalculated = profits.mean()
average_loss_recalculated = losses.mean()

# Risk to reward ratio and profit/loss ratio
correct_risk_to_reward_ratio = -average_profit_recalculated / average_loss_recalculated
correct_profit_loss_ratio = -total_profit / total_loss

# Plot the results
plt.figure(figsize=(14, 8))

plt.subplot(1, 2, 1)
plt.boxplot(losses, vert=True, patch_artist=True, boxprops=dict(facecolor="lightcoral"))
plt.title('Distribution of Losses')
plt.ylabel('Realized Loss (₹)')
plt.figtext(0.25, 0.92, f'Total Loss: ₹{total_loss:.2f}\nNumber of Losing Trades: {total_loss_trades}', ha='center', fontsize=12, color='red')

plt.subplot(1, 2, 2)
plt.boxplot(profits, vert=True, patch_artist=True, boxprops=dict(facecolor="lightgreen"))
plt.title('Distribution of Profits')
plt.ylabel('Realized Profit (₹)')
plt.figtext(0.75, 0.92, f'Total Profit: ₹{total_profit:.2f}\nNumber of Profitable Trades: {total_profit_trades}', ha='center', fontsize=12, color='green')

# Add the metrics at the top of the chart with proper spacing
plt.suptitle(
    f'Profit and Loss Analysis\n'
    f'Accuracy: {correct_accuracy:.2%} | Risk to Reward: {correct_risk_to_reward_ratio:.2f} | Profit/Loss Ratio: {correct_profit_loss_ratio:.2f}\n'
    f'Average Profit: ₹{average_profit_recalculated:.2f} | Average Loss: ₹{average_loss_recalculated:.2f} \n '
    f'Net Profit: ₹ {total_profit+total_loss}',
    fontsize=14, y=1.10)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
