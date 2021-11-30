"""
# behave example
@given('we have behave instruction')
def step_impl(context):
    pass

@when('we implement a test')
def step_impl(context):
    assert True is not False

@then('behave will test it for us')
def step_impl(context):
    assert context.failed is False
    # assert False is not True
"""