from status_code import _STATUSES
status = 200
def handler(response_headers):
    reason = _STATUSES[status]
    response_line = 'HTTP/1.1 %s %s\r\n' % (status, reason)
    blank_line = b'\r\n'
    response_body = b'<h1>501 Not Implemented</h1>'
    return b"".join([response_line, response_headers, blank_line, response_body])
    