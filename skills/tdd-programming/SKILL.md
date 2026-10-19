---
name: tdd-programming
description: Write, change, or fix code test-first, following one set of programming and testing principles (functional core and imperative shell, explicit dependencies, modular monolith, behaviour-first tests at unit, integration and E2E level). Use whenever you are about to write or modify production code or its tests, add a feature, or fix a bug, in any language. It also says when a change needs no tests, such as throwaway scripts and operational glue with no business logic.
---

# Tdd Programming

Decide the behaviour, capture it as tests, then write well-shaped code that passes them.

## Overview

This skill holds the programming and testing principles for any code change, in the order an agent uses them: decide whether the change needs tests, settle and test the behaviour, implement it, then finish honestly. Programming and testing live in one skill on purpose, so an agent that loads it to write code gets the testing rules with it.

Agents write good code fast, so classic human test-driven development (TDD), with its one-test, minimal-code micro-cycles, mostly costs tokens without improving the result. What still matters is the order. Tests written from the intended behaviour, before the implementation exists, catch bugs. Tests written after reading the code tend to confirm whatever the code does, bugs included.

A successful run leaves behaviour-level tests that failed before the change and pass after it, code that follows the programming principles, and a short note to the user covering any test that was itself wrong or any principle the agent departed from. For a change that needs no tests, it leaves well-shaped code and one line saying why no tests were added.

## When to use this skill

Use it whenever you are about to write, change, or fix code: a new feature or module, a bug fix, a refactor, or new or changed tests. It applies in any language and alongside any other skill that ends in a code change.

### When NOT to use this skill

Skip it for changes that contain no code, such as prose, documentation, or pure configuration values. For reviewing someone else's change without editing it, use a review skill.

## Constraints

- These principles are defaults. A project's established conventions and its own CLAUDE.md win where they conflict. Apply each principle only where the language supports it, express it in the idioms of the project's test framework (its fixtures, assertion style and doubles), and when one would make the code or a test worse, depart from it and say why.
- Fix a failing test by fixing the code. Change an expectation only when the intended behaviour changes, and tell the user when the test itself was wrong. Loosening an assertion, skipping a test, or pasting the current output into the expected value hides a bug rather than fixing it.
- Test what you add or change. Add tests for code you didn't touch only when the user asks.

## Workflow

### Step 1: Decide whether the change needs tests

Code that makes decisions needs tests: business logic, domain rules, calculations, parsing, validation, data transformations, and anything another module or caller relies on. Code that only sequences other tools usually doesn't: throwaway scripts and spikes, one-off data fixes, operational glue with no business logic (service init, provisioning, build and CI configuration, dotfiles), and generated code. For those, skip to Step 3 and apply the programming principles in proportion to the code's size and lifespan.

Say in one line which path you chose. When a script on the short path grows real logic or becomes permanent, move it onto the full path.

### Step 2: Decide the behaviour and write the tests

Settle what the module or use case should do, then capture it as tests before you write the implementation. Keep the test-writing view free of the implementation, using a fresh context or subagent when the change is big enough to warrant it. When the intended behaviour is unclear, ask the user rather than guessing it into the tests. For a bug, start from a test that reproduces it. Run the new tests and see each one fail for the expected reason before trusting it.

Test behaviour through the public API. A test calls what a real caller calls and asserts what a real caller could observe, so it survives refactoring and fails only when behaviour changes. Write one test per behaviour rather than one per function.

Pick the level by what the test crosses, whatever the project calls it:

- Unit test: one unit of behaviour, often several functions together, in one process with no network, disk, or database, running in milliseconds. Functional-core tests pass in data and check the result, with no doubles. "Isolated" means isolated from other tests, so the code under test uses its real in-process collaborators.
- Integration test: one use case of one module, called through the module's public API, with the real infrastructure the module owns (its own database schema, on the same engine as production). The imperative shell is tested here; write a few per use case rather than one per branch.
- End-to-end (E2E) test: the whole running application through its real entry point (HTTP, UI, CLI), across modules. Keep a few, covering the critical user journeys and the configuration and wiring that no lower-level test can see.

Put each check at the lowest level that can catch the bug. When a higher-level test exposes a bug, also add a test at the lowest level that could have caught it. A suite built this way lands near 80% unit, 15% integration, and 5% E2E; use that rule of thumb to sanity-check the suite's shape, not as a quota.

Decide what to assert by message type. Classify each call the code under test receives or sends, whether that code is a function or a whole module:

- Incoming query: assert on the value it returns.
- Incoming command: assert on its direct public side effect, such as the new state read back through the public API or the event it published.
- Calls to itself (private helpers): leave them to the incoming tests, which already cover them.
- Outgoing query: stub it if the test needs the data, and leave it unasserted; the receiver's own tests cover it.
- Outgoing command: when its effect lands outside the module (email, a message bus, another module), assert that it was sent with the right arguments. When the effect is cheap and local, assert the effect instead.

