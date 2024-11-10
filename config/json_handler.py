from json import load, JSONDecodeError


def load_config():
    try:
        with open('config/settings.json', 'r', encoding='utf-8') as f:
            return load(f)
    except FileNotFoundError:
        raise FileNotFoundError
    except JSONDecodeError:
        raise JSONDecodeError
    except Exception as e:
        raise Exception(f'Unexpected error: {e}')
