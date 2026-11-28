Feature: Greeting

  Scenario: Greets by name
    Given the service is running
    When I ask for a greeting for "alice"
    Then the greeting is "hello alice"

  Scenario: Greets formally (not built yet)
    Given the service is running
    When I ask for a greeting for "alice"
    Then the greeting is "good day alice"
