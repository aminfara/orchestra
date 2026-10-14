# orchestra

Multi-agent development environment: a Claude Code plugin in which a conductor runs software engineering flows with a small team of agent roles. The plan is in [docs/plans/orchestra/README.md](docs/plans/orchestra/README.md).

## Install for development

The repo is its own local marketplace, `orchestra-local`, whose one plugin, `orchestra`, loads in place from the checkout:

```bash
claude plugin marketplace add /path/to/orchestra
claude plugin install orchestra@orchestra-local
```

Start the delivery loop with `orchestra:conductor`.

## Dependencies

### Skills

- skill-creator

### MCP
