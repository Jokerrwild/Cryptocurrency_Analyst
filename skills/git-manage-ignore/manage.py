import sys
import os

def manage_ignore(action, pattern):
    gitignore = '.gitignore'
    if not os.path.exists(gitignore):
        print(f'{gitignore} does not exist. Creating new.')
        with open(gitignore, 'w') as f: pass

    if action == 'list':
        with open(gitignore, 'r') as f: print(f.read())
    elif action == 'add':
        with open(gitignore, 'a') as f: f.write(f'\n{pattern}')
        print(f'Added {pattern} to {gitignore}')
    elif action == 'remove':
        with open(gitignore, 'r') as f: lines = f.readlines()
        with open(gitignore, 'w') as f:
            for line in lines:
                if line.strip() != pattern: f.write(line)
        print(f'Removed {pattern} from {gitignore}')

if __name__ == '__main__':
    manage_ignore(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)