#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from nose.tools import *
sys.path.append('./config')
from lib_user_mng import *
import config  # pylint: disable=unused-import
from config import *
# https://gitlab.ispras.ru/svace-services/support/-/issues/2193

temp_part = get_temp_name()
role_name = "role_" + temp_part
project_group_01 = "project_group_01_" + temp_part
project_group_02 = "project_group_02_" + temp_part
project_group_03 = "project_group_03_" + temp_part


def test_create_project_groups():
    select_top_menu("Projects")
    open_group_settings()
    create_project_group(project_group_01)
    create_project_group(project_group_02)
    create_project_group(project_group_03)
    close_group_settings()


def test_add_group_in_project_permissions():
    open_roles()
    click("//div[@id = 'workspace-settings-panel']//span[text() = 'Create']")
    time.sleep(1)  # do not remove
    set_text(xpath_role_dialog + "//label[contains(text(), 'Name')]/following-sibling::div//input[@placeholder = 'Enter role name']", role_name)
    click_add_permission_button()
    select_permission_project_group()
    select_project_group_in_permission(project_group_01)
    waitForXpath(f"//table[@id = 'project-permissions-table']//div[text() = '{project_group_01}']")
    click_button_in_dialog("Create")


def test_show_permissions():
    show_permissions(role_name)
    waitForXpath(f"//h6//span[contains(text(), '{role_name}')]")
    waitForXpath("//h6//span[contains(text(), 'Role permissions')]")
    waitForXpath(f"//table[@id = 'project-permissions-table']//div[text() = '{project_group_01}']")
    click("//div[@class = 'bp5-dialog-header']//button")


def test_cleanup_delete_role():
    delete_role(role_name)


def test_delete_projects_groups():
    open_group_settings()
    delete_project_group(project_group_02)
    delete_project_group(project_group_03)
