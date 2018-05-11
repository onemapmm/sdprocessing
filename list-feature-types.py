import arcpy, os, csv
from arcpy import env
from arcpy.sa import *

#newlinetest
#2ndnewlinetest
#3rd new line

searchfolder = arcpy.GetParameterAsText(0)
output_textfile = arcpy.GetParameterAsText(1)           ## set type "file" and direction to output in tool GUI parameters tab.

searchfolder = r"D:\MIMU_OM_personal_backup20170828\MIMU\OneMap\Data\Survey-Extracts\Temp 2\Zone-47 _Raw_Data\1896_DWG"
output_textfile = r"D:\Survey-data-upgrade\scripts\Processing-from-TNT\outputs\DWG_files_listed.txt"

searchfolder = searchfolder.split(";")
arcpy.AddMessage("Selected folders to be processed:")

for entry in searchfolder:
    arcpy.AddMessage(entry)

arcpy.AddMessage("Compiling textfile...")
i = 0

for location in searchfolder:

    arcpy.env.workspace = location
    arcpy.env.overwriteOutput = True

    # file selection
    if i == 0:
        found_files = []

    for dirpath, dirnames, filename in arcpy.da.Walk(location):
        if dirpath.lower().endswith('.dwg'):
            for item in filename:
                found_files.append(os.path.join(dirpath, item))
    i = i+1


# get attribute values from file:

#function to get the field values from a specified attribute field:

def attribute_values(table , field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

#adding the subfile name to the filepath:
found_attribute_values= []

dictionary= {}

def update_dictionary(dict, key, value):
    if key not in dictionary:
        dictionary[key] = [value]
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]


for entry in found_files:
    found_attributes = attribute_values(entry,"Layer")
    for attr in found_attributes:
        update_dictionary(dictionary,attr,entry)

print dictionary

with open(output_textfile, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dictionary.items():
        writer.writerow([key, ", ".join([str(i) for i in value])])
