import os
from github import Github
from datetime import datetime, timezone
import re

def get_latest_activities(github_token):
    g = Github(github_token)
    user = g.get_user()
    
    activities = []
    
    # Get latest repo activity
    for repo in user.get_repos(sort='pushed', direction='desc'):
        if not repo.fork:  # Skip forked repositories
            activities.append(f"🚀 Working on [{repo.name}]({repo.html_url})")
            break
    
    # Get latest commits
    for repo in user.get_repos():
        if not repo.fork:
            try:
                commits = repo.get_commits(author=user)
                if commits.totalCount > 0:
                    latest_commit = commits[0]
                    activities.append(f"📝 Latest commit: {latest_commit.commit.message[:50]}...")
                    break
            except:
                continue
    
    # Add learning activity (you could customize this based on repo topics or other metrics)
    activities.append("📚 Learning Python, Rust and Android Development")
    
    return activities[:3]  # Return top 3 activities

def update_readme(activities):
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Define the section pattern
    pattern = r'(## 🔥 Latest Activity\n)(?:.*\n)*?((?=##)|$)'
    
    # Create new activity section
    activity_section = '## 🔥 Latest Activity\n'
    for activity in activities:
        activity_section += f'- {activity}\n'
    
    # Replace the old section with new content
    new_content = re.sub(pattern, f'{activity_section}\n', content)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(new_content)

def main():
    token = os.environ.get('GH_TOKEN')
    if not token:
        raise ValueError("No GitHub token found!")
    
    activities = get_latest_activities(token)
    update_readme(activities)

if __name__ == '__main__':
    main()
