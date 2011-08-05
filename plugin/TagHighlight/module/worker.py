#!/usr/bin/env python
# Tag Highlighter:
#   Author:  A. S. Budden <abudden _at_ gmail _dot_ com>
#   Date:    05/08/2011
# Copyright: Copyright (C) 2009-2011 A. S. Budden
#            Permission is hereby granted to use and distribute this code,
#            with or without modifications, provided that this copyright
#            notice is copied with it. Like anything else that's free,
#            the TagHighlight plugin is provided *as is* and comes with no
#            warranty of any kind, either expressed or implied. By using
#            this plugin, you agree that in no event will the copyright
#            holder be liable for any damages resulting from the use
#            of this software.

# ---------------------------------------------------------------------
from __future__ import print_function
import sys
import os

def RunWithOptions(options):
    from .config import config, SetInitialOptions, LoadLanguages
    from .debug import Debug

    SetInitialOptions(options)

    Debug("Running types highlighter generator", "Information")
    Debug("Release:" + config['release'], "Information")
    Debug("Version:" + repr(config['version']), "Information")

    if config['use_existing_tagfile'] and not os.path.exists(config['ctags_file']):
        config['use_existing_tagfile'] = False

    LoadLanguages()

    if config['print_config']:
        import pprint
        pprint.pprint(config)
        return

    if config['print_py_version']:
        print(sys.version)
        return

    from .ctags_interface import GenerateTags, ParseTags
    from .generation import CreateTypesFile

    if not config['use_existing_tagfile']:
        GenerateTags(config)
    tag_db = ParseTags(config)

    for language in config['language_list']:
        if language in tag_db:
            CreateTypesFile(config, language, tag_db[language])
