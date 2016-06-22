from gen.generate import Generator
import os


class RepositoryGenerator(Generator):
    template_name = 'repository.html'
    base_config = 'repo.txt'
    tb_config = 'tb.txt'

    def __init__(self):
        super(RepositoryGenerator, self).__init__()

    def _get_models(self):
        from json import load

        m_tb_fields = []
        with open(self.__get_config_file_path(self.base_config), 'r') as fin:
            m_base_config = load(fin)
        with open(self.__get_config_file_path(self.tb_config), 'r') as fin:
            for l in fin.readlines():
                m_tb_fields.append(self.__read_fields(l))
        return {
            'name': m_base_config['name'],
            'entity': m_base_config['entity'],
            'table': m_base_config['table'],
            'namespace': m_base_config['namespace'],
            'fields': m_tb_fields
        }

    def __read_fields(self, line):
        field = line.split()
        return {'name': field[0], 'dtype': self.__get_db_type(field[1]), 'ctype': self.__get_csharp_type(field[1])}

    def __get_config_file_path(self, file_name):
        return os.path.join(os.path.abspath('..'), 'gen/input', file_name)

    def __get_csharp_type(self, dbtype):
        return {
            'bigint': 'long',
            'int': 'int',
            'nvarchar': 'string',
            'datetime': 'DateTime',
            'tinyint': 'int'
        }[dbtype]

    def __get_db_type(self, dbtype):
        return {
            'bigint': 'Int64',
            'int': 'Int32',
            'nvarchar': 'String',
            'datetime': 'DateTime',
            'tinyint': 'Int16'
        }[dbtype]


def main():
    import time
    result = RepositoryGenerator().generate()
    output = os.path.join(os.path.abspath('.'), 'output', 'repo_{time}.txt'.format(time=time.strftime('%Y%m%dH%H%M')))
    with open(output, 'w+') as fp:
        fp.write(result)
    print 'done'


if __name__ == '__main__':
    main()
