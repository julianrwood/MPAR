

class SingleImageClass():
    print("We are converting the supplied path to a MPAR single Image Class")

    def __init__(self, imagePath):
        pass
        print(imagePath)
        self.filePath = imagePath

    def getFilepath(self):
        print('Getting file path')
        return self.filePath

