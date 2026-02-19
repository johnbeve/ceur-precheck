# CEUR Preflight Checker

This repository allows you to check whether your paper satisfies CEUR technical formatting requirements before submission.

The system runs the official CEUR validation scripts and reports any formatting errors.

Your uploaded PDF is automatically deleted after checking.

---

# How To Use

## Step 1 — Upload Your Paper

1. Click **Add file → Upload files**
2. Upload your `.pdf` file
3. Enter a short commit title (e.g., "John's CEUR paper")
4. Click **Commit changes direclty to main**

---

## Step 2 — Run the Check

1. Click the **Actions** tab at the top of the repository.
2. Click the job with the commit title you provided (usually named at the top).
4. Wait for the workflow to complete (this usually takes 1–2 minutes).

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
2. Return to **Step 1**.
3. Run the check again.

Repeat until all sections report:

> ok

