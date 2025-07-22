# Django Import Export Tools

This utility provides a management command to automatically generate an Excel workbook that acts as an import template for any Django app’s models. The template:

✅ Includes worksheets for each model with their fields as columns
✅ Automatically explodes ForeignKeys into natural key fields (unique constraints or primary key)
✅ Defines tables for each worksheet (ListObjects)
✅ Adds Excel Data Validations for:
- ForeignKey fields (cross-referencing natural key columns in other sheets)
- TextChoices and IntegerChoices fields (readable dropdowns using a `Choices` worksheet)
✅ Generates a `Choices` worksheet showing both keys and human-readable labels
✅ Ensures all validations are dynamic and adjust with the table as data is added

---

## 🔧 Installation

Clone this repository into your Django project and place `export_model_spec.py` in your app’s `management/commands` directory.

```
<yourapp>/management/commands/export_model_spec.py
```

Ensure you have `openpyxl` installed:

```
pip install openpyxl
```

---

## 🚀 Usage

Run the command for your app:

```
python manage.py export_model_spec <app_label>
```

The output will be saved to:

```
<app_label>/media/import_export/templates/<app_label>_import_file.xlsx
```

---

## 📝 Example features

- **Human-readable headers:** Clear, wrapped text headers for each column.
- **Choices dropdowns:** Friendly dropdowns for fields using Django `TextChoices` or `IntegerChoices`, displaying the `label` and resolving to the `key` on import.
- **ForeignKey validation:** Dropdown validation pointing to the first natural key of the related model (typically a human-readable field).
- **Dynamic named ranges:** All validations reference named ranges that resize as tables grow.
- **Choices worksheet:** Self-documenting reference for all choices used in dropdowns.

---

## 🔔 Use cases

- Populate development or staging databases quickly.
- Prepare client import templates with proper validations.
- Reduce human error during initial data load.
- Provide self-documenting import specifications for clients or teams.

---

## 💡 Notes

- Only managed and non-abstract models are included.
- Foreign keys targeting models with a unique constraint are resolved by exploding into separate columns.
- `Choices` worksheet keeps both key and label so your import routine can resolve `label → key` at import time.
- A corresponding import routine is coming shortly to handle:
  - Reverse lookup of `label` values to `key` values for choice fields.
  - Foreign key lookups to resolve natural keys or human-readable identifiers to internal database keys.
  - Compound foreign key lookups where multiple fields together define a relationship.

---

## 📖 Further reading

For background on why this tool was built and how it works:
[Read more about this project on Medium](https://medium.com/your-story-url)

---

## 🖋️ License

MIT License.

---

## ❤️ Contributions

PRs welcome — especially improvements to:
- Second-level validations (e.g., max length, numeric constraints)
- Inline documentation/comments
- Import routines that consume this file structure

---

Feel free to fork, improve, and share feedback! 🎯

