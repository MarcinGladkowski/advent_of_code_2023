def load_data(file_name: str) -> list:
    with open(file_name) as f:
        return [x.replace('\n', '') for x in f.readlines()]
