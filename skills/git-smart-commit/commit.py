import subprocess
import sys

def git_smart_commit(message):
    try:
        # Set persona identity
        subprocess.run(['git', 'config', 'user.name', 'Agent Zero'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'agent0@bunker.local'], check=True)
        
        # Stage all files
        subprocess.run(['git', 'add', '-A'], check=True)
        
        # Commit
        subprocess.run(['git', 'commit', '-m', message], check=True)
        print(f'Successfully committed changes: {message}')
    except subprocess.CalledProcessError as e:
        print(f'Git operation failed: {e}')

if __name__ == '__main__':
    msg = sys.argv[1] if len(sys.argv) > 1 else 'chore(agent): automated persona commit'
    git_smart_commit(msg)