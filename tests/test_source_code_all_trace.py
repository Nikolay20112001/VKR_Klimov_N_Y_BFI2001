#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from nose.tools import *
sys.path.append('./config')
from lib_user_mng import *
from lib_source_code import *
from config import *

# https://gitlab.ispras.ru/svace-services/support/-/issues/2844
# https://gitlab.ispras.ru/svace-services/support/-/issues/2019
# https://gitlab.ispras.ru/svace-services/support/-/issues/2845
# https://gitlab.ispras.ru/svace-services/support/-/issues/2453

tmp_part = get_temp_name()
user_login = 'test_all_trace' + tmp_part
user_pwd = 'test_user'

project = 'paho.mqtt.c' + tmp_part
branch = 'master'
snapshot = 'Snapshot 2020-03-25 09:09:41 +0300'
snap_file = 'Snapshot 2020-03-25 09 09 41 +0300.snap'  # paho
marker_file_name = "MQTTVersion.c"
marker_line_in_file = "218"


def preparation():
    load_snapshots_in(project, {snapshot: snap_file})
    select_snapshot(snapshot)


def test_switch_to_tmp_user():
    global user_login, user_pwd
    user_login, user_pwd = switch_to_tmp_admin()


def test_show_all_trace_option():  # 2844
    preparation()
    set_ui_setting("Code view|Reuse tab", dialog_action="open")
    click("//div[contains(@class, 'drawer')]//button//span[text() = 'Reset settings']")
    click("//div[contains(@class, 'settings-drawer')]//label[text() = \"Show marker's entire trace\"]")  # set "Show marker's entire trace"
    # check that the reset settings button is active
    waitForXpath("//div[contains(@class, 'drawer')]//button[not(disabled)]//span[text() = 'Reset settings']")
    close_user_dialog()


def test_show_all_trace_in_code_view():  # 2019 #2845
    select_marker(marker_file_name, marker_line_in_file)
    click("//div[contains(@class,'marker-in-code')]//button//span[contains(text(),'Show trace')]")
    # check that all the elements of the trace are displayed
    waitForXpath("//div[contains(@class,'trace-in-code')]//span[contains(@class,'intent-primary')]/span[text() = 'Trace 1.1']")
    waitForXpath("//div[contains(@class,'trace-in-code')]//span[contains(@class,'intent-primary')]/span[text() = 'Trace 2.1']")


def test_hide_trace_marker_button():  # 2453
    # check that the "Hide trace" button is present on the page near the marker
    waitForXpath("//div[contains(@class,'marker-in-code') and div/span[text() = 'TAINTED_PTR']]//button//span[contains(text(),'Hide trace')]")
    # click on the "Hide trace" button
    click("//div[contains(@class,'marker-in-code') and div/span[text() = 'TAINTED_PTR']]//button//span[contains(text(),'Hide trace')]")
    time.sleep(0.5)  # do not remove
    # check that the "Hide trace" button has changed to "Show trace"
    waitForXpath("//div[contains(@class,'marker-in-code') and div/span[text() = 'TAINTED_PTR']]//button//span[contains(text(),'Show trace')]")
    # check that all the elements of the trace have disappeared
    waitForXpathDisappear("//div[contains(@class,'trace-in-code')]//span[contains(@class,'intent-primary')]/span[text() = 'Trace 1.1']")
    waitForXpathDisappear("//div[contains(@class,'trace-in-code')]//span[contains(@class,'intent-primary')]/span[text() = 'Trace 2.1']")


def test_show_all_trace_off_in_code_view():  # 2019 #2845
    set_ui_setting("Code view|Show marker's entire trace", dialog_action="open")
    close_user_dialog()
    refresh()
    # click on the "Show trace" button
    click("//div[contains(@class,'marker-in-code')]//button//span[contains(text(),'Show trace')]")
    # check that the first element of the trace has been displayed
    waitForXpath("//div[contains(@class,'trace-in-code')]//span[contains(@class,'intent-primary')]/span[text() = 'Trace 1.1']")
    # check that the second element of the trace was not displayed
    safe_check.element("//div[contains(@class,'trace-in-code')]//span[contains(@class,'intent-primary')]/span[text() = 'Trace 2.2']").does_not_exist()
    safe_check.all_is_ok()


def test_hide_trace_by_hide_widjets_button():  # 2453
    # click on the "Hide all marker widgets" button
    click("//div[@id = 'code-panel']//*[@id='code-view-toolbar-hide-all-markers']")
    # click on the "Show all markers" button
    source_code_show_all_markers()
    # check that the marker is displayed
    waitForXpath("(//div[contains(@class,'marker-in-code') and div/span[text() = 'TAINTED_PTR']]//button//span[contains(text(),'Show trace')])[1]")
    # check that the trace of the marker was hidden
    waitForXpathDisappear("//div[contains(@class,'trace-in-code')]//span[contains(@class,'intent-primary')]/span[text() = 'Trace 1.1']")


def test_cleanup_delete_project():
    delete_project(project)


def test_delete_user():
    del_tmp_user(user_login)
