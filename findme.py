import fnmatch

from prettytable import PrettyTable

from commands import *

to_find = {"capacity": ["*256*", "*512*", "*1024*"],
           "name": ["*Pro Max*"]}

table = PrettyTable()
table.field_names = ["Name", "Code", "OS version", "Capacity", "Price"]

for root, dirs, files in OS.walk('./output'):
    for file in files:
        json = JsonDict(Path.combine(root, file))

        ext = File.get_extension(file)

        name = file.replace(ext, '')

        for code, data in json.items():
            if data['name'] is None:  # TODO: remove this line
                data['name'] = name  # TODO: remove this line
            to_print = True
            for key, values in to_find.items():
                if key in data:
                    found = False
                    for value in values:
                        if fnmatch.fnmatch(data[key], value):
                            found = True
                            break
                    if not found:
                        to_print = False
                        break
                else:
                    raise KeyError(f"Key {key} not found in {data}")
            if to_print:

                price_text = data['price']

                table.add_row([data['name'], code, data['os_version'], data['capacity'], price_text])
print(table)
