

class OscReader:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            data = f.readlines()
            for i in range(len(data)):
                line = data[i]
                # this is true for all lines in the osc-output
                # but I've seen some formats where it's not true for the last line
                # so just to be safe, I have it.
                if line[-1] == "\n":
                    line = line[:-1]
                row = line.split(",")
                # Row 0 is x-axis, 1, 2
                # Row 1 is the units
                # After that is the data
                if i > 1:
                    # sometimes oscilloscope will only output one probe
                    # so this makes sure we only handle one probe in that situation
                    for j in range(len(row)):
                        # PyCharm is mad at me for this
                        # probably cause i'm turning a string to a float and keeping the same var
                        # but whatever
                        row[j] = float(row[j])
                data[i] = row

            self.data = data

