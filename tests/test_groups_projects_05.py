#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from nose.tools import *
sys.path.append('./config')
from lib_user_mng import *
from lib_projects import *
import config  # pylint: disable=unused-import
from config import *

# https://gitlab.ispras.ru/svace-services/support/-/issues/2731

temp_part = get_temp_name()

user_login = 'user_group_projects_05_' + temp_part
user_pw = 'test_user'
project_group = 'group_project_' + temp_part
role_name = 'role_groups_projects_05_' + temp_part


def test_delete_project_group():  # 2731
    open_group_settings()
    create_project_group(project_group, "bash")
    close_group_settings()
    open_tab_in_user_mng_page('Roles')
    click("//div[@id = 'workspace-settings-panel']//span[text() = 'Create']")
    # enter data
    set_text(xpath_role_dialog + "//*[contains(label/text(), 'Name')]//input[@placeholder = 'Enter role name']", role_name)
    click(f"//div[@class='role-form-area']//label[text()='Project groups setup']")
    click_add_permission_button()
    select_permission_project_group()
    # select project
    select_project_group_in_permission(project_group)
    click("//table[@id = 'project-permissions-table']//label[contains(@class, 'bp5-checkbox')]/span")
    click_button_in_dialog("Create")
    add_user(user_login, user_pw, roles=role_name)
    relogin(user_login, user_pw)
    open_group_settings()
    delete_project_group(project_group)
    login(user_login, user_pw)
    select_top_menu("Review")
    click(xpath_menu('projects'))
    # Check that the list is empty
    waitForXpath("//div[text() = 'No results.']")
    waitForXpath("//span[@id='markers-count']//div[text() = '#: 0']")
    relogin()


def test_cleanup_delete_role():
    delete_role(role_name)


def test_cleanup_delete_user():
    delete_user(user_login)
