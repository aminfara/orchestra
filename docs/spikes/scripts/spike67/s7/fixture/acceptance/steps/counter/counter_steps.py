from behave import when, then
from http_helper import call

@when("I post to the counter")
def step_post(context):
    context.resp = call(context.base_url + "/count", "POST")[1]

@then("the count is {n:d}")
def step_count(context, n):
    assert context.resp["count"] == n, f"got {context.resp['count']}"

@then("the total field is {n:d}")
def step_total(context, n):
    assert context.resp["total"] == n  # KeyError: the response has no "total"
