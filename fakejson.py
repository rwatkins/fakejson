import re


def loads(s):
    end = 0
    nextchar = s[end:end+1]
    while is_whitespace(nextchar):
        end += 1
        nextchar = s[end:end+1]

    val = None
    if nextchar == '{':
        val, end = parse_object(s, end=end)
    elif nextchar == '[':
        val, end = parse_array(s, end=end)

    if val is None:
        raise Exception("No value found in input string")

    end += 1
    nextchar = s[end:end+1]

    # Check for extra non-whitespace characters after value
    while is_whitespace(nextchar):
        end += 1
        nextchar = s[end:end+1]

    if nextchar:
        raise Exception("Extra data found in input string")

    return val


def parse_object(s, end=0):
    def _print(st):
        print '[parse_object] %s' % st

    obj = {}
    while True:
        end += 1
        nextchar = s[end:end+1]
        _print('nextchar: %s    end: %s' % (nextchar, end))
        # parse key
        print 'parse key'
        while is_whitespace(nextchar):
            end += 1
            nextchar = s[end:end+1]

        if nextchar != '"':
            raise Exception("Expected \", got %s\nso far: %s\nwhole thing: %s"
                            % (nextchar, s[:end], s))

        key, end = parse_string(s, end=end)
        end += 1
        nextchar = s[end:end+1]
        while is_whitespace(nextchar):
            end += 1
            nextchar = s[end:end+1]

        if nextchar != ':':
            raise Exception("Expected :, got %s" % nextchar)

        # parse value
        print 'parse value'
        end += 1
        nextchar = s[end:end+1]
        while is_whitespace(nextchar):
            end += 1
            nextchar = s[end:end+1]

        value, end = parse_object_value(s, end=end)

        obj[key] = value
        end += 1
        nextchar = s[end:end+1]
        print 'obj[%r] = %r' % (key, value)
        while is_whitespace(nextchar):
            end += 1
            nextchar = s[end:end+1]

        print 'nextchar: %s' % nextchar
        if nextchar == ',':
            _print('Found comma! Continuing...')
            continue
        elif nextchar == '}':
            break

    return obj, end


def parse_object_value(s, end=0):
    """
    Allowed return values: object, array, string, number, null
    """
    def _print(st=''):
        print '[parse_object_value] %s' % st

    nextchar = s[end:end+1]
    _print('nextchar: %s    end: %s' % (nextchar, end))
    value = None
    if nextchar == '{':
        value, end = parse_object(s, end=end)
    elif nextchar == '[':
        value, end = parse_array(s, end=end)
    elif nextchar == '"':
        value, end = parse_string(s, end=end)
    elif re.match(r'\d', nextchar):
        value, end = parse_number(s, end=end)
    else:
        raise Exception("Don't know how to parse value starting with %s" %
                        nextchar)

    return value, end


def parse_array(s, end=0):
    def _print(st):
        print u'[parse_array] %s' % st

    assert s, "s is empty"
    nextchar = s[end:end+1]
    while is_whitespace(nextchar):
        end += 1
        nextchar = s[end:end+1]
        assert nextchar, 'Reached the end of s without finding non-whitespace'

    assert nextchar == '[', 'Expected %r, got %r instead' % ('[', nextchar)
    end += 1
    nextchar = s[end:end+1]
    assert nextchar

    values = []
    # Add things to `values`
    while nextchar:
        if is_whitespace(nextchar):
            end += 1
            nextchar = s[end:end+1]
            continue

        # end of array
        if nextchar == ']':
            break

        # number
        if re.match(r'\d', nextchar):
            num, end = parse_number(s, end)
            values.append(num)

        # array
        if nextchar == '[':
            array, end = parse_array(s, end=end)
            values.append(array)

        # string
        if nextchar == '"':
            # start parsing string
            st, end = parse_string(s, end=end)
            values.append(st)
        end += 1
        nextchar = s[end:end+1]

    return values, end


def parse_string(s, end=0):
    assert s, "s is empty"
    nextchar = s[end:end+1]
    assert nextchar == '"', 'parse_string() called for a non-string'
    value = ''
    end += 1
    nextchar = s[end:end+1]
    escape = False
    while nextchar:
        if nextchar == '\\' and not escape:
            escape = True
            end += 1
            nextchar = s[end:end+1]
            continue
        if nextchar == '"':
            if escape:
                escape = False
            else:
                break
        value += nextchar
        end += 1
        nextchar = s[end:end+1]
    return value, end


def parse_number(s, end=0):
    def _print(st):
        print u'[parse_number] %s' % st

    assert s, 's is empty'
    nextchar = s[end:end+1]
    # if we're parsing a number, it has to start with a digit
    assert re.match(r'\d', nextchar)
    value = ''
    while nextchar:
        if re.match(r'(\d|\.)', nextchar):
            value += nextchar
            end += 1
            nextchar = s[end:end+1]
        else:
            break
    return float(value) if '.' in value else int(value), end - 1


def is_whitespace(char):
    return char and char in ' \t\n\r'


if __name__ == '__main__':
    assert parse_array('[]')[0] == []
    assert parse_array(r'["Riley", "Watkins","\"Quoted\""]')[0] == ['Riley', 'Watkins', '"Quoted"']
    assert parse_array(r'[["a", "b"], ["c", "d", ["e"]]]')[0] == [['a', 'b'], ['c', 'd', ['e']]]
    assert parse_array('[1, 2, 3]')[0] == [1, 2, 3]
    assert parse_array('[1.0, [2, 3.45], "6.0"]')[0] == [1.0, [2, 3.45], '6.0']
