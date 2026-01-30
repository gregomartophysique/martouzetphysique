class TemplateBuild:
	def __init__(self, template_file, begin_key='#<', end_key='>#', encoding="utf-8"):
		self.begin_key = begin_key
		self.end_key = end_key
		with open( template_file, encoding=encoding ) as f:
			self.lignes_template = f.readlines()
	
	def save(self, file_name, data):
		lignes = [ self._search_( l, data ) for l in self.lignes_template ]
		
		with open( file_name, 'w', encoding="utf-8" ) as f:
			for ligne in lignes:
				f.write( ligne )
		
		
	def _search_( self, line, data ):
		#line = line.copy()
		while (begin := line.find( self.begin_key )) != -1 :
			end = line.find( self.end_key )
			key = line[begin+2:end]
			if key in data:
				v = data[key]
			else:
				v = '-0-'
				print( 'Erreur de clef dans le template :', key)  
			line = line[:begin]+str(v)+line[end+len(self.begin_key):]
		return line
