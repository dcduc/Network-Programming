from status_code import _STATUSES
status = 404
def handler():
    reason = _STATUSES[status]
    respone_line = 'HTTP/1.1 %s %s\r\n' % (status, reason)
    return respone_line.encode(), b'<h1>404 Not Found</h1>'
    