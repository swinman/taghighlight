from class_interface import LanguageClassInterface

class Language(LanguageClassInterface):
    def __init__(self, options):
        self.options = options

    def GetParameters(self):
        params = {
                'suffix': 'py',
                'name': 'python',
                'extensions': r'pyw?',
                }
        return params

    def GetCTagsOptions(self):
        return []

    def GetCTagsLanguageName(self):
        return 'python'

    @staticmethod
    def GetFriendlyLanguageName():
        return 'python'
