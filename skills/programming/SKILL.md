---
name: programming
description: Write, change, or fix code test-first in vertical slices, following one set of programming and testing principles (deep modules tested through their interface, functional core and imperative shell, explicit dependencies, modular monolith, mocks only at system boundaries). Use whenever you are about to write or modify production code or its tests, add a feature, or fix a bug, in any language. It also says when a change needs no tests, such as throwaway scripts and operational glue with no business logic.
---

# Programming

Settle the behaviour and its seam, then build it one failing test at a time into well-shaped code.

## Overview

This skill holds the programming and testing principles for any code change, in the order an agent uses them: decide whether the change needs tests, settle the behaviour and the seams, build it in vertical slices, then refactor and finish honestly. Programming and testing live in one skill on purpose, so an agent that loads it to write code gets the testing rules with it.

The order matters more than ceremony. A test written from the intended behaviour before the code exists catches bugs, while a test written after reading the code confirms whatever the code does, bugs included. Writing every test up front is the opposite failure: tests for imagined behaviour check the shape of things and go blind to real changes. The loop therefore runs in vertical slices, one test and then the code for it, each slice responding to what the last one taught.

A successful run leaves behaviour-level tests that failed before the change and pass after it, code that follows the programming principles, and a short note to the user covering any test that was itself wrong or any principle the agent departed from. For a change that needs no tests, it leaves well-shaped code and one line saying why no tests were added.

## When to use this skill

Use it whenever you are about to write, change, or fix code: a new feature or module, a bug fix, a refactor, or new or changed tests. It applies in any language and alongside any other skill that ends in a code change.

### When NOT to use this skill

Skip it for changes that contain no code, such as prose, documentation, or pure configuration values. For reviewing someone else's change without editing it, use a review skill.

## Constraints

- These principles are defaults. A project's established conventions and its own CLAUDE.md win where they conflict. Apply each principle only where the language supports it, express it in the idioms of the project's test framework, and when one would make the code or a test worse, depart from it and say why.
- Read the project's glossary (`GLOSSARY.md` or `CONTEXT.md`) and the ADRs (Architecture Decision Records) for the area you touch, if they exist, so names and interface vocabulary match the domain and no recorded decision is undone.
- Fix a failing test by fixing the code. Change an expectation only when the intended behaviour changes, and tell the user when the test itself was wrong. Loosening an assertion, skipping a test, or pasting the current output into the expected value hides a bug rather than fixing it.
- Test what you add or change. Add tests for code you didn't touch only when the user asks.

## Workflow

### Step 1: Decide whether the change needs tests

Code that makes decisions needs tests: business logic, domain rules, calculations, parsing, validation, data transformations, and anything another module or caller relies on. Code that only sequences other tools usually doesn't: throwaway scripts and spikes, one-off data fixes, operational glue with no business logic (service init, provisioning, build and CI configuration, dotfiles), and generated code. For those, skip to Step 4 and apply the programming principles in proportion to the code's size and lifespan.

Say in one line which path you chose. When a script on the short path grows real logic or becomes permanent, move it onto the full path.

### Step 2: Settle the behaviour and the seams

A seam is the public interface where a module's behaviour can be observed without reaching inside. Tests live at seams and never against internals. Write down the seams under test, each with one line on what a test there catches and what it misses, and the behaviours to cover, before the first test.

Ask the user only in two cases: the intended behaviour is unclear, or the change is backward incompatible (it breaks an existing caller of a public interface, a stored format, or a wire contract). Do not guess either into the tests. Otherwise state the seams in your note and proceed. When the shape of the interface is itself in question, such as how deep the module is or where the seam belongs, design the module first using the module guidance in Step 4.

For a bug, the first behaviour is the bug itself: a test that reproduces it at the seam where a caller sees it.

This step is done when each behaviour you will build has a named seam, and any question the two cases above raised is answered.

### Step 3: Build in vertical slices

Repeat the following for one behaviour at a time, and never write the tests for later behaviours ahead of their slice.

1. Red. Write one test for the next behaviour at its seam. Run it and see it fail for the expected reason before trusting it.
2. Green. Write only enough code to pass that test. Add no code for a future test or a speculative feature.
3. Move to the next behaviour, letting what this slice taught you reshape the next test.

A test verifies behaviour through the public interface, so it survives any internal refactor and fails only when behaviour changes. Write one test per behaviour rather than one per function, and make it read like a specification ("user can check out with a valid cart").

Choose what a test crosses by the behaviour, not by a quota. Most tests call a module through its interface with its real in-process collaborators and the real infrastructure it owns, such as its own database schema on the same engine as production. A few end-to-end (E2E) tests drive the running application through its real entry point (HTTP, UI, CLI) to cover the critical user journeys and the configuration and wiring that no module-level test can see. When you deepen a module, replace the old tests on its shallow parts with tests at the new interface instead of layering new tests on top.

Use the real thing wherever you can. Mock only at system boundaries, meaning what you don't control or what outside systems observe: third-party and external APIs, email and message buses, the clock, randomness, and sometimes the file system. Do not mock your own modules, internal collaborators, or anything you control. Prefer a real test database or a local stand-in over a mock of one. Classify a double by what it does, since frameworks use the names loosely:

- Fake: a working, simplified implementation, such as an in-memory message bus or payment gateway.
- Stub: returns canned answers and checks nothing.
- Spy: a stub that also records how it was called, for the test to inspect.
- Mock: set up with expected calls, and fails the test when they don't happen.

