def to_read_records(filename = 'records.txt'):
    with open(filename, 'r') as file:
        cnt = file.read()
    return cnt