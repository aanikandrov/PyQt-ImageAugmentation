
def labels_filepath(path):
    """ Ищет путь к аннотациям """

    new_index = path.rfind('images')
    new_path = path[:new_index] + 'labels' + path[new_index + 6:]

    new_index = max(path.rfind('jpg'), path.rfind('png'))
    return new_path[:new_index] + 'txt'

def find_dot_index(s):
    """ Индекс точки в имени файла """

    dot_index = s.rfind('.')
    return s[:dot_index] if dot_index > 0 else s