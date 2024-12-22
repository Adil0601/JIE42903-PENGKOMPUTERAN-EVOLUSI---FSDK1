
import matplotlib.pyplot as plt
import pandas as pd

# Project tasks and timelines
data = {
    'Task': [
        'Requirement Analysis',
        'Design & Prototyping',
        'Data Collection',
        'Exploratory Data Analysis',
        'Model Development (RNN+YOLO)',
        'System Integration',
        'Testing & Validation',
        'Deployment',
        'Final Documentation'
    ],
    'Start': [
        '2024-01-01', 
        '2024-01-16', 
        '2024-02-01', 
        '2024-03-01', 
        '2024-03-16', 
        '2024-04-16', 
        '2024-05-16', 
        '2024-06-16', 
        '2024-07-01'
    ],
    'End': [
        '2024-01-15', 
        '2024-01-31', 
        '2024-02-29', 
        '2024-03-15', 
        '2024-04-15', 
        '2024-05-15', 
        '2024-06-15', 
        '2024-06-30', 
        '2024-07-15'
    ]
}

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Convert Start and End columns to datetime
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Duration'] = (df['End'] - df['Start']).dt.days

# Create a figure for the Gantt chart
fig, ax = plt.subplots(figsize=(12, 8))

# Add the tasks to the Gantt chart
for i, task in enumerate(df['Task']):
    ax.barh(i, df['Duration'][i], left=df['Start'][i].toordinal(), color='skyblue', edgecolor='black')
    ax.text(df['Start'][i].toordinal(), i, f" {task}", va='center', ha='left', fontsize=10, color='black')

# Format the Gantt chart
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df['Task'])

# Generate xticks for weekly intervals
xticks = pd.date_range(df['Start'].min(), df['End'].max(), freq='W')
ax.set_xticks([x.toordinal() for x in xticks])
ax.set_xticklabels(xticks.strftime('%Y-%m-%d'), rotation=45, fontsize=8)

# Adjust the chart layout
ax.invert_yaxis()  # Invert y-axis for top-down order
ax.set_xlabel('Timeline')
ax.set_title('Gantt Chart for SITISMART Project', fontsize=14)

plt.tight_layout()
plt.show()
