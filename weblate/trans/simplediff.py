# Simple Diff for Python v 0.1
# (C) Paul Butler 2008 <http://www.paulbutler.org/>
# May be used and distributed under the zlib/libpng license
# <http://www.opensource.org/licenses/zlib-license.php>


def diff(old, new):
    """
    Find the differences between two lists. Returns a list of pairs, where
    the first value is in ['+','-','='] and represents an insertion, deletion,
    or no change for that list. The second value of the pair is the list of
    elements.
    """
    ohash = {}

    # Build a hash map with elements from old as keys, and
    # a list of indexes as values
    for i, val in enumerate(old):
        ohash.setdefault(val,[]).append(i)

    # Find the largest substring common to old and new
    last_row = [0] * len(old)
    sub_start_old = sub_start_new = sub_length = 0
    for j, val in enumerate(new):
        thisRow = [0] * len(old)
        for k in ohash.setdefault(val,[]):
            thisRow[k] = (k and last_row[k - 1]) + 1
            if(thisRow[k] > sub_length):
                sub_length = thisRow[k]
                sub_start_old = k - sub_length + 1
                sub_start_new = j - sub_length + 1
        last_row = thisRow
    if sub_length == 0:
        # If no common substring is found, assume that an insert and
        # delete has taken place...
        return (old and [('-', old)] or []) + (new and [('+', new)] or [])
    else:
        # ...otherwise, the common substring is considered to have no change,
        # and we recurse on the text before and after the substring
        return (
            diff(
                old[:sub_start_old],
                new[:sub_start_new]
            ) +
            [('=', new[sub_start_new:sub_start_new + sub_length])] +
            diff(
                old[sub_start_old + sub_length:],
                new[sub_start_new + sub_length:]
            )
        )


def stringDiff(old, new):
    """
    Returns the difference between the old and new strings when split on
    whitespace. Considers punctuation a part of the word
    """
    return diff(old.split(), new.split())


def htmlDiff(old, new):
    """
    Returns the difference between two strings (as in stringDiff) in
    HTML format.
    """
    con = {'=': (lambda x: x),
           '+': (lambda x: "<ins>" + x + "</ins>"),
           '-': (lambda x: "<del>" + x + "</del>")}
    return "".join([(con[a])("".join(b)) for a, b in diff(old, new)])

#Examples:
#print htmlDiff("The world is a tragedy to those who feel, but a comedy to those who think",
# "Life is a tragedy for those who feel, and a comedy to those who think") # Horace Walpole

#print htmlDiff("I have often regretted my speech, never my silence",
# "I have regretted my speech often, my silence never") # Xenocrates
