
class ProjectFile:
    def __init__(self,FileName,ProjectName,ProjectUserID,Processed ,UploadDate,UploadPath,lang):
        self.FileName = FileName
        self.ProjectName = ProjectName
        self.ProjectUserID = ProjectUserID
        self.Processed = Processed
        self.UploadDate = UploadDate
        self.UploadPath = UploadPath
        self.lang = lang
        self.FileID = ""

    def setFileID(self , fileID):
        self.FileID  = fileID




