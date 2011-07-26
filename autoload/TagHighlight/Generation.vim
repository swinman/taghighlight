" Tag Highlighter:
"   Author:  A. S. Budden <abudden _at_ gmail _dot_ com>
"   Date:    25/07/2011
" Copyright: Copyright (C) 2009-2011 A. S. Budden
"            Permission is hereby granted to use and distribute this code,
"            with or without modifications, provided that this copyright
"            notice is copied with it. Like anything else that's free,
"            the TagHighlight plugin is provided *as is* and comes with no
"            warranty of any kind, either expressed or implied. By using
"            this plugin, you agree that in no event will the copyright
"            holder be liable for any damages resulting from the use
"            of this software.

" ---------------------------------------------------------------------
try
	if &cp || (exists('g:loaded_TagHLGeneration') && (g:plugin_development_mode != 1))
		throw "Already loaded"
	endif
catch
	finish
endtry
let g:loaded_TagHLGeneration = 1

function! TagHighlight#Generation#UpdateTypesFile(recurse, skiptags)
	let option_file_info = TagHighlight#Option#LoadOptionFileIfPresent()
	" Initial very simple implementation
	
	" Call any PreUpdate hooks
	let preupdate_hooks = TagHighlight#Option#GetOption('PreUpdateHooks')
	for preupdate_hook in preupdate_hooks
		exe 'call' preupdate_hook . '()'
	endfor
	
	" Start with a copy of the settings so that we can tweak things
	let RunOptions = TagHighlight#Option#CopyOptions()
	if a:recurse
		let RunOptions['Recurse'] = 1
	endif
	if a:skiptags
		let RunOptions['DoNotGenerateTags'] = 1
	endif

	" Most simple options are automatic.  The options below are
	" handled manually.
	
	" Find the ctags path
	let ctags_option = TagHighlight#Option#GetOption('CtagsExecutable')
	if ctags_option == 'None'
		" Option not set: search for 'ctags' in the path
		let RunOptions['CtagsExeFull'] = TagHighlight#RunPythonScript#FindExeInPath('ctags')
	elseif ctags_option =~ '[\\/]'
		" Option set and includes '/' or '\': must be explicit
		" path to named executable: just pass to mktypes
		let RunOptions['CtagsExeFull'] = ctags_option
	else
		" Option set but doesn't include path separator: search
		" in the path
		let RunOptions['CtagsExeFull'] = TagHighlight#RunPythonScript#FindExePath(ctags_option)
	endif

	let tag_file_info = TagHighlight#Find#LocateFile('TAGS', '')
	if tag_file_info['Found'] == 1
		let RunOptions['CtagsFileLocation'] = tag_file_info['Directory']
	endif

	let types_file_info = TagHighlight#Find#LocateFile('TYPES', '*')
	if types_file_info['Found'] == 1
		let RunOptions['TypesFileLocation'] = types_file_info['Directory']
	endif

	if ! has_key(RunOptions, 'SourceDir')
		" The source directory has not been set.  If a project config file was
		" found, use that directory.  If not, but a types file was found,
		" use that directory.  If not, but a tag file was found, use that
		" directory.  If not, use the current directory.
		if option_file_info['Found'] == 1
			let RunOptions['SourceDir'] = option_file_info['Directory']
		elseif types_file_info['Found'] == 1
			let RunOptions['SourceDir'] = types_file_info['Directory']
		elseif tag_file_info['Found'] == 1
			let RunOptions['SourceDir'] = tag_file_info['Directory']
		else
			let RunOptions['SourceDir'] = '.'
		endif
	endif
	
	call TagHighlight#RunPythonScript#RunGenerator(RunOptions)

	let postupdate_hooks = TagHighlight#Option#GetOption('PostUpdateHooks')
	for postupdate_hook in postupdate_hooks
		exe 'call' postupdate_hook . '()'
	endfor
endfunction
