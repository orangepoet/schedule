from app import get_config, read_to_lines, write_file, TMP_OUT
from gen import render_template

template_name = 'repository.html'
tb_config = 'table.txt'

entity = get_config(__file__, 'entity')
table_name = get_config(__file__, 'table_name')
namespace = get_config(__file__, 'namespace')


def get_line_fields(line):
    field = line.split()
    return {'name': field[0], 'dtype': get_db_type(field[1]), 'ctype': get_csharp_type_from_dbtype(field[1])}


def get_csharp_type_from_dbtype(dbtype):
    return {
        'bigint': 'long',
        'int': 'int',
        'nvarchar': 'string',
        'datetime': 'DateTime',
        'tinyint': 'int'
    }[dbtype]


def get_db_type(dbtype):
    return {
        'bigint': 'Int64',
        'int': 'Int32',
        'nvarchar': 'String',
        'datetime': 'DateTime',
        'tinyint': 'Int16'
    }[dbtype]


def get_repo_model():
    ret = []

    for line in read_to_lines(tb_config):
        ret.append(get_line_fields(line))

    return {
        'name': entity,
        'entity': entity,
        'table': table_name,
        'namespace': namespace,
        'fields': ret
    }


def render_repo():
    model = get_repo_model()
    page = render_template(template_name, model=model)
    if page:
        write_file('{0}Repository.cs'.format(model['name']), page, TMP_OUT)

    print 'done'


if __name__ == '__main__':
    render_repo()
