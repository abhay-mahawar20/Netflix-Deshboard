import pandas as pd
import matplotlib.pyplot as plt

# Load data

df = pd.read_csv('netflix_titles.csv')

# Clean and prepare data

df = df.drop_duplicates()
df['country'] = df['country'].fillna('Unknown')
df['director'] = df['director'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Unknown')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year

# Prepare dashboard metrics
content_type = df['type'].value_counts()
top_countries = df['country'].value_counts().head(10)
top_genres = df['listed_in'].dropna().str.split(', ').explode().value_counts().head(10)
yearly = df['year_added'].dropna().value_counts().sort_index()

# Calculate KPI metrics
total_content = len(df)
total_movies = (df['type'] == 'Movie').sum()
total_shows = (df['type'] == 'TV Show').sum()
avg_year = int(df['release_year'].mean())
most_common_genre = df['listed_in'].dropna().str.split(', ').explode().value_counts().index[0]
total_countries = df['country'].nunique()

# Create comprehensive dashboard with KPI cards and charts
fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)

fig.patch.set_facecolor('#f8f9fa')
fig.suptitle('Netflix Content Analysis Dashboard', fontsize=24, fontweight='bold', y=0.995)

# KPI Cards Row
kpi_data = [
    ('Total Content', f'{total_content:,}', '#FF6B6B'),
    ('Movies', f'{total_movies:,}', '#4C78A8'),
    ('TV Shows', f'{total_shows:,}', '#F58518'),
    ('Avg Release Year', f'{avg_year}', '#54A24B'),
    ('Top Genre', f'{most_common_genre}', '#72B7B2'),
    ('Countries', f'{total_countries}', '#E45756')
]

# Create KPI cards in first row
for idx, (title, value, color) in enumerate(kpi_data):
    ax = fig.add_subplot(gs[0, idx % 3])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Draw card background
    rect = plt.Rectangle((0.3, 1), 9.4, 8, linewidth=3, edgecolor=color, facecolor='white')
    ax.add_patch(rect)
    
    # Add title
    ax.text(5, 7.5, title, fontsize=12, fontweight='bold', ha='center', va='center', color='#333333')
    
    # Add value
    ax.text(5, 4, value, fontsize=26, fontweight='bold', ha='center', va='center', color=color)
    
    if idx == 2:
        # Move to second row after 3 cards
        pass

# Create second row for first 3 KPI cards (already added)
for idx in range(3, 6):
    ax = fig.add_subplot(gs[1, idx - 3])
    title, value, color = kpi_data[idx]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    rect = plt.Rectangle((0.3, 1), 9.4, 8, linewidth=3, edgecolor=color, facecolor='white')
    ax.add_patch(rect)
    
    ax.text(5, 7.5, title, fontsize=12, fontweight='bold', ha='center', va='center', color='#333333')
    ax.text(5, 4, value, fontsize=26, fontweight='bold', ha='center', va='center', color=color)

# Charts Row 1 (spanning row 2)
# Content Type Distribution
ax1 = fig.add_subplot(gs[2, 0])
colors_bar = ['#4C78A8', '#F58518']
bars = ax1.bar(content_type.index, content_type.values, color=colors_bar, edgecolor='black', linewidth=1.5)
ax1.set_title('Content Type Distribution', fontsize=13, fontweight='bold')
ax1.set_ylabel('Count', fontsize=11)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height, f'{int(height):,}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Top Countries
ax2 = fig.add_subplot(gs[2, 1:])
ax2.barh(top_countries.index[::-1], top_countries.values[::-1], color='#72B7B2', edgecolor='black', linewidth=1)
ax2.set_title('Top 10 Countries', fontsize=13, fontweight='bold')
ax2.set_xlabel('Number of Titles', fontsize=11)
ax2.grid(axis='x', alpha=0.3, linestyle='--')
for i, v in enumerate(top_countries.values[::-1]):
    ax2.text(v, i, f' {int(v):,}', va='center', fontweight='bold')

# Charts Row 2 (spanning row 3)
# Top Genres
ax3 = fig.add_subplot(gs[3, :2])
bars = ax3.bar(range(len(top_genres)), top_genres.values, color='#54A24B', edgecolor='black', linewidth=1)
ax3.set_xticks(range(len(top_genres)))
ax3.set_xticklabels(top_genres.index, rotation=45, ha='right')
ax3.set_title('Top 10 Genres', fontsize=13, fontweight='bold')
ax3.set_ylabel('Count', fontsize=11)
ax3.grid(axis='y', alpha=0.3, linestyle='--')
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height, f'{int(height):,}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

# Yearly Trend
ax4 = fig.add_subplot(gs[3, 2])
ax4.plot(yearly.index, yearly.values, marker='o', color='#E45756', linewidth=2.5, markersize=6)
ax4.fill_between(yearly.index, yearly.values, alpha=0.3, color='#E45756')
ax4.set_title('Content Added Over Years', fontsize=13, fontweight='bold')
ax4.set_xlabel('Year', fontsize=11)
ax4.set_ylabel('Count', fontsize=11)
ax4.grid(alpha=0.3, linestyle='--')

plt.savefig('netflix_comprehensive_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
plt.close(fig)
