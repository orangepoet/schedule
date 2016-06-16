from gen.generate import Generator
import os


class EnumCodeGenerate(Generator):
    def __init__(self):
        super(EnumCodeGenerate, self).__init__()

    def _get_models(self):
        ret = {'name': '', 'enum_items': []}
        lines = self.__get_lines(enum_file)
        ret.name = self.__get_enum_name(lines[0])

        for line in lines:
            if '=' in line:
                fields = line.strip().strip(',').split('=')
                if 'unknown' == fields[0].strip().lower():
                    continue
                ret['enum_items'].append({
                    'name': fields[0],
                    'value': fields[1]
                })

    def __get_lines(self, path):
        with open(path, 'r') as fin:
            return fin.readlines()

    def __get_enum_name(self, line):
        fields = line.split()
        if len(fields) == 3:
            return fields[2]
        else:
            index = line.find('enum')
            return line[index + 1].strip()

global enum_file

def main():
    enum_file = os.path.join('.','gen/input/enum.txt')
    generator = EnumCodeGenerate()
    generator.generate()


if __name__ == '__main__':
    main()
