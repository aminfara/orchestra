# Flow: new feature

A new capability for a product that already exists. It is not a flow with phases of its own: it chains the flows that already exist, each as its own run, scoped to the feature, and tells you what to carry from one to the next. The point is to start from what the system is, so the feature extends it rather than reworking it.

## The chain

1. **Map, when needed.** If the architecture doc and glossary are missing or no longer match the code in the area the feature touches, run the understand flow scoped to that area first. Skip it when they are current; ask the user only if you cannot tell.
2. **Idea, rarely.** Run the idea flow only when the feature is big enough to need market research or a PR/FAQ, such as a new product line or a paid tier. Most features skip it.
3. **Requirements.** Run the requirements flow to extend the existing PRD with the feature's requirements. The product manager sizes them with estimation against the existing architecture doc, and designs the UX for the feature's journeys if it has a user interface.
4. **Architecture.** Run the architecture flow for the selected requirements. The architecture doc is updated in place and says what changes and why; the breakdown adds the feature's stories to the existing board.
5. **Build.** Run the build flow for the feature's milestones, on an integration branch of its own.

## Carrying context

Each run's log names the next run and the artifacts it hands over, and each brief points to the existing living docs rather than to anything new. Resume a role across runs when its assignment continues: the architect who mapped the area designs the change to it, if its instance is still current. Start fresh when the instance is spent or the work is independent, from the role's notes and the living docs.

At each flow's last gate, say which link comes next and why, and let the user stop the chain there.
