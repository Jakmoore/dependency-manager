import os
import shutil
import git

def main():
    localRepo = "gradle_repo"
    repo = getRepo(localRepo)
    filesInRepo = getFilesInRepo(localRepo)

    for a in filesInRepo: 
        with open(f"{localRepo}/{a}", "rb") as gradleFile, open("text_gradle_file.txt", "wb") as textGradleFile:
            textGradleFile.write(gradleFile.read())
            scanFile("text_gradle_file.txt")
            gradleFile.close()
            textGradleFile.close()
            os.remove("text_gradle_file.txt")

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

def scanFile(gradleFile):
    print(f"Scanning file {gradleFile}")
    textGradleFile = open(gradleFile, "rb")

def removeRepo(localRepo):
    print("Removing cloned repo.")
    shutil.rmtree(localRepo)

if __name__ == "__main__":
    main()