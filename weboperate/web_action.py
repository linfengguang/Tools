# -*- coding:utf-8 -*-
import sys
import time
from selenium import webdriver
from web_element import page_element

sys.path.append('G:\\code\\Tools\\configfile')
from configure_all import *


class web_action(object):
    browser = ''
    implicitly_wait = 5
    element = page_element()

    def __init__(self):
        pass

    def web_login(self, host=dut_host, user=dut_user, passwd=dut_passwd, profileDir=None):
        print("run keyword:%s " % (sys._getframe().f_code.co_name))
        print('open chrome browser')
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(self.implicitly_wait)
        host = 'http://' + host
        print("browser open url %s" % host)
        self.browser.get(host)
        self.browser.find_element_by_name("usr").send_keys(user)
        self.browser.find_element_by_name("pwd").send_keys(passwd)
        self.browser.find_element_by_tag_name("button").click()
        print("login %s" % host)

    def web_close_alert(self):
        print("run keyword:%s" % (sys._getframe().f_code.co_name))
        print('click accept alert')
        self.browser.switch_to_alert().accept()

    def web_logout(self, name):
        print("run keyword:%s" % (sys._getframe().f_code.co_name))
        self.browser.refresh()
        self.browser.find_element_by_xpath(
            self.element._get_logout_element(name)).click()
        self.browser.quit()
        print("logout and close browser")

    def _features_page(self, path):
        '''
        进入到功能页面，格式 分类-模块-功能-子功能，最多四级

        '''
        path = path.split('-')
        print(path)
        self.browser.switch_to.parent_frame()  # 进入到iframe后回到进入前的界面
        self.browser.switch_to_default_content()  # 进入到iframe后回到root界面
        print("into page %s" % str('-'.join(path)))
        self.browser.refresh()  # 刷新页面
        if len(path) >= 2:
            self.browser.find_element_by_xpath(
                self.element._get_classification_element(path[0])).click()
            self.browser.find_element_by_xpath(
                self.element._get_module_element(path[1])).click()
            if len(path) >= 3:
                self.browser.find_element_by_xpath(
                    self.element._get_function_element(path[2])).click()
                if len(path) == 4:
                    time.sleep(1)
                    self.browser.switch_to_frame("Main_con")
                    self.browser.find_element_by_xpath(
                        self.element._get_header_element(path[3])).click()
        else:
            raise ExpectError("number of args is error ,please check.")

    def _status_check(self, name, status, expect, message=None):
        if str(status) == str(expect):
            print("status check Success , %s current status : %s,  expect status : %s" % (
                name, status, expect))
        else:
            if message == None:
                raise ExpectError("status check False , %s current status : %s,  expect status : %s" % (
                    name, status, expect))
            else:
                raise ExpectError("status check False , %s current status : %s,  expect status : %s  message=%s" % (
                    name, status, expect, message))

    def _iframe_input_box(self, name, path, value):
        print("input box %s %s" % (name, value))
        element = self.browser.find_element_by_xpath(
            self.element._get_iframe_input_file_element(name))
        element.send_keys("%s%s" % (path, value))

    def _iframe_submit_options(self, option):
        '''
        确定/提交/取消等按钮操作。
        '''
        print("click %s button" % option)
        self.browser.find_element_by_xpath(
            self.element._get_iframe_submit_options_element(option)).click()

if __name__ == '__main__':
    avversion = '%s-%s.avc' % (av_version, av_newversion)
    a = web_action()
    a.web_login()
    a._features_page(av_update_page_path)
    time.sleep(5)
    a._iframe_input_box(av_update_file_box, avfile_path, avversion)
    time.sleep(1)
    a._iframe_submit_options(av_update_submit_button)
    print('...30s...')
    time.sleep(30)
    a.web_close_alert()
    a.web_logout(web_logout_button)
