import os
import shutil
import git

def main():
    repoUrl = "https://github.com/Jakmoore/dev-gradle-repo"
    localRepo = "gradle_repo"
    repo = git.Repo.clone_from(repoUrl, localRepo, progress=None, env=None)
    print("Cloned repo contents: " + str(os.listdir("gradle_repo")))
    filesInRepo = getFilesInRepo()

    for file in filesInRepo:
        with open("gradle_repo/" + file, "rb") as gradleFile, open("text_gradle_file.txt", "wb") as textGradleFile:
            textGradleFile.write(gradleFile.read())
            scanFile("text_gradle_file.txt")
            gradleFile.close()
            textGradleFile.close
            os.remove("text_gradle_file.txt")

    removeRepo()

def getFilesInRepo():
    files = os.listdir("gradle_repo")
    gradleFiles = []

    for file in files:
        if ".gradle" in file:
            gradleFiles.append(file)

    return gradleFiles

def scanFile(gradleFile):
    textGradleFile = open(gradleFile, "rb")
    print(textGradleFile.read())

def removeRepo():
    print("removing cloned repo.")
    shutil.rmtree("gradle_repo")

if __name__ == "__main__":
    main()