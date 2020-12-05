run("Raw...", "open=[F:/Dec 12/10122019_01 ZF-01-2019/10122019_01 ZF-01-2019_rar.vol] image=[16-bit Unsigned] width=2183 height=2006 number=1667 little-endian");
run("8-bit");
run("Image Sequence... ", "format=TIFF save=[C:/Users/jeffzeyl/Desktop/ZF-01-2019/10122019_01 ZF-01-2019_rar0000.tif]");


dirname = r""C:\Users\jeffzeyl\Desktop\okzip"
# create a ZipFile object
with ZipFile('sampletest.zip', 'w') as zipObj:
   # Iterate over all the files in directory
   for folderName, subfolders, filenames in os.walk(dirName):
       for filename in filenames:
           #create complete filepath of file in directory
           filePath = os.path.join(folderName, filename)
           # Add file to zip
           zipObj.write(filePath, basename(filePath))