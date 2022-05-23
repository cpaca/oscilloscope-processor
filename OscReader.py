import os

class OscilloscopeException(Exception):
    pass

class OscReader(object):
    def __init__(self, filename: str):
        if not os.path.exists(filename):
            if not filename.endswith(".csv"):
                filename += ".csv"

        if not os.path.exists(filename):
            if not filename.startswith("osc-data"):
                filename = "osc-data/" + filename

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
        self.name = os.path.basename(filename)
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

    #   Output-filename: The filename of the output.
    #       You can open it in OscReader later.
    #   Probes: Which probes to copy and combine.
    #       Sometimes you only want to combine one probe.
    #   Oscs: The oscilloscopes you're going to combine.
    @staticmethod
    def combine(output_filename: str, probes: list, oscs: list):
        for i in range(len(oscs)):
            osc = oscs[i]
            if type(osc) == OscReader:
                pass # already an oscilloscope reading
            elif type(osc) == str:
                # transform it into an oscilloscope reading
                oscs[i] = OscReader(oscs[i])
            else:
                raise OscilloscopeException("Cannot use " + str(osc) + " to create an oscilloscope reading.")

        if len(oscs) < 2:
            raise OscilloscopeException("Why would you need to combine less than two oscilloscope readings?")
        first = oscs[0]
        for osc in oscs:
            if not osc.check(first):
                raise OscilloscopeException("Oscilloscopes failed the check() function.")

        max_probes = len(first.data[1])
        for probe in probes:
            if type(probe) != int:
                raise OscilloscopeException("You need to number which probe you're using.")
            if probe < 1:
                raise OscilloscopeException("Probes are indiced starting at 1, not 0.")
            if probe > max_probes:
                raise OscilloscopeException("There are not " + probe + " probes.")

        with open(output_filename, "w") as f:
            # Because of the check() we know all of the oscilloscope readings have the same # of elements.
            rows = len(first.data)

            # Write the first row first.
            # No comma at the end of the first column
            # The later columns handle that
            f.write("x-axis")
            for osc in oscs:
                for probe in probes:
                    f.write(",")
                    f.write(osc.name)
                    f.write(" P" + str(probe))

            f.write("\n")

            # Second row.
            # From the check() we know all of them have the same second row.
            # So we can use any oscilloscope's second row, first column.
            f.write(first.data[1][0])
            # Next, go through the oscs and add their individual units.
            # Shouldn't matter regardless (repeat "volts" a million times) but just for ssfety.
            for osc in oscs:
                for probe in probes:
                    f.write(",")
                    f.write(str(osc.data[1][probe]))

            f.write("\n")
            # Third row and beyond.
            # We know they all have the same timestamp for each row.
            # Just need to copy the data.
            num_rows = len(first.data)
            for row in range(num_rows):
                if row < 2:
                    continue
                f.write(str(first.data[row][0]))
                for osc in oscs:
                    for probe in probes:
                        f.write(",")
                        f.write(str(osc.data[row][probe]))
                f.write("\n")

