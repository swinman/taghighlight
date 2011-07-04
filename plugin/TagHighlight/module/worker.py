from __future__ import print_function
import sys
import os
from .options import AllOptions

def RunWithOptions(options):
    from .config import config, SetInitialOptions, LoadLanguages

    SetInitialOptions(options)

    if config['cscope_dir'] is not None:
        config['cscope_exe_full'] = config['cscope_dir'] + '/' + 'cscope'

    if config['use_existing_tagfile'] and not os.path.exists(config['ctags_file']):
        config['use_existing_tagfile'] = False

    LoadLanguages()

    if config['print_py_version']:
        print(sys.version)
        return

    from .cscope import GenerateCScopeDBIfRequired
    from .ctags import GenerateTags, ParseTags
    from .generation import CreateTypesFile

    GenerateCScopeDBIfRequired(config)

    if not config['use_existing_tagfile']:
        GenerateTags(config)
    tag_db = ParseTags(config)

    for language in config['language_list']:
        if language in tag_db:
            CreateTypesFile(config, language, tag_db[language])
