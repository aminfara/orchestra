---
name: programming
description: Before writing, changing, or fixing any code in any language, read this guide of design principles (deep modules, functional core and imperative shell, explicit dependencies, modular monolith). It applies under any workflow skill, including test-first ones, and does not define a test loop.
---

# Programming

Design principles for any code change. Read them before the first edit, then let whatever workflow is running (a test-first skill, `/implement`, a plain request) drive the steps.

## Constraints

- These principles are defaults. A project's established conventions and its own CLAUDE.md win where they conflict. Apply each principle only where the language supports it, and when one would make the code worse, depart from it and say why in your closing note.
- Read the project's glossary (`GLOSSARY.md` or `CONTEXT.md`) and the ADRs (Architecture Decision Records) for the area you touch, if they exist, so names match the domain and no recorded decision is undone.
- Change only what the task needs. Point out problems in existing code instead of refactoring them unasked.
- Scale the principles to the code's size and lifespan. A throwaway script or operational glue (provisioning, build configuration, dotfiles) needs readable code and little else.

## Principles

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

6. Functional core, imperative shell. Keep business logic as pure functions over data, and do I/O and mutation in a thin outer layer that calls them. Return results instead of producing side effects, which keeps interfaces easy to test. Accept a few pragmatic side effects in the core when purity would need monad-style plumbing. If a test of new code needs many mocks, the code mixes decisions with I/O: split it into a pure core and a thin shell (the Humble Object pattern) instead of mocking around it.

7. Immutable by default. Return new values instead of mutating existing ones; immutable data makes concurrent code far easier to reason about.

8. Make illegal states unrepresentable. Model states with the type system (enums, sum types, exhaustive pattern matching) so invalid combinations fail at compile time instead of relying on runtime checks alone. Represent "no value" explicitly (`Option`, `Maybe`, or strictly checked nullable types) and check it at the earliest point. Stop before this needs advanced type-level machinery.

9. Specific errors, wrapped with context, handled at boundaries. Define an error type for each failure a caller can act on. Wrap errors with context as they propagate ("loading invoice 42: connection refused"). Handle them (log, retry, translate into a response) only at system boundaries such as HTTP handlers, CLI entry points, and job runners; business logic lets them propagate.

## Seams for tests

A seam is the public interface where a module's behaviour can be observed without reaching inside. Tests that a workflow skill asks for go through seams, use real collaborators, and mock only at system boundaries: third-party APIs, email and message buses, the clock, randomness, and sometimes the file system. Your own modules are never mocked.
