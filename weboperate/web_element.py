# -*- coding:utf-8 -*-  

class page_element:
    '''
    use xpath find the web element.
    '''
    def __init__(self):
        pass
    
    def _name_not_none(self, name):
        pass
    
    def _get_logout_element(self, name):
        xpath = '//*[@title=\'%s\']' % str(name)
        return xpath    
    
    def _get_classification_element(self, name):
        self._name_not_none(name)
        xpath = '//*[@id=\'headnavli\']//li[text()=\'%s\']' % str(name)
        return xpath

    def _get_module_element(self, name):
        self._name_not_none(name)
        xpath = '//*[@id=\'page_all_conetent\']//span[contains(text(),\'%s\')]' % str(name)
        return xpath

    def _get_function_element(self, name):
        self._name_not_none(name)
        xpath = '//*[@id=\'page_all_conetent\']//li[contains(text(),\'%s\')]' % str(name)
        return xpath

    def _get_header_element(self, name):
        self._name_not_none(name)
        xpath = '//a[contains(text(),\'%s\')]' % str(name)
        return xpath
    
    def _get_iframe_menu_element(self, name):
    #新建
        self._name_not_none(name)
        xpath = '//span/span[contains(text(),\'%s\')]' % str(name)
        return xpath
    
    def _get_iframe_select_element(self, name=None, value=None):
    #下拉框
        print(self._name_not_none(name))
        print(self._name_not_none(value))
        if name == None :
            xpath_name = '//option[text()=\'%s\']/parent::*' % value
            xpath_value = '//option[text()=\'%s\']' % value
        else:
            xpath_name = '//*[text()=\'%s\']/following-sibling::*/select' % name
            xpath_value = '//option[text()=\'%s\']' % value
        return xpath_name,xpath_value
    
    def _get_iframe_input_box_element(self, name):
    #输入框
        self._name_not_none(name)
        xpath = '//*[text()=\'%s\']/following-sibling::td//input' % name
        return xpath
  
    def _get_iframe_input_file_element(self, name):
    #文件选择框
        self._name_not_none(name)
        xpath = '//*[@id="%s"]' % name
        return xpath
    
    def _get_iframe_submit_options_element(self, name):
    #提交
        self._name_not_none(name)
        xpath = '//*[@id="avupdate_form"]/span/input[4]'
        return xpath
 
    def _get_result_element(self, name):
    #提交
        self._name_not_none(name)
        xpath = '//*[@id="baseinfodiv2"]/li[9][contains(text(),\'%s\')]' % (name)
        return xpath
   
    def _get_iframe_conf_checkbox_element(self, name):
    #配置复选框
        self._name_not_none(name)
        xpath = '//*[contains(text(),\'%s\')]/following-sibling::*//*[@type=\'checkbox\'] | //*[text()=\'%s\']/*[@type=\'checkbox\']' % (name,name)
        return xpath
      
    def _get_iframe_radio_element(self, name):
    #单选框
        self._name_not_none(name)
        xpath = '//label[text()=\'%s\']/preceding-sibling::*[@type=\'radio\']' % name
        return xpath   
    
if __name__ == '__main__':
    pass