# Run log

The run log, `log.md` in the run folder, is the conductor's memory across sessions. A fresh session that reads only this file should know which flow is running, where it stands, who is working on what, and what the user has decided. Keep entries short: the artifacts and reports hold the detail, and the log points at them.

## Shape

```markdown
# Run: <flow> — <product or request, in a few words>

- **Run ID:** <the run folder's name>
- **Flow:** <flow> — chosen because <one sentence>
- **Project root:** <path>
- **Started:** <yyyy-mm-dd>
- **Status:** in progress at phase <n> | complete | stopped (<reason>)

## Team

| Role | Agent ID | Model, effort | Since phase | Notes file |
| --- | --- | --- | --- | --- |
| product manager | <id> | opus, high | 2 | — |

## Phases

### Phase <n>: <name> — <not started | in progress | checking | at gate | approved | skipped>

- **Who:** <roles and instances>
- **Artifacts:** <paths>
- **Report:** <path> — <status>; <the report's summary, one or two sentences>
- **Check:** <checker> — <pass | revise>; <findings by severity>; ledger <ids>
- **Gate:** <yyyy-mm-dd> approved | changes requested (<n> comments, ledger <ids>)
- **Rulings:** <decisions roles made on their own, one line each>

## Decisions

- <yyyy-mm-dd> <decision the user made, and where it is recorded (brief section, ADR)>

## Open questions

- <question> — <who answers, by which phase>

## Deviations

- <phase>: <what changed from the flow file, and why>
```

## Notes

Update the log at each phase boundary and whenever the team changes, so it is never more than one phase behind. When an instance is replaced by a fresh one, add a row rather than editing the old one; the history shows how often contexts fill.

Record decisions with dates, and put the decision itself in the brief or an ADR. The log says that a decision was made and where to find it.
