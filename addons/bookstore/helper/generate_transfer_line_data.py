from collections import defaultdict


def generate_transfer_line_data(lines):
    book_set = defaultdict(lambda: 0)
    for line in lines:
        book_set[line.book_id.id] += line.qty
    return [(0, 0, {'book_id': book_id, 'qty': qty}) for book_id, qty in book_set.items()]
