# Auto-Generating Excel Import Templates for Django Apps: A How-To

In every real-world Django project, there comes a point when you need to populate your database with meaningful data. Whether you're onboarding clients, prepping for production, or setting up a demo environment — you need a fast, reliable, and user-friendly way to structure and validate that data.

That’s where this project began.

I wanted a tool that could **auto-generate an Excel workbook** tailored to my Django models — something that anyone could fill out with confidence. It needed to:

* Handle ForeignKeys using human-readable identifiers (not raw IDs)
* Support compound natural keys
* Use readable labels for `Choices` fields
* Enforce dropdowns and validations natively in Excel

I looked to [`django-import-export`](https://github.com/django-import-export/django-import-export), a fantastic library used by thousands. But while it’s great for moving data in and out of Django, it doesn’t generate human-friendly, validated Excel templates. So I built one that does.

---

## 🧠 What Problem Does This Solve?

Manually creating import templates is:

* Tedious to maintain
* Prone to human error
* Fragile when your models change

And while many libraries (like `django-import-export`) handle **import/export logic**, they often leave the **template design** up to the developer.

I needed something that was:

* **Self-documenting**
* **Schema-aware**
* **Client-friendly**

---

## 🛠️ What This Tool Does

With a single management command, it generates an Excel workbook that:

✅ Creates a worksheet per model
✅ Lists all fields with readable, wrapped headers
✅ Explodes ForeignKeys into natural key columns (including compound keys)
✅ Adds dropdown validations for ForeignKeys and `Choices` fields
✅ Includes a `Choices` worksheet that maps keys to human-readable labels
✅ Uses dynamic named ranges so validations grow as rows are added
✅ Supports hierarchical MP\_Node models via a validated `parent` field

The result is a template that’s **ready to use and easy to understand**, even for non-technical users.

---

## 🚀 Use Cases

* Populate dev or staging databases with valid seed data
* Provide structured templates to clients for data onboarding
* Reduce import errors by enforcing constraints up front
* Document expected fields and relationships clearly for your team
* Handle complex model relationships like `Organisation + Account + Project` with zero config

---

## ⚙️ How It Works (Under the Hood)

The tool uses Django’s `apps.get_app_config` to introspect your app’s models.

For each model:

* It creates a worksheet and adds each field as a column
* ForeignKey fields are **exploded** into natural key columns (single or compound)
* `Choices` fields (like `TextChoices`, `IntegerChoices`) are listed in a separate `Choices` sheet
* Excel validations are applied via `openpyxl.DataValidation` using named ranges
* Validations auto-expand as users add rows — no formulas or macros required

The resulting Excel file is robust, friendly, and highly maintainable.

---

## 📂 Running the Export Command

To create a new import template for your Django app:

```bash
python manage.py create_import_template <app_name>
```

This will generate the file in the following directory structure (relative to your Django project root):

```
<project_root>/
└── <app_name>/
    └── import_export/
        └── templates/
            └── <app_name>_import_file.xlsx
```

The file will include a worksheet per model, exploded keys, dropdown validations, and a `Choices` sheet.

---

## 💾 Running the Import Command

Once the workbook is filled out, save it to the following directory:

```
<app_name>/import_export/import_files/<app_name>_import_file.xlsx
```

Then import it back into the database using:

```bash
python manage.py import_workbook <app_name>
```

This will:

* Resolve `label → key` mappings for choices
* Match ForeignKeys using natural key lookups
* Handle compound key resolution where necessary
* Create or update model instances as needed

  * MP\_Node-based models are automatically structured by referencing the `parent` column, using Treebeard’s `add_root` or `add_child` methods under the hood to preserve hierarchical relationships.

This turns your Excel workbook into a fully functional import pipeline.

---

## 📦 Installation

To use this tool in your project, you'll need:

* Python 3
* Django
* `openpyxl`

Install dependencies with pip:

```bash
pip install django openpyxl
```

Then clone the project from GitHub:

```bash
git clone https://github.com/LlewopNomis/django-import-export-tools.git
```

The project is already structured as a full Django-compatible app, complete with a working demo app called `core`. This includes several models with a mix of ForeignKeys, ChoiceFields, and MP\_Node hierarchies so you can test the import/export process out of the box. Once cloned, you're ready to go — no extra setup required.

---

## 📘 Usage Guide

Once you've installed and cloned the project, follow these three steps to put the tool to use:

### 1. Generate an Import Template

```bash
python manage.py create_import_template <app_name>
```

This creates an Excel file at:

```
<project_root>/<app_name>/import_export/templates/<app_name>_import_file.xlsx
```

### 2. Fill Out the Template

Populate the file using readable values for ForeignKeys, choice labels, and structured hierarchies (MP\_Node models include a `parent` field).

### 3. Import Your Data

Save the file to:

```
<app_name>/import_export/import_files/<app_name>_import_file.xlsx
```

Then run:

```bash
python manage.py import_workbook <app_name>
```

Your data will be automatically validated, mapped, and imported into the database.

---

## 💬 Why This Matters

This project isn’t just about generating Excel files.

It’s about:

* **Saving developer time**
* **Reducing onboarding friction**
* **Improving collaboration with clients and testers**
* **Avoiding silent data errors**

If you’ve ever juggled stale templates, broken validations, or client-uploaded files with the wrong columns — this can help.

---

## 🔮 Coming Soon?

Would you use this in your project?

Would you like to see this packaged as an installable Django app that can be added via `pip install django-import-export-tools`?

Let me know in the comments — or connect with me:

* 🕊️ [Twitter/X](https://twitter.com/LlewopNomis)
* 💻 [GitHub](https://github.com/LlewopNomis)
* ✍️ [Medium](https://medium.com/@LlewopNomis)
