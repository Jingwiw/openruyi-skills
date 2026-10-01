# Rust Quality Checklist

## Architecture

- Keep orchestration thin and behavior behind traits/plugins.
- Prefer clear ownership over shared mutable state.
- Isolate distro-specific rules from generic core.

## Error Handling

- Add context for external process calls, IO, and parse failures.
- Keep error messages actionable and include boundary location.

## Memory And Performance

- Use `Box<T>` for recursive or large value containment when ownership is single-owner.
- Use `Arc<T>` only for true shared ownership across async/tasks/threads.
- Prefer borrowing over cloning; justify unavoidable clones.
- Use arena/indexed IDs only when allocation volume or graph relationships justify it.

## Parser And AST

- Keep span strategy explicit and stable across transforms.
- Keep AST types composable and avoid semantic leakage between phases.
- Use Pratt parsing only where precedence and extensibility require it.

## Verification

- Run targeted checks first, then broader checks.
- Record what was validated and what remains unverified.
