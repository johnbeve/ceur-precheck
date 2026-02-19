# CEUR Preflight Checker

This repository allows you to check whether your paper satisfies CEUR technical formatting requirements before submission.

The system runs the official CEUR validation scripts and reports any formatting errors.

Your uploaded PDF is automatically deleted after checking.

---

# How To Use

## Step 0 - Log in to GitHub

1. If you have a GitHub account, log in
2. Otherwise, create a GitHub account [here](https://github.com/), then log in

## Step 1 — Open an Issue and Submit Your Paper

1. Click the **Issues** tab.
2. Click **New Issue**.
3. Select **CEUR Precheck Submission**.
4. Drag and drop your `.pdf` file into the upload box.
5. Click **Submit new issue**.

---

## Step 2 — Wait for the Check

After submitting the issue:

- The CEUR validation workflow will run automatically.
- This usually takes 1–2 minutes.

You can click the **Actions** tab to monitor progress, or simply refresh the Issue page.

---

## Step 3 — Interpret the Results

The following CEUR requirements are validated:

- Readable/selectable text (not scanned images)
- Correct CEUR copyright clause and year
- Declaration on Generative AI
- No premature CEUR branding
- Libertinus font usage
- No duplicate PDFs
- No leftover CEURART template elements
- One-column CEURART format

When complete, you will see output like:

> (*) Readable/Selectable text inside PDF files
> ok

> (*) CEUR-WS standard copyright phrase
> ERROR: PDF file paper.pdf seems to lack the proper copyright clause...
> ===> Make sure that paper PDFs have the correct copyright clause...

If every section ends with:

> ok

then your paper likely satisfies CEUR technical requirements.

- If you see any line beginning with:

> ERROR:

then your paper likely does **not** satisfy the requirements and must be revised.

The text immediately below the error explains what must be fixed.

---

## Step 4 — Revise and Repeat (Optional)

If there are errors:

1. Fix the issue(s) in your paper.
2. Return to **Step 1** and note that you will need to open a new Issue and upload the updated PDF; issues are automatically closed after runs.
3. Run the check again.

Repeat until all sections report:

> ok

