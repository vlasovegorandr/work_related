import pytest
from pywinauto import application
from pywinauto.findwindows import ElementNotFoundError
from pytest_html import extras
from pathlib import Path
from datetime import datetime


@pytest.fixture()
def app_window(request):
    app = application.Application(backend='uia').connect(title='window title')
    window = app.window(title='window title')
    yield window
    # тут проверяется, что упал сам тест, а не всякие фикстуры/финализаторы
    if request.node.rep_call.failed:
        try:
            this_btn = window.child_window(auto_id='this button')
            this_btn.click_input()
        except ElementNotFoundError:
            pass
        try:
            that_btn = window.child_window(auto_id='that button')
            that_btn.click_input()
        except ElementNotFoundError:
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # item - объект теста, report.when - название текущего этапа теста ('setup', 'call', 'teardown'), report - отчет по тесту
    setattr(item, "rep_" + report.when, report)

    extra = getattr(report, 'extra', [])
    if report.when == 'call' and report.failed and not hasattr(report, 'wasxfail'):
        test_name = report.nodeid.split('::')[-1]
        screenshot_path = create_screenshot(test_name)
        extra.append(extras.png(screenshot_path))
    report.extra = extra


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # config.option - параметры, с которыми запускается тест ран
    if not config.option.htmlpath:
        current_datetime = datetime.now().strftime("%d.%m.%Y-%H.%M")
        reports_dir = Path('reports')
        reports_dir.mkdir(parents=True, exist_ok=True)
        report = reports_dir.joinpath(f'{current_datetime}_report.html')
        config.option.htmlpath = report
        config.option.self_contained_html = True