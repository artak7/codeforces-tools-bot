"""
Test script for HTML standings generation
Run this to test the HTML generation without starting the bot
"""

from codeforces.html_standings import generate_html_standings
from data.configs_reader import DIR

# Sample test data
contest_name = "Test Contest - КВАНТомания"

problem_list = [
    {'index': 'A', 'name': 'Вышивание с Диной'},
    {'index': 'B', 'name': 'Олимпиада по математике'},
    {'index': 'C', 'name': 'Плакат для лаборатории'},
    {'index': 'D', 'name': 'Спор о сумме'},
]

standings_data = [
    {
        'participant': 'Участник 46',
        'rank': 1,
        'solved': 4,
        'penalty': 195,
        'problems': [
            {'accepted': True, 'attempts': 1, 'time': 420},  # 00:07
            {'accepted': True, 'attempts': 3, 'time': 3360}, # 00:56
            {'accepted': True, 'attempts': 1, 'time': 900},  # 00:15
            {'accepted': True, 'attempts': 1, 'time': 1260}, # 00:21
        ]
    },
    {
        'participant': 'Участник 45',
        'rank': 2,
        'solved': 3,
        'penalty': 143,
        'problems': [
            {'accepted': True, 'attempts': 1, 'time': 1260},  # 00:21
            {'accepted': True, 'attempts': 1, 'time': 1560},  # 00:26
            {'accepted': True, 'attempts': 1, 'time': 300},   # 00:05
            {'accepted': False, 'attempts': 2, 'time': 0},
        ]
    },
    {
        'participant': 'Участник 47',
        'rank': 3,
        'solved': 3,
        'penalty': 97,
        'problems': [
            {'accepted': True, 'attempts': 1, 'time': 360},   # 00:06
            {'accepted': True, 'attempts': 1, 'time': 720},   # 00:12
            {'accepted': True, 'attempts': 1, 'time': 840},   # 00:14
            {'accepted': False, 'attempts': 0, 'time': 0},
        ]
    },
]

custom_names = {
    'Участник 46': 'Иван Иванов',
    'Участник 45': 'Петр Петров',
    'Участник 47': 'Мария Сидорова'
}

if __name__ == '__main__':
    print("Generating HTML standings...")
    
    # Generate without custom names
    html_original = generate_html_standings(
        contest_name=contest_name,
        standings_data=standings_data,
        problem_list=problem_list
    )
    
    with open(f'{DIR}/data/standings_original.html', 'w', encoding='utf-8') as f:
        f.write(html_original)
    print("✓ Generated standings_original.html (with anonymous names)")
    
    # Generate with custom names
    html_custom = generate_html_standings(
        contest_name=contest_name,
        standings_data=standings_data,
        problem_list=problem_list,
        custom_names=custom_names
    )
    
    with open(f'{DIR}/data/standings_custom.html', 'w', encoding='utf-8') as f:
        f.write(html_custom)
    print("✓ Generated standings_custom.html (with custom names)")
    
    print("\nOpen the HTML files in your browser to view the results!")
