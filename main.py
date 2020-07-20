import os
import shutil
import re
import git
from dependency import Dependency

local_repo = "gradle_repo"

def main():
    repo = get_repo()
    files_in_repo = get_files_in_repo()

    try:
        for a in files_in_repo: 
         with open(f"{local_repo}/{a}", "rb") as gradle_file, open("text_gradle_file.txt", "wb") as text_gradle_file:
            text_gradle_file.write(gradle_file.read())
            gradle_file.close()
            text_gradle_file.close()       
            scan_file()
            os.remove("text_gradle_file.txt") 
    except Exception as e:
       # os.remove("text_gradle_file.txt") 
        remove_repo()
        print(f"Error: {e}")

    finally:
        if os.path.isdir(local_repo):
            remove_repo()

def get_repo():
    repo_url = "https://github.com/Jakmoore/dev-gradle-repo"
    return  git.Repo.clone_from(repo_url, local_repo, progress=None, env=None)

def get_files_in_repo():
    files = os.listdir(local_repo)
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
             print(dependency.toString())

       for dependency in dependencies:
           for new_version in new_versions:
               print(dependency.name)

def get_new_versions():
    data = [['commons-io', 'commons-io', '2.8'], ['org.springframework.boot', 'spring-boot-starter-web', '2.3.1.RELEASE']]
    print("Retrieving data source.")
    return data

def remove_repo():
    print("Removing cloned repo.")
    shutil.rmtree(local_repo)

if __name__ == "__main__":
    main()
