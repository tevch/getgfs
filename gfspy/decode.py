import regex as re
import numpy as np


class Variable:
    def __init__(self, name, coords, data):
        self.name = name
        self.coords = coords
        self.data = data

    def __str__(self):
        print(type(self))
        return self.name


class Coordinate:
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def __str__(self):
        print(type(self))
        return self.name


class File:
    def __init__(self, text):
        text = text.splitlines()
        # Get variable name and dimensionality
        ind_head = 0
        variables = []
        while ind_head < len(text):
            variable_name = re.findall("(.*?), ", text[ind_head])[0]
            dims = re.findall("\[(.*?)\]", text[ind_head])
            dims.reverse()
            lines_data = 0
            for dim in dims[1:]:
                lines_data = int(dim) * (lines_data + 1)
            dims.reverse()

            lines_meta = len(dims) * 2  # Starts +1 from end of lines data
            name_line = True
            coords = []
            for line in text[
                ind_head + 2 + lines_data : ind_head + 3 + lines_data + lines_meta
            ]:
                if name_line:
                    name = re.findall("(.*?), ", line)[0]
                    name_line = False
                else:
                    coords.append(
                        Coordinate(name, [float(v[:-1]) for v in line.split()])
                    )
                    name_line = True

            data = np.zeros(tuple([int(d) for d in dims]))
            data[:] = np.nan
            for line in text[ind_head + 1 : ind_head + 1 + lines_data - 1]:
                if len(line) > 0 and line[0] == "[":
                    position = [int(v) for v in re.findall("\[(.*?)\]", line)]
                    values = line.split()[1:]
                    if len(values) > 1:
                        for ind, value in enumerate(values):
                            if value[-1] == ",":
                                value = value[:-1]
                            data = replace_val(data, float(value), position + [ind])
                    else:
                        data = replace_val(data, float(values[0]), position)

            coords = {c.name: c for c in coords}
            variables.append(Variable(variable_name, coords, data))

            ind_head += lines_data + lines_meta + 2

        self.variables = {v.name: v for v in variables}
    
    def __str__(self):
        print(type(self))
        return "File containing %s"%self.variables.keys()


def replace_val(arr, val, position):
    if not isinstance(position, list):
        raise TypeError("Wrong type entered for replacement position")
    # I wish I could find a proper way todo this, np.put only works for 1D arrays
    if len(position) == 1:
        arr[position[0]] = val
    elif len(position) == 2:
        arr[position[0]][position[1]] = val
    elif len(position) == 3:
        arr[position[0]][position[1]][position[2]] = val
    elif len(position) == 4:
        arr[position[0]][position[1]][position[2]][position[3]] = val
    else:
        raise ValueError(
            "Number of dimensions for value replacement not supported, please edit and make pull request it will be very easy"
        )

    return arr
