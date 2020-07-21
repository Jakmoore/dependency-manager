import os
import shutil
import re
import git
import traceback
from pathlib import Path
from dependency import Dependency

LOCAL_REPO = "gradle_repo"

def main():
    repo = get_remote_repo()
    files_in_repo = get_files_in_repo()

    try:
        with open(f"{LOCAL_REPO}/test_gradle.gradle", "rb") as gradle_file, open("text_gradle_file.txt", "wb") as text_gradle_file:
            text_gradle_file.write(gradle_file.read())
            gradle_file.close()
            text_gradle_file.close()       
            scan_file()
            push_updated_gradle_file(repo)
            os.remove("text_gradle_file.txt") 
            os.remove("updated_gradle_file.txt")
    except Exception as e:
        if os.path.isfile("text_gradle_file.txt"):
            os.remove("text_gradle_file.txt") 
            os.remove("updated_gradle_file.txt")

        remove_repo()
        traceback.print_exc()
    finally:
        if os.path.isdir(LOCAL_REPO):
            remove_repo()

def get_remote_repo():
    repo_url = "https://github.com/Jakmoore/dev-gradle-repo"
    return  git.Repo.clone_from(repo_url, LOCAL_REPO, progress=None, env=None)

def get_files_in_repo():
    files = os.listdir(LOCAL_REPO)
    gradle_files = []

    for a in files:
        if ".gradle" in a:
            gradle_files.append(a)

    return gradle_files

def scan_file():
    print(f"Scanning file.")
    with open("text_gradle_file.txt") as text_gradle_file:
       lines = text_gradle_file.readlines()
       dependencies = []
       new_versions = get_new_versions()

       for line in lines:
           extracted_elements = re.findall(r"'([^']+)'", line)

           if len(extracted_elements) > 0:
             dependency = Dependency(extracted_elements[0], extracted_elements[1], extracted_elements[2])
             dependencies.append(dependency)
        
       for current_dependency in dependencies:
            for new_version in new_versions:
                if current_dependency.name == new_version.name and current_dependency.group == new_version.group:
                    print(f"Upgrading {current_dependency.name} from version {current_dependency.version} to version {new_version.version}")
                    current_dependency.version = new_version.version

       apply_new_versions(dependencies)

def apply_new_versions(new_versions):
    with open("updated_gradle_file.txt", "w") as updated_gradle_file:
        for dep in new_versions:
            updated_gradle_file.write(f"{dep.toString()} \n")
    
def get_new_versions():
    data = [['commons-io', 'commons-io', '2.8'], ['org.springframework.boot', 'spring-boot-starter-web', '2.3.3.RELEASE']]
    print("Retrieving data source.")
    new_versions = []

    for element in data:
        new_versions.append(Dependency(element[0], element[1], element[2]))

    return new_versions

def push_updated_gradle_file(repo: git.Repo):
    index = repo.index
    path = Path("updated_gradle_file.txt")
    path.rename(path.with_suffix(".gradle"))
    index.remove("test_gradle.gradle")
    index.add(["updated_gradle_file.gradle"])
    index.commit("Updated gradle dependencies.")
    origin = repo.remote()
    origin.push("master")

def remove_repo():
    print("Removing cloned repo.")
    shutil.rmtree(LOCAL_REPO)

if __name__ == "__main__":
    main()