# Website Upload Instructions

These instructions are for uploading the completed package to the existing GitHub branch without using a command line.

Do not upload until the package has been reviewed and explicitly marked final.

1. Download `DCP-challenge-author-correction-2026.zip`.
2. Unzip it on your computer.
3. Open the extracted folder `DCP-challenge-author-correction-2026`.
4. In the GitHub repository, switch the branch selector to `author-correction-2026`.
5. Click **Add file** and then **Upload files**.
6. In Ubuntu Files, press **Ctrl+H** so that `.gitignore` and the `.github/` folder are visible.
7. Drag the **contents inside** the extracted folder into the upload area. Do not drag the outer folder itself, or GitHub will create an unwanted extra directory level.
8. Wait until all files have appeared in the upload list.
9. Confirm that the original six root scripts are present and that `README.md`, `.gitignore`, `.github/workflows/tests.yml`, `correction/`, `src/`, `tests/`, `results/`, and `witness/` are present.
10. Use this commit message:

```text
Add author correction and corrected DCP analysis
```

11. Select **Commit directly to the author-correction-2026 branch**.
12. Click **Commit changes**.

After upload, compare the branch against `main` before merging. Do not delete the immutable `paper-2022-original` release or tag.

The hidden files are part of the audited package. If `.github/workflows/tests.yml` is omitted, GitHub will not run the automated test workflow; if `.gitignore` is omitted, generated local files may be added accidentally later.
