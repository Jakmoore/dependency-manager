import os
import shutil
import re
import traceback
import requests
import json
from os import path
from dependency import Dependency

LOCAL_REPO = "dev-gradle-repo"
ORGINAL_DIR = os.getcwd()

def main():
    remote_repo = os.getenv("REMOTE_REPO", "https://github.com/Jakmoore/dev-gradle-repo.git")
    os.system(f"git clone {remote_repo}")
    files_in_repo = get_files_in_repo()
    error_occurred = False

    for x in files_in_repo:
        file = os.path.splitext(f"{x}")[0]

        try:
            with open(f"{LOCAL_REPO}/{x}", "rb") as gradle_file, open(f"{file}.txt", "wb") as text_gradle_file:
                text_gradle_file.write(gradle_file.read())
                gradle_file.close()
                text_gradle_file.close()       
                scan_file(file)
                add_file_to_git(file)
                os.chdir("/Users/jak/Documents/VS Code Projects/dependency-manager/") # Change to server directory
        except Exception as e:
            error_occurred = True
            if os.path.isfile(f"{file}.txt"):
                os.remove(f"{file}.txt") 

            traceback.print_exc()

    if not error_occurred: 
     push_updated_gradle_files()
    
    remove_repo()

def get_files_in_repo():
    files = []

    for file in os.listdir(LOCAL_REPO):
        if ".gradle" in file:
            files.append(file)
    
    print(f"Files in repo: {files}")
    
    return files

def scan_file(file):
    with open(f"{file}.txt") as text_gradle_file:
       lines = text_gradle_file.readlines()
       dependencies = []
       new_versions = get_new_versions()

       for line in lines:
           if "compile" in line:
            extracted_elements = re.findall(r"'([^']+)'", line)

            if len(extracted_elements) > 0:
                dependency = Dependency(extracted_elements[0], extracted_elements[1], extracted_elements[2])
                dependencies.append(dependency)
        
       for current_dependency in dependencies:
            for new_version in new_versions:
                if current_dependency.name == new_version.name and current_dependency.group == new_version.group:
                    if not current_dependency.version == new_version.version:
                     print(f"Upgrading {current_dependency.name} from version {current_dependency.version} to version {new_version.version}")
                     current_dependency.version = new_version.version

       apply_new_versions(dependencies, file)

def apply_new_versions(new_versions, file):
    dependencies = ""

    for dep in new_versions:
        dependencies += dep.toString() + "\n"
        
    gradle_template = "ext { springBoot = '2.1.5.RELEASE' activeMQVersion = '5.15.11' camelVersion = '2.23.4' log4jVersion = '2.13.2' } \n dependencies {%s}" % dependencies 

    with open(f"{file}.txt", "w") as updated_gradle_file:
        updated_gradle_file.write(gradle_template)
         
def get_new_versions():
    vulnerabilities_url = os.getenv("VULNERABILITIES_ENDPOINT", "http://localhost:5000/vulnerabilities")
    response = requests.get(vulnerabilities_url)

    if response.status_code == 200:
        response_content = json.loads(response.content.decode("UTF-8"))
        new_versions = []

        for dep in response_content["vulnerabilities"]:
            new_versions.append(Dependency(dep.get("group"), dep.get("name"), dep.get("version")))  
        
        return new_versions 
    
    else:
        raise Exception(f"Error, HTTP status code: {response.status_code}")

def add_file_to_git(file):
    os.rename(f"{file}.txt", f"{file}.gradle")
    os.chdir(LOCAL_REPO)
    os.system(f"git rm {file}.gradle")
    os.system(f"mv /Users/jak/Documents/VS\ Code\ Projects/dependency-manager/{file}.gradle /Users/jak/Documents/VS\ Code\ Projects/dependency-manager/{LOCAL_REPO}/") # Change to server directory
    os.system(f"git add {file}.gradle")

def push_updated_gradle_files():
   os.chdir(LOCAL_REPO)
   print("Pushing updated files to remote repo.")
   os.system("git commit -m 'Updated gradle files'")
   os.system("git push")

def remove_repo():
    os.chdir(ORGINAL_DIR)
    
    if path.isdir(LOCAL_REPO):
        print(f"Removing cloned repo: '{LOCAL_REPO}'.")
        shutil.rmtree(LOCAL_REPO)

if __name__ == "__main__":
    main()