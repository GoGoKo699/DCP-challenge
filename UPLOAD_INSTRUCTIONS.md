# Website Upload Instructions

These instructions are for uploading the completed package to the existing GitHub branch without using a command line.

Do not upload until the package has been reviewed and explicitly marked final.

1. Download `DCP-challenge-author-correction-2026.zip`.
2. Unzip it on your computer.
3. Open the extracted folder `DCP-challenge-author-correction-2026`.
4. In the GitHub repository, switch the branch selector to `author-correction-2026`.
5. Click **Add file** and then **Upload files**.
6. Drag the **contents inside** the extracted folder into the upload area. Do not drag the outer folder itself, or GitHub will create an unwanted extra directory level.
7. Wait until all files have appeared in the upload list.
8. Confirm that the original six root scripts are present and that `README.md`, `correction/`, `src/`, `tests/`, `results/`, and `witness/` are visible.
9. Use this commit message:

```text
Add author correction and corrected DCP analysis
```

10. Select **Commit directly to the author-correction-2026 branch**.
11. Click **Commit changes**.

After upload, compare the branch against `main` before merging. Do not delete the immutable `paper-2022-original` release or tag.

Note: files inside `.github/` may be hidden by some desktop file browsers. They are useful for automated tests but are not required for the scientific content. A later verification step will check whether `.github/workflows/tests.yml` was uploaded.
