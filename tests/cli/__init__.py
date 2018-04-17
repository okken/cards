def detabulate_output(output):
    """
    Turn a tabulate output into a tuple of headers and rows
    assuming the output was formatted in the "jira" style
    """
    lines = output.split('\n')
    headers = lines[0].split('||')
    headers = [header.strip() for header in headers[1:-1]]
    values = [[item.strip()
               for item in row.split('|')[1:-1]] for row in lines[1:]]
    return headers, values
