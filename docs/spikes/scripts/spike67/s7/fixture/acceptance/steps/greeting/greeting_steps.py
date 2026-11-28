from urllib.parse import quote
from behave import given, when, then
from http_helper import call

@given("the service is running")
def step_running(context):
    assert call(context.base_url + "/hello")[0] == 200

@when('I ask for a greeting for "{name}"')
def step_ask(context, name):
    context.resp = call(context.base_url + "/hello?name=" + quote(name))[1]

@then('the greeting is "{text}"')
def step_greeting(context, text):
    assert context.resp["greeting"] == text, f"got {context.resp['greeting']!r}"
