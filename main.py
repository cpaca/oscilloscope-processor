from OscReader import OscReader
import os

# Run checks on the data
print("Checking oscilloscopes...")
passed = True
BasicOscReading = "osc-data/1MV2.csv"
CompareWith = OscReader(BasicOscReading)
for dirpath, dirnames, filenames in os.walk("osc-data"):
    for filename in filenames:
        filepath = dirpath + "\\" + filename
        reader = OscReader(filepath)
        if not CompareWith.check(reader):
            print(CompareWith, " Failed check with ", filepath)
            passed = False
            break

if passed:
    print("Passed osc-reading checker")
else:
    print("Failed osc-reading checker. Stopping.")
    import sys
    sys.exit("Invalid oscilloscope readings")

# Now to start combining oscilloscope data.
OscReader.combine("output-oscs/1uFV123456.csv", [1], ["OCv1", "OCV2", "OCV3", "OCV4", "OCV5", "OCV6"])
OscReader.combine("output-oscs/22uFV123456.csv", [2], ["OCV1", "OCV2", "OCV3", "OCV4", "OCV5", "OCV6"])
OscReader.combine("output-oscs/1uFWithLoad.csv", [1], ["OCV6", "10MV6", "5MV6", "1MV6", "500kV6", "10kV6"])
OscReader.combine("output-oscs/22uFWithLoad.csv", [2], ["OCV6", "10MV6", "5MV6", "1MV6", "500kV6", "10kV6"])