Use the real thing where you can, and the simplest double where you can't. Frameworks use these names loosely (Jest calls everything a mock, Mockito's `spy` wraps a real object, and Sinon's `fake` is a spy rather than a working implementation), so classify a double by what it does:

- Real collaborator: the production implementation.
- Fake: a working, simplified implementation, such as an in-memory message bus or payment gateway.
- Stub: returns canned answers and checks nothing.
- Spy: a stub that also records how it was called, for the test to inspect afterwards.
- Mock: set up with expected calls, and fails the test when they don't happen.

Prefer them in that order. Use the real implementation for in-process code and for infrastructure the module owns, including its database. Replace only what the module doesn't control or what outside systems observe: email, message buses, third-party APIs, other modules, and the clock. If many tests rely on one fake, run a shared contract test against both the fake and the real adapter so they can't drift apart.

Test each module on its own. A module's unit and integration tests set up data through its own public API, touch only its own tables, and run without other modules loaded; only E2E tests cross modules. Other modules appear as doubles of their public API, and you check event-based collaboration by asserting on the published events. If the project has architecture tests (ArchUnit, Spring Modulith's `verify()`, Packwerk), keep them passing, and propose new ones rather than adding them unasked.

Make each test independent and obvious when it fails. A test gives the same result alone or in any order, and its name and assertion point straight at the cause. Write tests as straight-line Arrange, Act, Assert code without loops or conditionals; a table-driven or parameterised test over a list of cases is fine. Repeat a little setup rather than hide it in shared helpers (DAMP, "descriptive and meaningful phrases", over DRY). For asynchronous flows, poll for the expected outcome with a timeout instead of sleeping.

Test what you would hate to see break, then stop. Cover the behaviour you are adding or changing with inputs from every class the requirement names and at its extremes (the longest name, the largest amount, the state with the most text), not the convenient sample. Skip tests for plain accessors, wiring, and library or framework behaviour. Coverage percentage points at untested code; it is not a target.

This step is done when every behaviour you settled has a test and each new test has failed for the expected reason.

### Step 3: Implement the code

Design and implement in whole, well-structured passes rather than one-test micro-cycles, refactoring freely with the tests as the safety net. Follow these principles:

1. Simplicity first (YAGNI, "you aren't gonna need it"). Write the code that is easiest to read and reason about. Add an abstraction when a second real use case needs it, not in anticipation of one.

2. Package by feature, toward a modular monolith. Organise code around domain concepts (`Order`, `Invoice`) rather than technical layers (`router`, `service`, `model`), so everything about invoices lives together. Each module exposes a small public API and keeps its internals and data private; other modules reach it only through that API. Keep internals package-private so the compiler enforces the boundary.

3. Composition over inheritance. Build behaviour from small functions, closures, and interfaces, using structural or duck typing where the language has it. Closures and modules encapsulate state; keep class hierarchies shallow.

4. Explicit dependencies. Pass collaborators in as arguments or closures, so a function's signature shows everything it depends on and a test can substitute any of them. That includes the clock, random source, and ID generator, so a result never depends on when or where it runs.

5. SOLID, applied with functions and modules rather than classes:
    - Single responsibility: each function or module has one reason to change.
    - Open/closed: extend behaviour by passing in a function or adding a new variant, leaving working code unedited.
    - Liskov substitution: every implementation of an interface honours its whole contract, including errors and edge cases.
    - Interface segregation: keep interfaces small (one or two operations) and define them in the module that consumes them, not the one that implements them.
    - Dependency inversion: core logic depends on interfaces it defines, and the I/O adapters at the edge implement them.

6. Functional core, imperative shell. Keep business logic as pure functions over data, and do I/O and mutation in a thin outer layer that calls them. Accept a few pragmatic side effects in the core when purity would need monad-style plumbing. If a test of new code needs many mocks, the code mixes decisions with I/O: split it into a pure core and a thin shell (the Humble Object pattern) instead of mocking around it. In existing code, point out the problem rather than refactoring unasked.

7. Immutable by default. Return new values instead of mutating existing ones; immutable data makes concurrent code far easier to reason about.

8. Make illegal states unrepresentable. Model states with the type system (enums, sum types, exhaustive pattern matching) so invalid combinations fail at compile time instead of relying on runtime checks alone. Represent "no value" explicitly (`Option`, `Maybe`, or strictly checked nullable types) and check it at the earliest point. Stop before this needs advanced type-level machinery.

9. Specific errors, wrapped with context, handled at boundaries. Define an error type for each failure a caller can act on. Wrap errors with context as they propagate ("loading invoice 42: connection refused"). Handle them (log, retry, translate into a response) only at system boundaries such as HTTP handlers, CLI entry points, and job runners; business logic lets them propagate.

### Step 4: Make the tests pass honestly and finish

Run the whole affected suite, not only the new tests. When a test fails, work out whether the code or the test is wrong, and fix the code unless the test itself is wrong; when it is, fix it and tell the user what was wrong. Repeat until the suite passes.

Finish with a short note to the user: which tests you added, any test you had to correct, and any principle you departed from and why.
