import os
import shutil
import re
import traceback
import csv
from dependency import Dependency

LOCAL_REPO = "dev-gradle-repo"

def main():
    os.system("git clone https://github.com/Jakmoore/dev-gradle-repo.git")
    files_in_repo = get_files_in_repo()

    try:
        with open(f"{LOCAL_REPO}/test_gradle.gradle", "rb") as gradle_file, open("text_gradle_file.txt", "wb") as text_gradle_file:
            text_gradle_file.write(gradle_file.read())
            gradle_file.close()
            text_gradle_file.close()       
            scan_file()
            push_updated_gradle_file()
            os.chdir("/Users/jak/Documents/VS Code Projects/DependencyManager/")
            os.remove("text_gradle_file.txt") 
    except Exception as e:
        if os.path.isfile("text_gradle_file.txt"):
            os.remove("text_gradle_file.txt") 
        
        if os.path.isfile("updated_gradle_file.gradle"):
            os.remove("updated_gradle_file.gradle")

        remove_repo()
        traceback.print_exc()
    finally:
        if os.path.isdir(LOCAL_REPO):
            remove_repo()

def get_files_in_repo():
    files = os.listdir(LOCAL_REPO)
    gradle_files = []

    for a in files:
        if ".gradle" in a:
            gradle_files.append(a)

    return gradle_files

def scan_file():
    with open("text_gradle_file.txt") as text_gradle_file:
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

       apply_new_versions(dependencies)

def apply_new_versions(new_versions):
    dependencies = ""

    for dep in new_versions:
        dependencies += dep.toString() + "\n"
    
    print(dependencies)

    gradle_template = "ext { springBoot = '2.1.5.RELEASE' activeMQVersion = '5.15.11' camelVersion = '2.23.4' log4jVersion = '2.13.2' } dependencies {%s}" % dependencies

    with open("updated_gradle_file.txt", "w") as updated_gradle_file:
        updated_gradle_file.write(gradle_template)
         
def get_new_versions():
    new_versions = []

    with open("dev_gradle_csv.csv") as f:
       rows = csv.reader(f)

       for row in rows:
           new_versions.append(Dependency(row[0].strip('"\''), row[1].strip('"\''), row[2].strip('"\'')))

    return new_versions

def push_updated_gradle_file():
    os.rename("updated_gradle_file.txt", "test_gradle.gradle")
    os.chdir(LOCAL_REPO)
    os.system("git rm test_gradle.gradle")
    os.system(f"mv /Users/jak/Documents/VS\ Code\ Projects/DependencyManager/test_gradle.gradle /Users/jak/Documents/VS\ Code\ Projects/DependencyManager/{LOCAL_REPO}/")
    os.system("git add test_gradle.gradle")
    os.system("git commit -m 'Updated gradle file'")
    os.system("git push")

def remove_repo():
    print("Removing cloned repo.")
    shutil.rmtree(LOCAL_REPO)

if __name__ == "__main__":
    main()