from gen import render_template, write_file, read_as_json, read_as_lines

template_name = 'repository.html'
base_config = 'repo.txt'
tb_config = 'tb.txt'


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

    _base = read_as_json(base_config)
    for line in read_as_lines(tb_config):
        ret.append(get_line_fields(line))

    return {
        'name': _base['name'],
        'entity': _base['entity'],
        'table': _base['table'],
        'namespace': _base['namespace'],
        'fields': ret
    }


def main():
    model = get_repo_model()
    page = render_template(template_name, model)
    if page:
        write_file('repo.txt', page)

    print 'done'


if __name__ == '__main__':
    main()
