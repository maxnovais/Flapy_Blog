# utf-8
# Framework Imports
from flask import request

def paginate(query, unity):
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=unity, error_out=False)
    return pagination
