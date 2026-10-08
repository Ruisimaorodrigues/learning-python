# Contributing to olist_dbt

## Development workflow

All changes go through pull requests. Direct pushes to `main` are not allowed.

### Steps

1. Create a feature branch from main
   `git checkout -b feature/your-feature-name`

2. Make your changes and test locally
   `dbt build`

3. Run sqlfluff to check SQL style
   `sqlfluff lint models/ --dialect duckdb --templater dbt`

4. Commit and push
   `git add .`
   `git commit -m "descriptive message"`
   `git push -u origin feature/your-feature-name`

5. Open a Pull Request on GitHub

6. GitHub Actions runs `dbt build` automatically on the PR

7. Merge only when CI passes

## Testing

Run all tests locally before pushing:
`dbt build`

## SQL style

This project uses sqlfluff for SQL linting. Fix violations with:
`sqlfluff fix models/ --dialect duckdb --templater dbt`