# --- Voice Setup ---
import pyttsx3
import threading
import queue

# Speech queue and worker thread for serialized voice output
speech_queue = queue.Queue()

def speech_worker():
    engine = pyttsx3.init()
    zoe_voice_id = None
    for v in engine.getProperty('voices'):
        if 'zoe' in v.name.lower():
            zoe_voice_id = v.id
            break
    if zoe_voice_id:
        engine.setProperty('voice', zoe_voice_id)
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()
# --- Imports ---
import os
import emoji
import subprocess


# --- Helper Functions ---
def talk(text):
    speech_queue.put(text)

def github_repo_exists(repo_name):
    talk("Checking if the repository exists on GitHub.")
    try:
        result = subprocess.run(
            ["gh", "repo", "view", f"99ashr/{repo_name}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False

def get_and_announce_repo_name():
    talk("Please enter the name of your repository.")
    # Wait for voice to finish before showing input
    speech_queue.join()
    repo_name = input(emoji.emojize("Enter the name of your repository here!:pensive_face:\nHere!:\t"))
    if not repo_name.strip():
        repo_name = os.path.basename(os.getcwd())
        talk(f"No name entered. Repository name will be saved as {repo_name} by default.")
    else:
        talk(f"Repository name will be saved as {repo_name}.")
    # Sanitize repo name for GitHub (replace spaces with dashes)
    safe_repo_name = repo_name.replace(' ', '-')
    if safe_repo_name != repo_name:
        talk(f"Repository name for GitHub will be {safe_repo_name}.")
    return safe_repo_name

def auto_gitignore_and_bfg_large_files():
    pass

def current_dir():
    return os.getcwd()

def writefun(repo_name):
    pass

def creating_md(repo_name):
    talk("Creating README file for you.")
    with open("README.md", "w") as f:
        f.write(f"# {repo_name}\n")
    talk("README created.")

def git_init():
    talk("Initializing your git repository.")
    os.system("git init")
    talk("Git repository initialized.")

def git_add():
    talk("Adding files to commit.")
    os.system("git add .")
    talk("Files added.")

def git_status():
    pass

def git_commit():
    # Check if there's anything to commit first
    status_result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not status_result.stdout.strip():
        talk("Nothing new to commit. Your working tree is already clean and all changes have been committed previously.")
        return
    talk("How would you like to remember this commit?")
    # Wait for voice to finish before showing input
    speech_queue.join()
    print(emoji.emojize("Ready To Commit Your MESS...?:expressionless_face:"))
    commit_msg = input(emoji.emojize("Please enter your commit message here:drooling_face:\n message:"))
    if not commit_msg.strip():
        commit_msg = "Auto-commit from auto_git"
    talk("It might take some time, we are committing your files.")
    commit = f'git commit -m "{commit_msg}"'
    result = os.system(commit)
    if result == 0:
        talk("Commit successful. Your changes have been saved.")
    else:
        talk("Commit failed. Please check for errors.")

def connect_remote(repo_name):
    talk("Connecting to your remote GitHub repository.")
    print(emoji.emojize("Connecting to your remote directory...:lying_face:"))
    remote_url = f"https://github.com/99ashr/{repo_name}.git"
    remote_check = os.system("git remote get-url origin > /dev/null 2>&1")
    if remote_check != 0:
        os.system(f"git remote add origin {remote_url}")
    else:
        os.system(f"git remote set-url origin {remote_url}")
    talk("Remote repository set.")

def git_push(repo_name):
    talk("Pushing your changes to GitHub.")
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    except Exception:
        branch = "main"
    push_cmd = f"git push -u origin {branch}"
    result = subprocess.run(push_cmd, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    if result.returncode == 0:
        if "Everything up-to-date" in output or "Everything up to date" in output:
            talk("Everything is up to date. No new changes to push.")
        else:
            talk("Push to GitHub successful.")
    else:
        # Check if it's just "up to date" message in stderr
        if "Everything up-to-date" in output or "Everything up to date" in output:
            talk("Everything is up to date. No new changes to push.")
        elif "rejected" in output and "fetch first" in output:
            talk("Push rejected. Remote has changes. You may need to pull first.")
            print("Push rejected. Remote has changes you don't have locally.")
        else:
            talk("Push failed. Please check for errors.")
            print(f"Push failed. Output: {output}")

def run_full_workflow(repo_name, rerun=False):
    if rerun:
        talk("Restarting the auto git workflow after repository creation.")
    writefun(repo_name)
    creating_md(repo_name)
    git_init()
    git_add()
    git_status()
    git_commit()
    git_status()
    connect_remote(repo_name)
    if not rerun:
        git_push(repo_name)
    else:
        talk("Auto git workflow complete after repository creation.")

# --- Main Guard ---
if __name__ == "__main__":
    try:
        talk("Starting the auto git workflow.")
        auto_gitignore_and_bfg_large_files()
        current_dir()
        repo_name = get_and_announce_repo_name()
        # Always ensure git init, README, add, and commit before creating repo
        if not os.path.exists('.git'):
            talk("Initializing a new git repository in this directory.")
            os.system('git init')
        creating_md(repo_name)
        git_add()
        git_commit()
        # Now check if repo exists on GitHub, if not, create it (without --push)
        if not github_repo_exists(repo_name):
            talk(f"Repository {repo_name} does not exist on GitHub. Creating it now.")
            create_cmd = f"gh repo create '{repo_name}' --public --source=."
            create_result = subprocess.run(create_cmd, shell=True)
            if create_result.returncode == 0:
                talk(f"Repository {repo_name} created on GitHub.")
            else:
                talk(f"Failed to create repository {repo_name} on GitHub. Please check your GitHub CLI authentication and try again.")
                print(f"Failed to create repository {repo_name} on GitHub.")
                exit(1)
        connect_remote(repo_name)
        git_push(repo_name)
        talk("Auto git workflow complete.")
    except Exception as e:
        talk("oh oo! an error occurred")
        print(f"Error: {e}")
    finally:
        # Wait for all voice messages to finish before exiting
        speech_queue.join()
