class OscReader(object):
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

    # Checks whether this osc-reading and another osc reading
    # are similar to each other
    # "Similar" means they have the same timestep
    # and they have the same units
    def check(self, other):
        selfdata = self.data
        othdata = other.data

        if selfdata[1] != othdata[1]:
            return False

        if len(selfdata) != len(othdata):
            return False

        for i in range(len(selfdata)):
            # First two rows do not have time values.
            if i < 2:
                continue
            if selfdata[i][0] != othdata[i][0]:
                # Different timestep?
                # I found out - accidentally - that this one definitely works
                # also, don't open the csv files in excel. For some reason they get rounded off when you do.
                return False

        return True

