# Creating Your First Hugo Website with HugoStudio

This guide explains how to create your first local Hugo website using HugoStudio.

No Git knowledge is required.

---

# Requirements

Before you begin, install:

- **Hugo** (required)

Git is optional. It is only needed for advanced features such as installing themes from Git repositories or deploying your site using Git.

---

# Step 1 – Create a New Project

1. Start **HugoStudio**.
2. Select **File → New Project**.
3. Choose an empty folder.
4. Enter your website name.
5. Click **Create**.

HugoStudio creates a standard Hugo project.

At this point, your project contains the basic Hugo folder structure but **does not contain a theme**.

---

# Step 2 – Install a Theme

A Hugo website requires templates to display your content.

These templates are provided either by:

- a **theme**, or
- your own files in the **layouts** folder.

A newly created Hugo project contains neither, so there is nothing to display yet.

To install a theme in HugoStudio:

1. Select **Hugo → Install Theme**.
2. Install a theme from a ZIP file or a Git repository.
3. Open your configuration file (`hugo.toml`, `hugo.yaml`, or `hugo.json`).
4. Add the theme name.

For example:

```toml
theme = "papermod"
```

or

```yaml
theme: papermod
```

Save the configuration file.

---

# Step 3 – Explore the Project

The most important folders are:

- **content/** – your website pages and posts
- **static/** – files copied directly to the website
- **layouts/** – your own templates
- **themes/** – installed themes
- **public/** – generated website (created after building)
- **hugo.toml** (or `hugo.yaml`) – website configuration

For most beginners, only the **content** folder and the configuration file need to be edited.

---

# Step 4 – Create Your First Page

Right-click the **content** folder.

Select:

**New Page**

Enter a page name, for example:

```
about
```

HugoStudio creates:

```
content/about.md
```

Open the file and edit it.

Example:

```markdown
---
title: "About"
---

# About

Welcome to my first Hugo website.
```

Save the file.

---

# Step 5 – Preview the Website

Select:

**Hugo → Preview**

Hugo starts a local web server and opens your website in your browser.

Whenever you save a Markdown file, the browser automatically refreshes to show the changes.

---

# Step 6 – Create More Pages

Create additional pages in the same way.

For example:

```
contact.md
projects.md
news.md
```

Each Markdown file becomes a page on your website.

---

# Step 7 – Build the Website

When your website is ready:

Select:

**Hugo → Build**

Hugo generates the complete website in the **public** folder.

Everything inside the **public** folder can be uploaded to a web server or hosting service.

---

# Summary

Creating a Hugo website follows a simple workflow:

1. Create a new project.
2. Install a theme.
3. Configure the theme.
4. Create Markdown pages.
5. Preview your website.
6. Build the website for publishing.

Once you understand this workflow, you can begin exploring more advanced Hugo features such as menus, page bundles, taxonomies, custom layouts, and deployment.