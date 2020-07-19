import os
import shutil
import re
import git
from Dependency import Dependency

def main():
    localRepo = "gradle_repo"
    repo = getRepo(localRepo)
    filesInRepo = getFilesInRepo(localRepo)

    try:
        for a in filesInRepo: 
         with open(f"{localRepo}/{a}", "rb") as gradleFile, open("text_gradle_file.txt", "wb") as textGradleFile:
            textGradleFile.write(gradleFile.read())
            gradleFile.close()
            textGradleFile.close()       
            scanFile()
            os.remove("text_gradle_file.txt") 
    except Exception as e:
        os.remove("text_gradle_file.txt") 
        removeRepo(localRepo)
        print(f"Error: {e}")

    finally:
        if os.path.isdir(localRepo):
            removeRepo(localRepo)

def getRepo(localRepo):
    repoUrl = "https://github.com/Jakmoore/dev-gradle-repo"
    repo = git.Repo.clone_from(repoUrl, localRepo, progress=None, env=None)
    print(f"Cloned repo contents: {str(os.listdir(localRepo))}")
    return repo

def getFilesInRepo(localRepo):
    files = os.listdir(localRepo)
    gradleFiles = []

    for a in files:
        if ".gradle" in a:
            gradleFiles.append(a)

    return gradleFiles

def scanFile():
    print(f"Scanning file.")
    with open("text_gradle_file.txt") as textGradleFile:
       lines = textGradleFile.readlines()

       for line in lines:
           extractedElements = re.findall(r"'([^']+)'", line)
           dependency = Dependency(extractedElements[0], extractedElements[1], extractedElements[2])

           print(f"Group: {dependency.group}, name: {dependency.name}, version: {dependency.version}")
           

def removeRepo(localRepo):
    print("Removing cloned repo.")
    shutil.rmtree(localRepo)

if __name__ == "__main__":
    main()