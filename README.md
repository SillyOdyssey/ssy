# SSY Programming Language 🚀

Welcome to the official repository for **SSY**, a highly custom, lightweight programming tool built from scratch using **Pydroid 3** and **Python**. 

Designed specifically for mobile integrated development environments (IDEs) and terminal use, SSY offers a unique visual syntax, built-in calculator pipelines, custom table layouts, and isolated native command hooks.

---

## 📦 What's Inside the Release Package

The first official release is distributed as a clean **ZIP file** containing the complete core workspace:

* 📄 **`ssycore.py`** – The main compiler interpreter engine.
* 📝 **`main.ssy`** – A template script containing base functional expressions.
* 🌐 **`README.html`** – A responsive, localized user guide and licensing layout page.

---

## ⚙️ Environment Implementation & Support

### 1. IDE Export Mode
SSY is specifically licensed for use inside Python mobile IDE environments like **Pydroid 3**. You can load and execute the `ssycore.py` binary directly through the built-in console layout.

### 2. Host Terminal Execution
To run SSY via terminal command line arguments, ensure your working directory paths are correctly mapped to your local system or Android emulated media environment paths:
```bash
python ssycore.py main.ssy
```
*Note: Running in script compiler mode requires the target workspace to point directly to a valid `.ssy` container path (like `main.ssy`).*

---

## 🛠️ Feature Summary
Once you are inside the active interactive terminal or execution prompt, you can call the custom system parameters built right into the core language parser:
* **Interactive Engine Manual:** Type `::guide` to print a complete operational syntax reference sheet on screen.
* **Wipe Environment Memory:** Type `::restart` to cleanly flush active variable registries and wipe the console pixels.
* **Custom Sandboxed Modules:** Leverage the `PY:` token prefix to safely trigger isolated host utilities like `PY:clear`, `PY:break`, or `PY:input`.

---

## 📄 License and Distribution

Developed by **[SillyOdyssey](https://github.com/SillyOdyssey)**.

This project is open-source software licensed under the [MIT License](LICENSE.md).
