from pathlib import Path

class FileHandling():
    def __init__(self, path_to_file: str):
        
        self.absolute_filename = Path(path_to_file)
        
        if self.absolute_filename.exists():
            self.file = open(self.absolute_filename)
        else:
            raise ValueError("Invalid path to file")
    
    def print(self):
        print(self.absolute_filename)
    
    def get_raw_input(self) -> dict:
        dict_input = dict()
        lines = self.file.readlines()
        
        dict_input["Components"] = lines[0][:-1]
        dict_input["Rules"] = [line[:-1] for line in lines[1:]]
        
        return dict_input