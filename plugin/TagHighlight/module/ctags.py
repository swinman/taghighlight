from __future__ import print_function
import subprocess
import os
import re
import glob
from .utilities import DictDict
from .languages import Languages

field_processor = re.compile(
r'''
    ^                 # Start of the line
    (?P<keyword>.*?)  # Capture the first field: everything up to the first tab
    \t                # Field separator: a tab character
    .*?               # Second field (uncaptured): everything up to the next tab
    \t                # Field separator: a tab character
    (?P<search>.*?)   # Any character at all, but as few as necessary (i.e. catch everything up to the ;")
    ;"                # The end of the search specifier (see http://ctags.sourceforge.net/FORMAT)
    (?=\t)            # There MUST be a tab character after the ;", but we want to match it with zero width
    .*\t              # There can be other fields before "kind", so catch them here.
                      # Also catch the tab character from the previous line as there MUST be a tab before the field
    (kind:)?          # This is the "kind" field; "kind:" is optional
    (?P<kind>\w)      # The kind is a single character: catch it
    (\t|$)            # It must be followed either by a tab or by the end of the line
    .*                # If it is followed by a tab, soak up the rest of the line; replace with the syntax keyword line
''', re.VERBOSE)

def GenerateTags(options):
    print("Generating Tags")

    args = GetCommandArgs(options)

    ctags_cmd = [options['ctags_exe_full']] + args

    #subprocess.call(" ".join(ctags_cmd), shell = (os.name != 'nt'))
    subprocess.call(ctags_cmd)

    tagFile = open(options['ctags_file'], 'r')
    tagLines = [line.strip() for line in tagFile]
    tagFile.close()

    # Also sort the file a bit better (tag, then kind, then filename)
    tagLines.sort(key=ctags_key)

    tagFile = open(options['ctags_file'], 'w')
    for line in tagLines:
        tagFile.write(line + "\n")
    tagFile.close()

def ParseTags(options):
    """Function to parse the tags file and generate a dictionary containing language keys.

    Each entry is a list of tags with all the required details.
    """
    languages = options['language_handler']
    kind_list = languages.GetKindList()

    # Language: {Type: set([keyword, keyword, keyword])}
    ctags_entries = DictDict()

    lineMatchers = {}
    for key in languages.GetAllLanguages():
        lineMatchers[key] = re.compile(
                r'^.*?\t[^\t]*\.(?P<extension>' +
                languages.GetLanguageHandler(key)['PythonExtensionMatcher'] +
                ')\t')

    p = open(options['ctags_file'], 'r')
    while 1:
        line = p.readline()
        if not line:
            break

        for key, lineMatcher in list(lineMatchers.items()):
            if lineMatcher.match(line):
                # We have a match
                m = field_processor.match(line.strip())
                if m is not None:
                    try:
                        short_kind = 'ctags_' + m.group('kind')
                        kind = kind_list[key][short_kind]
                        keyword = m.group('keyword')
                        if options['parse_constants'] and \
                                (key == 'c') and \
                                (kind == 'CTagsGlobalVariable'):
                            if field_const.search(m.group('search')) is not None:
                                kind = 'CTagsConstant'
                        if short_kind not in languages.GetLanguageHandler(key)['SkipList']:
                            ctags_entries[key][kind].add(keyword)
                    except KeyError:
                        print("Unrecognised kind '{kind}' for language {language}".format(kind=m.group('kind'), language=key))
    p.close()

    return ctags_entries

def GetCommandArgs(options):
    args = []

    ctags_languages = [l['CTagsName'] for l in options['language_handler'].GetAllLanguageHandlers()]
    if 'c' in ctags_languages:
        ctags_languages.append('c++')
    args += ["--languages=" + ",".join(ctags_languages)]

    if options['ctags_file']:
        args += ['-f', options['ctags_file']]

    if not options['include_docs']:
        args += ["--exclude=docs", "--exclude=Documentation"]

    if options['include_locals']:
        kinds = options['language_handler'].GetKindList()
        def FindLocalVariableKinds(language_kinds):
            """Finds the key associated with a value in a dictionary.

            Assumes presence has already been checked."""
            return "".join(key[-1] for key,val in language_kinds.items() if val == 'CTagsLocalVariable')

        for language in ctags_languages:
            if language in kinds and 'CTagsLocalVariable' in kinds[language].values():
                args += ['--{language}-kinds=+{kind}'.format(language=language,
                    kind=FindLocalVariableKinds(kinds[language]))]

    # Must be last as it includes the file list:
    if options['recurse']:
        args += ['--recurse']
        args += ['.']
    else:
        args += glob.glob('*')

    return args

key_regexp = re.compile('^(?P<keyword>.*?)\t(?P<remainder>.*\t(?P<kind>[a-zA-Z])(?:\t|$).*)')

def ctags_key(ctags_line):
    match = key_regexp.match(ctags_line)
    if match is None:
        return ctags_line
    return match.group('keyword') + match.group('kind') + match.group('remainder')
