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
        _print('nextchar: %s    end: %s' % (nextchar, end))
        if is_whitespace(nextchar):
            end += 1
            nextchar = s[end:end+1]
            continue

        # end of array
        if nextchar == ']':
            break

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


def is_whitespace(char):
    return char and char in ' \t\n\r'


if __name__ == '__main__':
    print repr(parse_array('[]'))
    print repr(parse_array(r'["Riley", "Watkins","\"Quoted\""]'))
    print repr(parse_array(r'[["a", "b"], ["c", "d", ["e"]]]'))
