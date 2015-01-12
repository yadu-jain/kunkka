"""
"""
class Edit_Form(object):
	def __init__(self,update_fun,table_no):
		pass
		self.update_fun=update_fun
		self.update_fun=update_fun.replace("/","")
		self.table_no=table_no
	def get_form(self):		
		return {"url":"/report_ajax/"+self.update_fun+"/","table_no":self.table_no}

def get_edit_forms_config(data,form_configs):
	"""
	"""	
	counter=0
	forms=[]	
	for config in form_configs:
		table_no=config[0]
		update_fun=config[1]
		if len(data)>table_no:	
			forms.append(({},Edit_Form(update_fun,table_no).get_form()))			
	return forms

def get_changed_list(field,response):
	key_list=[]
	for key in field:
		if key in response["Table"][0]:
			key_list.append(key)
	return key_list
