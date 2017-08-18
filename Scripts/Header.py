import json
from time import gmtime, strftime

indent = 4 * ' '

def filter_type(type):
    if type == 'void':
        return 'Void'

    if type == 'Vector3':
        return 'WVector3'

    if type == 'Vector3*':
        return 'WVector3*'

    return type

def load_natives_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_natives_json(natives_json, file, enum_hashes = False, show_comments = False):
    with open(file, 'w') as f:

        f.write('#pragma once\n\n')

        current_time = strftime('%d %b %Y', gmtime())

        f.write(f'// Generated on {current_time}\n')

        for (section_name, section_natives) in natives_json.items():
            f.write(f'\nnamespace {section_name}\n{{\n')

            for (native_hash, native_info) in section_natives.items():
                name        = native_info['name']
                params      = [ (filter_type(param['type']), param['name']) for param in native_info['params'] ]
                return_type = filter_type(native_info['return_type'])

                params_full_string = ', '.join([ f'{param_type} {param_name}' for param_type, param_name in params ])
                params_name_string = ', '.join([ f'Native_{native_hash}' if enum_hashes else native_hash ] + [ param_name for param_type, param_name in params ])

                comment = f'// {native_hash}'

                if 'jhash' in native_info:
                    comment += ' ' + native_info['jhash']

                comment += ' b' + native_info['first_build']

                if show_comments:
                    if native_info['comment']:
                        f.write('\n'.join([ f'{indent}// {line}' for line in native_info['comment'].strip().split('\n') ]) + '\n')

                f.write(indent + f'inline {return_type} {name}({params_full_string}) {{ return invoke<{return_type}>({params_name_string}); }} {comment}\n\n')

            f.write(f'}}\n')

save_natives_json(load_natives_json('../Natives.json'), 'Natives.h', enum_hashes = True, show_comments = True)
