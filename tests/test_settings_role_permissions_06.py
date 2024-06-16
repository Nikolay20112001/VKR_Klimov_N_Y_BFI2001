#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from nose.tools import *
sys.path.append('./config')
from lib_user_mng import *
import config  # pylint: disable=unused-import
from config import *
# https://gitlab.ispras.ru/svace-services/support/-/issues/2369
# https://gitlab.ispras.ru/svace-services/support/-/issues/2406

temp_part = get_temp_name()
role_name = "role_" + temp_part
project_group_01 = "a_" + temp_part
project_group_02 = "ab_" + temp_part
project_group_03 = "b_" + temp_part
project_group_04 = "c_" + temp_part


def test_add_project_groups_to_sort():  # 2369
    select_top_menu("Projects")
    open_group_settings()
    create_project_group(project_group_01)
    create_project_group(project_group_02)
    create_project_group(project_group_03)
    create_project_group(project_group_04)
    close_group_settings()
    open_roles()
    click("//div[@id = 'workspace-settings-panel']//span[text() = 'Create']")
    time.sleep(1)  # do not remove
    set_text(xpath_role_dialog + "//label[contains(text(), 'Name')]/following-sibling::div//input[@placeholder = 'Enter role name']", role_name)
    click_add_permission_button()
    select_permission_project_group()
    select_project_group_in_permission(project_group_04)
    click_add_permission_button()
    select_permission_project_group()
    select_project_group_in_permission(project_group_03)
    click_add_permission_button()
    select_permission_project_group()
    select_project_group_in_permission(project_group_01)
    click_add_permission_button()
    select_permission_project_group()
    select_project_group_in_permission(project_group_02)
    click_add_permission_button()  # start 2406
    select_permission_project_group()
    click("//table[@id='project-permissions-table']//button/span[text() = 'Select project group']")
    set_text("//div[contains(@class, 'bp5-popover-enter-done')]//input[@placeholder = 'Search']", project_group_01)
    time.sleep(1)
    waitForXpathDisappear("//ul[contains(@class, 'menu')]//li//a/div[text() = '" + project_group_01 + "']")  # end 2406
    click_button_in_dialog("Create")


def test_sort_project_groups():  # 2369
    show_permissions(role_name)
    waitForXpath(f"//table[@id='project-permissions-table']//tbody//tr[1][td//div/text() = '{project_group_01}']")
    waitForXpath(f"//table[@id='project-permissions-table']//tbody//tr[2][td//div/text() = '{project_group_02}']")
    waitForXpath(f"//table[@id='project-permissions-table']//tbody//tr[3][td//div/text() = '{project_group_03}']")
    waitForXpath(f"//table[@id='project-permissions-table']//tbody//tr[4][td//div/text() = '{project_group_04}']")
    click("//div[@class = 'bp5-dialog-header']//button")


def test_sort_after_cloning_role():  # 2369
    invoke_role_action(role_name, "Create copy")
    show_permissions(role_name + '_1')
    waitForXpath(f"//table[@id='project-permissions-table']//tbody//tr[1][td//div/text() = '{project_group_01}']")
    waitForXpath(f"//table[@id='project-permissions-table']//tbody//tr[2][td//div/text() = '{project_group_02}']")
    waitForXpath(f"//table[@id='project-permissions-table']//tbody//tr[3][td//div/text() = '{project_group_03}']")
    waitForXpath(f"//table[@id='project-permissions-table']//tbody//tr[4][td//div/text() = '{project_group_04}']")
    click("//div[@class = 'bp5-dialog-header']//button")


def test_cleanup_delete_role():
    delete_role(role_name)


def test_delete_projects_groups():
    open_group_settings()
    delete_project_group(project_group_01)
    delete_project_group(project_group_02)
    delete_project_group(project_group_03)
    delete_project_group(project_group_04)
