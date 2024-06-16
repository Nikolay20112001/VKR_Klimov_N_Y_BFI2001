#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from nose.tools import *
sys.path.append('./config')
from lib_user_mng import *
import config  # pylint: disable=unused-import
from config import *

# https://gitlab.ispras.ru/svace-services/support/-/issues/2727

temp_part = get_temp_name()
project = 'test_project_01_' + temp_part
branch = 'master'
new_branch = 'master' + temp_part
snapshot = imported_snapshot_name = 'Snapshot 2020-03-25 09:09:41 +0300'
snap_file = 'Snapshot 2020-03-25 09 09 41 +0300.snap'

user_login = get_temp_name('test_user')
user_pw = 'test_user'

role_name = 'role_permissions_08' + temp_part


def preparation():
    load_snapshots_in(project, {imported_snapshot_name: snap_file})
    select_snapshot(snapshot)


def test_delete_project_permission_with_new_branch():  # 2727
    preparation()
    # creating a role with access to the uploaded project and with server access to create projects
    add_role(role_name, project, server_perms="Create projects")
    # creating a user and assigning them a role
    add_user(user_login, user_pw, roles=role_name)
    # log in under the created user
    relogin(user_login, user_pw)
    select_top_menu("Projects")
    # creating a new branch in the project
    invoke_project_action(project, "Create branch")
    set_text("//input[@placeholder = 'Enter branch name']", new_branch)
    click_button_in_dialog('Create')
    import_snapshot(snap_file, imported_snapshot_name)
    select_top_menu("Review")
    select_project(project)
    # select the created branch
    select_branch(new_branch)
    select_snapshot(snapshot)
    # open chrome in private mode to remove access to the project through the admin
    open_chrome_browser_in_private_mode(server_url)
    # switch to the 2d browser
    activate_driver(1)
    time.sleep(1)  # do not remove
    # log in under the admin
    login()
    select_top_menu("Settings")
    open_roles()
    invoke_role_action(role_name, "Edit")
    # deleting access to the project
    click(f"//table[@id = 'project-permissions-table']//tbody[//tr//div[text() = '{project}']]//span[contains(@class, 'bp5-icon-trash')]")
    click_button_in_dialog("Save")
    # switch to the first browser
    activate_driver(0)
    time.sleep(1)
    # log in again under the created user (since it was automatically thrown out)
    login(user_login, user_pw)
    # open the project selection menu
    click("//div[@id = 'breadcrumb-panel']//div[text() = 'Select project']")
    # check that there is no project that we have removed
    waitForXpath("//div[contains(@class, 'bp5-popover-appear-done')]//ul//div[text() = 'No results.']")
    # check that the panel with markers is empty
    waitForXpath("//span[@id='markers-count']//div[text() = '#: 0']")


def test_cleanup_delete_user():
    del_tmp_user(user_login)


def test_cleanup_delete_project():
    delete_project(project)
