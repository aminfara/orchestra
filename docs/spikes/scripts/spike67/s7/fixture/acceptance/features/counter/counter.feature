Feature: Counter

  Scenario: Counter increments
    When I post to the counter
    Then the count is 1

  Scenario: Counter resets (step not written)
    When I reset the counter
    Then the count is 0

  Scenario: Counter reports total (step crashes)
    When I post to the counter
    Then the total field is 2
