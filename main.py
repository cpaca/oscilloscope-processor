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

