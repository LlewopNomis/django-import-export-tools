# Django Import Export Tools

---

A utility for Django developers who need **Excel-based import templates** that are:

- 🧑‍💼 **Human-friendly** — labels, dropdowns, natural keys
- 🎯 **Model-aware** — understands ForeignKeys, Choices, constraints
- 🪄 **Zero-config** — no need to define `Resource` classes or custom widgets

While developing this tool, I explored the excellent [`django-import-export`](https://github.com/django-import-export/django-import-export) library. It excels at serializing Django models to and from tabular formats like CSV and Excel. However, when I needed a fully validated **Excel workbook for human data entry**, I found that several critical features weren’t available out of the box, including:

- Auto-expansion of ForeignKey and compound key fields
- Dropdowns for `TextChoices` and `IntegerChoices` with friendly labels
- Named ranges and dynamic Excel validations
- A `Choices` sheet for self-documenting reference

Rather than compete, this project complements `django-import-export` by handling the *front-end data entry side*. I'd be thrilled if this project sparks further development in that direction — or even gets absorbed into more mainstream tools.

---

This utility provides a management command that automatically generates an Excel workbook for any Django app’s models. The logic is modular and can also be used in views or background tasks. The template includes:

✅ A worksheet per model with one column per field  
✅ ForeignKey fields auto-expanded into their natural key fields (e.g., unique constraints or human-readable PKs)  
✅ Tables (Excel ListObjects) defined for each worksheet  
✅ Data validation using:
- Excel dropdowns for ForeignKeys (referencing other sheets)
- Dropdowns for `TextChoices`/`IntegerChoices` with friendly labels

✅ A `Choices` worksheet showing keys and human-readable labels  
✅ Dynamic named ranges to grow with your data  
✅ MP_Node support via `parent` field with validated natural key references

---

## 🔧 Getting started

- [Installation](#) *(coming soon or link to Medium section)*
- [Usage Guide](#) *(coming soon or link to Medium section)*

---

## 📝 Features

- **Human-readable headers:** Clear, wrapped text headers
- **Choices dropdowns:** Friendly dropdowns using Django `Choices` fields (resolves `label → key` on import)
- **ForeignKey validation:** Dropdown to first natural key of related model (usually a readable code)
- **Dynamic named ranges:** Excel validations auto-expand as the user adds rows
- **Choices worksheet:** Self-documenting lookup for all choice-based fields
- **Compound foreign keys:** Automatically broken into constituent fields, no custom config needed
- **MP_Node support:** Adds a validated `parent` field so hierarchical trees are preserved

---

## 🔔 Use cases

- Populate dev or staging environments quickly
- Provide clients with validated import templates
- Reduce human error when onboarding data
- Allow non-technical teams to enter relational data in Excel
- Handle **complex model relationships** — compound keys, hierarchy trees, foreign keys
- Provide fully self-documenting Excel templates for teams and stakeholders

---

## 💡 Notes

- Only **managed**, **non-abstract** models are included
- ForeignKeys are resolved into separate columns using natural keys
- `Choices` worksheet ensures your import routine can reverse map `label → key`
- A corresponding import utility (in progress) will support:
  - Resolving choice field labels into values
  - ForeignKey lookups using natural keys
  - Compound foreign key resolution

---

## 📖 Further reading

For the full story and walkthrough, see:  
👉 [How I Built a Django Excel Import Template Generator (Medium)](https://medium.com/@LlewopNomis/how-i-built-a-django-excel-import-template-generator-and-how-you-can-too-68ff6b5e8af5)

---

## 🖋️ License

MIT License

---

## ❤️ Contributions

PRs welcome — especially for:

- Additional validations (e.g., length, numeric ranges)
- Documentation and inline comments
- Enhanced import routines to match the template format

---

Feel free to fork, improve, and share feedback! 🎯

---

## 📫 Contact

Reach out via [Medium](https://medium.com/@LlewopNomis) or [Twitter/X](https://twitter.com/@LlewopNomis)
