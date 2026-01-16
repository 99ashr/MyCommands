import os
import emoji
import pickle
import pyttsx3


# &Create Object and Set voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')  # getting details of current voice
# Set to a British female English voice if available
british_female_voice = None
for v in voices:
    if (
        ((hasattr(v, 'gender') and 'female' in v.gender.lower()) or ('female' in v.name.lower()))
        and (
            'british' in v.name.lower() or 'uk' in v.name.lower() or 'en-gb' in v.id.lower() or 'en_uk' in v.id.lower()
        )
    ):
        british_female_voice = v
        break
if not british_female_voice:
    # Fallback: any English female voice
    for v in voices:
        if (
            ((hasattr(v, 'gender') and 'female' in v.gender.lower()) or ('female' in v.name.lower()))
            and ('english' in v.name.lower() or 'en_' in v.id.lower())
        ):
            british_female_voice = v
            break
if not british_female_voice:
    # Fallback: any female voice
    for v in voices:
        if (hasattr(v, 'gender') and 'female' in v.gender.lower()) or ('female' in v.name.lower()):
            british_female_voice = v
            break
if british_female_voice:
    engine.setProperty('voice', british_female_voice.id)
else:
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
    talk("Saving repository name to myRepos.txt.")
    with open("myRepos.txt", "ab") as filehandle:
        pickle.dump(repo_name, filehandle)
    talk("Repository name saved.")

def readfun():
    talk("Reading last saved repository name from myRepos.txt.")
    with open("myRepos.txt", "rb") as filehandle:
        try:
            while True:
                all_repos.append(pickle.load(filehandle))
        except EOFError:
            pass
        talk(f"Last saved repository name is {all_repos[-1]}")
        return all_repos[-1]

def current_dir():
    talk("Getting current working directory.")
    return os.getcwd()

def creating_md():
    talk("Creating README file for you.")
    print("Creating README File for you!")
    print(emoji.emojize("\nPlease Wait...:slightly_smiling_face:"))
    os.system(f"echo '# {repo_name}'>README.md")
    talk("Created README.md successfully for you.")
    print(
        emoji.emojize(
            "\nCreated README.md successfully for you!:smiling_face_with_halo:"
        )
    )

def git_init():
    talk("Initializing your git repository.")
    print(
        emoji.emojize(
            "\nInitializing your repository...:smiling_face_with_smiling_eyes:"
        )
    )
    os.system("git init")
    talk("Git repository initialized.")

def git_add():
    talk("Adding files to commit.")
    print(emoji.emojize("\n Initializing Git Add Command for you...:smiling_face:"))
    os.system("git add .")
    talk("Files added to commit.")

def git_status():
    talk("Checking git status.")
    print(emoji.emojize("Here's the status of this REPO...:face_savoring_food:"))
    os.system("git status")

def git_commit():
    talk("Ready to commit your changes.")
    print(emoji.emojize("Ready To Commit Your MESS...?:expressionless_face:"))
    talk("Please enter your commit message")
    commit_msg = input(
        emoji.emojize(
            "Please enter your commit message here:drooling_face:\n message:")
    )
    if not commit_msg.strip():
        commit_msg = "Auto-commit from auto_git"
    commit = f'git commit -m "{commit_msg}"'
    result = os.system(commit)
    if result == 0:
        talk("Commit successful.")
    else:
        talk("Commit failed. Please check for errors.")

user_repo_link = "https://github.com/99ashr/"
remote = "git remote add origin"

def connect_remote():
    talk("Connecting to your remote GitHub repository.")
    print(emoji.emojize("Connecting to your remote directory...:lying_face:"))
    # Check if remote 'origin' exists
    remote_url = f"{user_repo_link}{repo_name}.git"
    remote_check = os.system("git remote get-url origin > /dev/null 2>&1")
    if remote_check != 0:
        os.system(f"git remote add origin {remote_url}")
    else:
        os.system(f"git remote set-url origin {remote_url}")
    talk("Remote repository set.")

def git_push():
    talk("Pushing your changes to GitHub.")
    import subprocess
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    except Exception:
        branch = "main"
    push_cmd = f"git push -u origin {branch}"
    result = os.system(push_cmd)
    # If push fails due to missing remote repo, try to create it using GitHub CLI and push again
    if result != 0:
        print("Push failed. Attempting to create the repository on GitHub using GitHub CLI...")
        talk("Push failed. Attempting to create the repository on GitHub.")
        # Try to create the repo (public by default)
        create_cmd = f"gh repo create {repo_name} --public --source=. --push"
        create_result = os.system(create_cmd)
        # Always set the remote URL to origin after creation
        remote_url = f"https://github.com/99ashr/{repo_name}.git"
        os.system(f"git remote set-url origin {remote_url}")
        if create_result == 0:
            print("Repository created and pushed to GitHub.")
            talk("Repository created and pushed to GitHub successfully.")
        else:
            print("Failed to create repository on GitHub. Please check your GitHub CLI authentication and try again.")
            talk("Failed to create repository on GitHub. Please check your GitHub CLI authentication and try again.")
    else:
        talk("Push to GitHub successful.")

if __name__ == "__main__":
    talk("Starting the auto git workflow.")
    current_dir()
    if repo_name == "":
        try:
            repo_name = readfun()
        except FileNotFoundError:
            talk("Oops, something is wrong. Please enter the name manually.")
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
    talk("Auto git workflow complete.")
    engine.stop()
