import re


def loads(s):
    return parse_array(s)[0]


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
