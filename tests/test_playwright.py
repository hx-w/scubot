# -*- coding: utf-8 -*-

from playwright.sync_api import sync_playwright

with sync_playwright() as play:
    browser = play.chromium.launch()
    page = browser.new_page()
    page.goto("https://wfw.scu.edu.cn/ncov/wap/default/index")
    page.screenshot(path="test.png")
    browser.close()