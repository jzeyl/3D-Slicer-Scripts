# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"([^\[\]]*)"

test_str = "run(\"Image Sequence...\", \"open=[E:/0backof head analyses/5_Feb7crops/CFranc-01-2019/cfranc-01-2019 backofhead0000.tif] sort\")"

split_ = re.split(regex,test_str)
filenames = ["E:/0backof head analyses/6_Feb12crops/FTdrong-01-2019/Ftdrong-01-2019backofhead0000.tif",
"E:/0backof head analyses/6_Feb12crops/KTC-01-2020/KTC-01-20200000.tif",
"E:/0backof head analyses/6_Feb12crops/LB/LBbackofhead0000.tif",
"E:/0backof head analyses/6_Feb12crops/Bouc-01-2020/Bcouc-01-2020 backofhead0042.tif",
"E:/0backof head analyses/6_Feb12crops/BCL-01-2019/BCL-01-2019 black capped lory0000.tif",
"E:/0backof head analyses/6_Feb12crops/Cfisc-01-2019/Cfisc-01-2019backofhead0000.tif",
"E:/0backof head analyses/6_Feb12crops/Othrush-01-2019/Othrush-01-2019backofhead0000.tif"]

#fifth regex match is the one needed to swap out
filepart = re.split(regex,test_str)[5]#replace this regex with the file name into the split_ list
for i in range(7):
    split_[5] = filenames[i]
    ''.join(split_)

#run("Image Sequence...", "open=[E:/0backof head analyses/6_Feb12crops/FTdrong-01-2019/Ftdrong-01-2019backofhead0000.tif] sort")
#run("Image Sequence...", "open=[E:/0backof head analyses/6_Feb12crops/KTC-01-2020/KTC-01-20200000.tif] sort")
#run("Image Sequence...", "open=[E:/0backof head analyses/6_Feb12crops/LB/LBbackofhead0000.tif] sort")
#run("Image Sequence...", "open=[E:/0backof head analyses/6_Feb12crops/Bouc-01-2020/Bcouc-01-2020 backofhead0042.tif] sort")
#run("Image Sequence...", "open=[E:/0backof head analyses/6_Feb12crops/BCL-01-2019/BCL-01-2019 black capped lory0000.tif] sort")
#run("Image Sequence...", "open=[E:/0backof head analyses/6_Feb12crops/Cfisc-01-2019/Cfisc-01-2019backofhead0000.tif] sort")
#run("Image Sequence...", "open=[E:/0backof head analyses/6_Feb12crops/Othrush-01-2019/Othrush-01-2019backofhead0000.tif] sort")


matches = re.finditer(regex, test_str)
listmatches = list(matches)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.