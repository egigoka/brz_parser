from commands import *



for root, dirs, files in OS.walk('./output'):
    for file in files:
        json = JsonDict(Path.combine(root, file))

        ext = File.get_extension(file)

        name = file.replace(ext, '')
        
        for code, data in json.items():
            print(name, code, data['os_version'], data['storage'], data['price'].replace(newline, ''))

            
