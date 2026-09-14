name: Generate Snake

on:
  schedule:
    - cron: "0 */12 * * *"
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  generate:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: Platane/snk@v3
        with:
          github_user_name: burgerSlayer766
          outputs: |
            dist/github-contribution-grid-snake.svg?color_dots=#ebedf0,#9be9a8,#40c463,#30a14e,#216e39
            dist/github-contribution-grid-snake-dark.svg?palette=github-dark

      - name: Patch empty cells with sleeping emoji
        run: |
          sudo chmod -R a+rwX dist
          python3 scripts/patch_snake.py dist/github-contribution-grid-snake.svg
          python3 scripts/patch_snake.py dist/github-contribution-grid-snake-dark.svg

      - uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