Prefer them in that order. If many tests rely on one fake, run a shared contract test against both the fake and the real adapter so they can't drift apart.

Decide what to assert by message type:

- Incoming query: assert on the value it returns.
- Incoming command: assert on its direct public side effect, such as the new state read back through the public interface or the event it published.
- Calls to itself (private helpers): leave them to the incoming tests.
- Outgoing query: stub it if the test needs the data, and leave it unasserted.
- Outgoing command: when its effect lands outside the system (email, a message bus, a third-party API), assert that it was sent with the right arguments. When the effect is local, assert the effect instead. Do not assert call counts or call order on internal collaborators.

Avoid these tests:

- Implementation-coupled: mocks internal collaborators, tests private methods, or verifies through a side channel such as querying the database instead of using the interface. The tell is a test that breaks on a refactor with no change in behaviour.
- Tautological: the expected value is recomputed the way the code computes it, so the test passes by construction. Take expected values from an independent source: a known-good literal, a worked example, or the spec.

Make each test independent and obvious when it fails. A test gives the same result alone or in any order, and its name and assertion point straight at the cause. Write tests as straight-line Arrange, Act, Assert code without loops or conditionals; a table-driven or parameterised test over a list of cases is fine. Repeat a little setup rather than hide it in shared helpers (DAMP, "descriptive and meaningful phrases", over DRY). For asynchronous flows, poll for the expected outcome with a timeout instead of sleeping.

Test what you would hate to see break, then stop. Cover each behaviour with inputs from every class the requirement names and at its extremes (the longest name, the largest amount, the state with the most text), not the convenient sample. Skip tests for plain accessors, wiring, and library or framework behaviour. If the project has architecture tests (ArchUnit, Spring Modulith's `verify()`, Packwerk), keep them passing, and propose new ones rather than adding them unasked. Coverage percentage points at untested code; it is not a target.

This step is done when every behaviour from Step 2 has a passing test that failed first for the expected reason.

### Step 4: Refactor to the design principles

Refactoring is not part of the red-green loop. Once the slices pass, restructure the code with the tests as the safety net, in whole, well-structured passes. Follow these principles:

1. Simplicity first (YAGNI, "you aren't gonna need it"). Write the code that is easiest to read and reason about. Add an abstraction when a second real use case needs it, not in anticipation of one.

2. Deep modules, packaged by feature, toward a modular monolith. A module is anything with an interface and an implementation, from a function to a package. Make it deep: a lot of behaviour behind a small interface, where the interface is everything a caller must know (signature, invariants, ordering, error modes). Organise code around domain concepts (`Order`, `Invoice`) rather than technical layers (`router`, `service`, `model`). Each module keeps its internals and data private, and other modules reach it only through its interface. Apply the deletion test: if deleting a module would make its complexity vanish, it was a pass-through, and if the complexity would reappear across its callers, it earns its keep. Prefer the words module, interface, seam and adapter over component, service, API and boundary.

3. Composition over inheritance. Build behaviour from small functions, closures, and interfaces, using structural or duck typing where the language has it. Closures and modules encapsulate state; keep class hierarchies shallow.

4. Explicit dependencies. Pass collaborators in as arguments or closures, so a function's signature shows everything it depends on and a test can substitute any of them at a system boundary. That includes the clock, random source, and ID generator, so a result never depends on when or where it runs.

5. SOLID, applied with functions and modules rather than classes:
    - Single responsibility: each function or module has one reason to change.
    - Open/closed: extend behaviour by passing in a function or adding a new variant, leaving working code unedited.
    - Liskov substitution: every implementation of an interface honours its whole contract, including errors and edge cases.
    - Interface segregation: keep interfaces small and define them in the module that consumes them, not the one that implements them.
    - Dependency inversion: core logic depends on interfaces it defines, and the I/O adapters at the edge implement them. Add such a port only when two adapters are justified, typically production and test. One adapter is a hypothetical seam and just adds indirection.

6. Functional core, imperative shell. Keep business logic as pure functions over data, and do I/O and mutation in a thin outer layer that calls them. Return results instead of producing side effects, which keeps interfaces easy to test. Accept a few pragmatic side effects in the core when purity would need monad-style plumbing. If a test of new code needs many mocks, the code mixes decisions with I/O: split it into a pure core and a thin shell (the Humble Object pattern) instead of mocking around it. In existing code, point out the problem rather than refactoring unasked.

7. Immutable by default. Return new values instead of mutating existing ones; immutable data makes concurrent code far easier to reason about.

8. Make illegal states unrepresentable. Model states with the type system (enums, sum types, exhaustive pattern matching) so invalid combinations fail at compile time instead of relying on runtime checks alone. Represent "no value" explicitly (`Option`, `Maybe`, or strictly checked nullable types) and check it at the earliest point. Stop before this needs advanced type-level machinery.

9. Specific errors, wrapped with context, handled at boundaries. Define an error type for each failure a caller can act on. Wrap errors with context as they propagate ("loading invoice 42: connection refused"). Handle them (log, retry, translate into a response) only at system boundaries such as HTTP handlers, CLI entry points, and job runners; business logic lets them propagate.

### Step 5: Make the tests pass honestly and finish

Run the whole affected suite, not only the new tests. When a test fails, work out whether the code or the test is wrong, and fix the code unless the test itself is wrong; when it is, fix it and tell the user what was wrong. Repeat until the suite passes.

Finish with a short note to the user: the seams you chose, which tests you added, any test you had to correct, and any principle you departed from and why.
