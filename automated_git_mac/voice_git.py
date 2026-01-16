import os
import emoji
import pickle
import pyttsx3

# &Create Object and Set voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')  # getting details of current voice
# On macOS, voice index 1 may not be female; fallback to index 0 if out of range
try:
    engine.setProperty('voice', voices[1].id)
except IndexError:
    engine.setProperty('voice', voices[0].id)

all_repos = []

def talk(talk):
    engine.say(talk)
    engine.runAndWait()


# Default repo name to current folder if left blank
import os
def get_default_repo_name():
    return os.path.basename(os.getcwd())

talk("Please enter the name of your repository")
repo_name = input(
    emoji.emojize(
        "Enter the name of your repository here!:pensive_face:\nHere!:\t")
)
if not repo_name.strip():
    repo_name = get_default_repo_name()
    print(f"No name entered. Using current folder name as repo name: {repo_name}")

def writefun():
    with open("myRepos.txt", "ab") as filehandle:
        pickle.dump(repo_name, filehandle)

def readfun():
    with open("myRepos.txt", "rb") as filehandle:
        try:
            while True:
                all_repos.append(pickle.load(filehandle))
        except EOFError:
            pass
        return all_repos[-1]

def current_dir():
    return os.getcwd()

def creating_md():
    print("Creating README File for you!")
    print(emoji.emojize("\nPlease Wait...:slightly_smiling_face:"))
    os.system(f"echo '# {repo_name}'>README.md")
    print(
        emoji.emojize(
            "\nCreated README.md successfully for you!:smiling_face_with_halo:"
        )
    )

def git_init():
    talk("Initializing your repository")
    print(
        emoji.emojize(
            "\nInitializing your repository...:smiling_face_with_smiling_eyes:"
        )
    )
    os.system("git init")

def git_add():
    talk("Adding files to commit")
    print(emoji.emojize("\n Initializing Git Add Command for you...:smiling_face:"))
    os.system("git add .")

def git_status():
    talk("These files are added")
    print(emoji.emojize("Here's the status of this REPO...:face_savoring_food:"))
    os.system("git status")

def git_commit():
    talk("Ready To Commit")
    print(emoji.emojize("Ready To Commit Your MESS...?:expressionless_face:"))
    talk("Please enter your commit message")
    commit_msg = input(
        emoji.emojize(
            "Please enter your commit message here:drooling_face:\n message:")
    )
    if not commit_msg.strip():
        commit_msg = "Auto-commit from auto_git"
    commit = f'git commit -m "{commit_msg}"'
    os.system(commit)

user_repo_link = "https://github.com/99ashr/"
remote = "git remote add origin"

def connect_remote():
    talk("Connecting to your remote directory")
    print(emoji.emojize("Connecting to your remote directory...:lying_face:"))
    # Check if remote 'origin' exists
    remote_url = f"{user_repo_link}{repo_name}.git"
    remote_check = os.system("git remote get-url origin > /dev/null 2>&1")
    if remote_check != 0:
        os.system(f"git remote add origin {remote_url}")
    else:
        os.system(f"git remote set-url origin {remote_url}")

def git_push():
    talk("We're good to go.")
    # Get current branch name
    import subprocess
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    except Exception:
        branch = "main"
    os.system(f"git push -u origin {branch}")

if __name__ == "__main__":
    current_dir()
    if repo_name == "":
        try:
            repo_name = readfun()
        except FileNotFoundError:
            talk("oops something is wrong")
            print("please enter the name manually!")
    else:
        writefun()
    creating_md()
    git_init()
    git_add()
    git_status()
    git_commit()
    git_status()
    connect_remote()
    git_push()
    engine.stop()
