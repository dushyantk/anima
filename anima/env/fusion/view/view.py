import PeyeonScript


class form():
	def __init__(self):
		self.dialog = {}
		self.fusion = PeyeonScript.scriptapp("Fusion")
		self.comp = self.fusion.GetCurrentComp()

	def AskUser(self, name, value,whichDialog):
		self.dialog[0] = {1: {1: "Path", 2: "ClipBrowse", "Name": "Select file of the "+name, "Default": value}}
		self.dialog[1] = {1: {1: "project",	2: "Dropdown", 'Name': "Project:", 'Options': value, "Default": 0}}
		self.dialog[2] = {1: {1: "sequence",	2: "Dropdown", 'Name': "Sequence :", 'Options': value, "Default": 0}}
		return self.comp.AskUser("QuickEdit - "+name, self.dialog[whichDialog])
