from os import walk


class Interface:
    
    def __init__(self, folder):
        self.folder = folder
        
    
    def readFiles(self):
        self.filenames = next(walk(self.folder), (None, None, []))[2]
        
        
    
    def runningGui(self):
        
        chosenFile = {}
        counter = 0
        
        self.readFiles()
        
        for i in self.filenames:
            counter += 1
            chosenFile[counter] = i
            print(counter, ":", i)
        
        chosenValue = int(input("Choose a Value: "))
        

        if chosenValue > len(chosenFile) or chosenValue <= 0:
            raise ValueError ("Invalid Number")

        
        return chosenFile[chosenValue]
        
