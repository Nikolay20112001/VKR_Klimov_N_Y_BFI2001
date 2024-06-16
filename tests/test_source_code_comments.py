#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from nose.tools import *
sys.path.append('./config')
from config import *

# https://gitlab.ispras.ru/svace-services/tests/-/issues/69
# https://gitlab.ispras.ru/svace-services/support/-/issues/3054

project = get_temp_name('test_source_code_comments')
branch = 'master'
snapshot = imported_snapshot_name_01 = 'Snapshot 2020-03-25 09:09:41 +0300'
snap_file_01 = 'Snapshot 2020-03-25 09 09 41 +0300.snap'  # paho


def preparation():
    load_snapshots_in(project, {imported_snapshot_name_01: snap_file_01})
    select_snapshot(snapshot)


def test_add_comment_ESC():
    preparation()
    select_marker("MQTTAsync.c", "1956")
    element = waitForXpath("//div[@class = 'view-lines monaco-mouse-cursor-text']//div[@class = 'view-line']//span[contains(text(), 'ListEmpty')]")
    actions().context_click(element).perform()
    time.sleep(1)  # do not remove
    add_comment_context_command()
    actions().send_keys(Keys.ESCAPE).perform()
    waitForXpathDisappear("//div[@role='dialog']//h6[text() = 'Add comment for MQTTAsync.c: 1956']")


def test_add_comment():
    element = waitForXpath("//div[@class = 'view-lines monaco-mouse-cursor-text']//div[@class = 'view-line']//span[contains(text(), 'ListEmpty')]")
    actions().context_click(element).perform()
    time.sleep(1)  # do not remove
    add_comment_context_command()
    set_text("//div[@role = 'dialog']//textarea[@placeholder = 'Enter comment']", "$$$")
    waitForXpath("//div[@role = 'dialog']//button[not(contains(@class, 'bp5-disabled'))]//span[text() = 'Save']")
    click("//div[@role = 'dialog']//span[text() = 'Save']")
    waitForXpathDisappear("//div[@role='dialog']//h6[text() = 'Add comment for MQTTAsync.c: 1956']")
    waitForXpath("//div[span//div[text() = '$$$']]")


def test_display_comment():  # 3054
    waitForXpath("//div[span//div[text() = '$$$']]")
    waitForXpath("//div[span//div[text() = '$$$']]//button[@title = 'Add comment']")
    waitForXpath("//div[span//div[text() = '$$$']]//button[@title = 'Edit']")
    waitForXpath("//div[span//div[text() = '$$$']]//button[@title = 'Delete']")


def test_add_another_comment():
    element = waitForXpath(
        "//div[@class = 'view-lines monaco-mouse-cursor-text']//div[@class = 'view-line']//span[contains(text(), 'TRACE_MINIMUM')]")
    actions().context_click(element).perform()
    time.sleep(1)  # do not remove
    add_comment_context_command()
    set_text("//div[@role = 'dialog']//textarea[@placeholder = 'Enter comment']", "@@@")
    waitForXpath("//div[@role = 'dialog']//button[not(contains(@class, 'bp5-disabled'))]//span[text() = 'Save']")
    click("//div[@role = 'dialog']//span[text() = 'Save']")
    waitForXpathDisappear("//div[@role='dialog']//h6[text() = 'Add comment for MQTTAsync.c: 1957']")
    waitForXpath("//div[span//div[text() = '@@@']]")
    waitForXpath("//div[span//div[text() = '$$$']]")


def test_display_comments():  # 3054
    waitForXpath("//div[span//div[text() = '$$$']]")
    waitForXpath("//div[span//div[text() = '$$$']]//button[@title = 'Add comment']")
    waitForXpath("//div[span//div[text() = '$$$']]//button[@title = 'Edit']")
    waitForXpath("//div[span//div[text() = '$$$']]//button[@title = 'Delete']")
    waitForXpath("//div[span//div[text() = '@@@']]")
    waitForXpath("//div[span//div[text() = '@@@']]//button[@title = 'Add comment']")
    waitForXpath("//div[span//div[text() = '@@@']]//button[@title = 'Edit']")
    waitForXpath("//div[span//div[text() = '@@@']]//button[@title = 'Delete']")


def test_edit_comment():
    waitForXpath("//div[span//div[text() = '$$$']]//button[@title = 'Edit']")
    click("//div[span//div[text() = '$$$']]//button[@title = 'Edit']")
    time.sleep(1)  # do not remove
    set_text("//div[@role = 'dialog']//textarea[@placeholder = 'Enter comment']", "$$$$")
    click("//div[@role = 'dialog']//span[text() = 'Save']")
    waitForXpath("//div[span//div[text() = '$$$$']]")
    waitForXpath("//div[span//div[text() = '$$$$']]//span[text() = 'edited']")


def test_edit_comment_ESC():
    click("//div[span//div[text() = '$$$$']]//button[@title = 'Edit']")
    time.sleep(1)  # do not remove
    actions().send_keys(Keys.ESCAPE).perform()
    waitForXpathDisappear("//div[@role='dialog']//h6[text() = 'Add comment for MQTTAsync.c: 1956']")


def test_delete_comment():
    waitForXpath("//div[span//div[text() = '$$$$']]//button[@title = 'Delete']")
    click("//div[span//div[text() = '$$$$']]//button[@title = 'Delete']")
    time.sleep(1)  # do not remove
    waitForXpathDisappear("//div[span//div[text() = '$$$$']]")


def test_cleanup_delete_project():
    delete_project(project)
