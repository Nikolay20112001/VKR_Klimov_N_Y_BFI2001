#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from nose.tools import *
sys.path.append('./config')
from config import *

# https://gitlab.ispras.ru/svace-services/support/-/issues/3053
# https://gitlab.ispras.ru/svace-services/support/-/issues/3045
# https://gitlab.ispras.ru/svace-services/support/-/issues/3052
# https://gitlab.ispras.ru/svace-services/support/-/issues/3130

project = get_temp_name('test_source_code_comments')
branch = 'master'
snapshot = imported_snapshot_name_01 = 'Snapshot 2020-03-25 09:09:41 +0300'
snap_file_01 = 'Snapshot 2020-03-25 09 09 41 +0300.snap'  # paho


def preparation():
    load_snapshots_in(project, {imported_snapshot_name_01: snap_file_01})
    select_snapshot(snapshot)


def test_show_comment_when_function_collapsed():  # 3053
    preparation()
    select_marker("test2.c", "280")
    element_01 = waitForXpath("//div[@class = 'view-lines monaco-mouse-cursor-text']//div[@class = 'view-line']//span[contains(text(), '!=')]")
    actions().context_click(element_01).perform()
    time.sleep(0.5)  # do not remove
    add_comment_context_command()
    set_text("//div[@role = 'dialog']//textarea[@placeholder = 'Enter comment']", "$$$")
    click("//div[@role = 'dialog']//span[text() = 'Save']")
    element_02 = waitForXpath(
        "(//div[@class = 'view-lines monaco-mouse-cursor-text']//div[@class = 'view-line']//span[contains(text(), 'lock_mutex')])[1]")
    actions().context_click(element_02).perform()
    time.sleep(0.5)  # do not remove
    add_comment_context_command()
    set_text("//div[@role = 'dialog']//textarea[@placeholder = 'Enter comment']", "@@@")
    click("//div[@role = 'dialog']//span[text() = 'Save']")
    time.sleep(0.5)
    move_to("//div[contains(@class, 'line-numbers') and text() = '278']")
    time.sleep(0.5)
    click("//div[contains(@class, 'line-numbers') and text() = '278']/preceding-sibling::div[contains(@class, 'folding-expanded')]")
    time.sleep(1)
    waitForXpathDisappear("//div[contains(@class, 'line-numbers') and text() = '280']")
    waitForXpathDisappear("//div[span//div[text() = '$$$']]")
    waitForXpath("//div[span//div[text() = '@@@']]")
    click("//div[@role = 'code']//button[@title = '1 comment']")
    waitForXpathDisappear("//div[span//div[text() = '@@@']]")
    click("//div[@role = 'code']//button[@title = '1 comment']")
    waitForXpath("//div[span//div[text() = '@@@']]")


def test_add_comment_by_button():  # 3045
    move_to("//div[contains(@class, 'line-numbers') and text() = '278']")
    time.sleep(0.5)
    click("//div[contains(@class, 'line-number') and text() = '278']/preceding-sibling::div[contains(@class, 'folding-collapsed')]")
    time.sleep(0.5)
    click("//div[span//div[text() = '$$$']]//button[@title = 'Add comment']")
    set_text("//div[@role = 'dialog']//textarea[@placeholder = 'Enter comment']", "###")
    click("//div[@role = 'dialog']//span[text() = 'Save']")
    waitForXpath("//div[span//div[text() = '###']]")
    waitForXpath(f"//div[span//div[text() = '###']]//div[text() = '{SVACER_DEFAULT_LOGIN}']")
    waitForXpath("//div[span//div[text() = '###']]//button[@title = 'Add comment']")
    waitForXpath("//div[span//div[text() = '###']]//button[@title = 'Edit']")
    waitForXpath("//div[span//div[text() = '###']]//button[@title = 'Delete']")


def test_delete_first_comment():  # 3052
    click("//div[span//div[text() = '$$$']]//button[@title = 'Delete']")
    time.sleep(0.5)  # do not remove
    waitForXpathDisappear("//div[span//div[text() = '$$$']]")


def test_delete_project_after_collapse_function():  # 3130
    time.sleep(0.5)  # do not remove
    click("//div[div[contains(@class, 'line-numbers') and text() = '278']]")
    time.sleep(0.5)  # do not remove
    click("//div[div[contains(@class, 'line-numbers') and text() = '278']]//div[@title = 'Click to collapse the range.']")


def test_cleanup_delete_project():  # 3130
    delete_project(project)
