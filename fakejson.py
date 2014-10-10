def parse_array(s, end=0):
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
            return values, end

        # array
        if nextchar == '[':
            array, end = parse_array(s, end=end)
            print 'appending array: %s' % array
            values.append(array)

        print 'checking string'
        # string
        if nextchar == '"':
            # start parsing string
            print 'parsing string'
            st, end = parse_string(s, end=end)
            values.append(st)
        end += 1
        nextchar = s[end:end+1]


def parse_string(s, end=0):
    assert s, "s is empty"
    nextchar = s[end:end+1]
    assert nextchar == '"', 'parse_string() called for a non-string'
    value = ''
    end += 1
    nextchar = s[end:end+1]
    escape = False
    while nextchar:
        print nextchar
        if nextchar == '\\' and not escape:
            print 'found escape character'
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
    print 'parsed string: %s' % value
    return value, end


def is_whitespace(char):
    return char and char in ' \t\n\r'


if __name__ == '__main__':
    print repr(parse_array('[]'))
    print repr(parse_array(r'["Riley", "Watkins","\"Quoted\""]'))
    print repr(parse_array(r'[["a", "b"], ["c", "d", ["e"]]]'))
