![Frame 33 (1)](https://github.com/user-attachments/assets/0340ea31-3fc5-4138-92f5-58924ad3b589)

# Album - Productivity Widget
![Release](https://img.shields.io/github/v/release/CamdenMontgomery/Album-Desktop-Widget?sort=semver)
![License](https://img.shields.io/github/license/CamdenMontgomery/Album-Desktop-Widget)
![Last Commit](https://img.shields.io/github/last-commit/CamdenMontgomery/Album-Desktop-Widget)
![Top Language](https://img.shields.io/github/languages/top/CamdenMontgomery/Album-Desktop-Widget)
![Open Issues](https://img.shields.io/github/issues/CamdenMontgomery/Album-Desktop-Widget)
![Open PRs](https://img.shields.io/github/issues-pr/CamdenMontgomery/Album-Desktop-Widget)

> A Camera, Sticky Notes, and Flash Cards all in your computer's back pocket.

---

## Overview

**Album** is a lightweight desktop companion built to help users capture, organize, and revisit the ideas that appear throughout their digital workspace. It’s a simple tool with a simple purpose: to make it effortless to save what matters in the moment — a screenshot, a note, or a flashcard — and keep it all neatly organized for later review.

Rather than functioning as another full-sized application competing for attention, Album lives quietly at the edge of the screen. It’s always ready, yet never in the way. With a smooth, minimal interface that reveals itself only when needed, Album provides three core tools:

* a **snapshot utility** for quickly capturing regions of the screen,
* a **sticky note pad** for jotting down thoughts before they fade, and
* a **flashcard creator** for turning captured information into something you can study and remember.

These tools work together to bridge the gap between casual discovery and structured learning. Whether it’s a line of code, a slide in a lecture, or a fleeting idea during research, Album helps turn those moments into organized content — automatically sorted by topic and stored where you decide.

Each workspace acts as a container for related materials. Within a workspace, users can create separate folders for individual topics, each holding its own notes, snapshots, and flashcards. Switching between projects is as simple as selecting a different workspace, letting users move fluidly between subjects without clutter or confusion.

Album isn’t designed to overwhelm. It’s designed to blend into your workflow — a quiet, reliable utility that keeps everything you collect just a click away.


![Mockup Scene 4](https://github.com/user-attachments/assets/9d32a3de-2d35-47f2-92ef-2a9f9a16e2e5)

---

## Design Story

Album’s design is built around approachability. It avoids corporate tones and harsh contrasts, instead using light colors and soft shapes to create a calm, comfortable interface. Its goal isn’t to demand attention, but to quietly assist users in capturing what matters most while staying out of the way.

Every element of the interface was refined with small, deliberate choices — limited font weights, tighter letter spacing, and consistent sizing to create visual rhythm. Album isn’t meant to impress through complexity; it’s meant to feel natural and kind to look at.

---

## Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![Pynput](https://img.shields.io/badge/pynput-34b7f1?style=for-the-badge&logo=python&logoColor=white)
![PyInstaller](https://img.shields.io/badge/pyinstaller-2e2b7f?style=for-the-badge&logo=python&logoColor=white)
![Inno Setup](https://img.shields.io/badge/Inno%20Setup-9f1f2d?style=for-the-badge&logo=inno-setup&logoColor=white)


Album is written in **Python**, using **PySide6 (Qt for Python)** and the **QtWidgets** module for its UI. It follows an **MVC-inspired structure**, with a global store managing state changes across components. This approach keeps UI and logic cleanly separated while maintaining lightweight communication between parts of the application.

Persistent user preferences, such as workspace pins and hotkey bindings, are saved in `settings.ini`, ensuring a consistent experience across sessions.

---

## Building and Distribution

Album uses **PyInstaller** for bundling and **Inno Setup** for creating an installer.

### Building

To build from source:

```bash
pyinstaller main.spec
```

If you are replacing or adding new image assets, run a clean build:

```bash
pyinstaller --clean main.spec
```

### Creating the Installer

An Inno Setup script is provided in the `installer/` directory. Open the `.iss` file in Inno Setup, **build** it first, and then run it to create the installer. Remember to rebuild using PyInstaller before running Inno if any changes were made to the source code.

### Releases

Version 1 will include:

* A `.zip` file containing the executable and dependencies.
* A Windows installer built through Inno Setup.

### Supported Platforms
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

Currently developed and tested on **Windows 10 (x64)**. Other Windows versions may work, but only this configuration has been verified.

---

## Usage

When Album is opened, a small toolbar appears near the bottom of the screen. It can hide itself when the mouse moves away and reappear when the user hovers near the bottom edge.

From left to right, the toolbar includes:

1. **Workspace Button** – Opens a dialog to select or create a workspace folder. Workspaces organize notes, snapshots, and flashcards by topic.
2. **Folder Dropdown** – Displays the folders (topics) within the current workspace.
3. **Add Folder Button** – Creates a new topic/folder.
4. **Delete Folder Button** – Removes the selected folder after confirmation.
5. **Pin Slots (1–5)** – Quick access slots for pinned folders, specific to the current workspace.
6. **Tool Buttons** – The main tools: Snapshot, Note, and Flashcard.

   * **Snapshot** freezes the screen and lets the user select a region to save as an image.
   * **Note** opens a small sticky note window to jot down text.
   * **Flashcard** opens two text fields (front and back) that save to an exportable text file compatible with Quizlet’s import feature.
7. **Close Button** – Quits the application.

### Hotkeys

* `Alt + 1–5` → Switch between pinned folders.
* `Alt + Z` → Create a snapshot.
* `Alt + X` → Open a note.
* `Alt + C` → Open a flashcard dialog.

---

## Folder Structure

### Project Structure

```
Album/
├── src/
│   ├── main.py                # Entry point for the application
│   ├── view/                  # UI components and window definitions
│   │   ├── components/        # Reusable widgets (buttons, selectors, etc.)
│   │   └── windows/           # Main app windows and dialogs
│   ├── utils/                 # Utility modules (Store, UseStore, etc.)
│   ├── enums/                 # Enumerations for actions and state handling
│   ├── resources/             # Icons, images, fonts, stylesheets
│   └── settings.ini           # Persistent user settings and hotkey preferences
│
├── installer/                 # Inno Setup script and installer files
│   └── album_installer.iss
│
├── dist/                      # PyInstaller output (built .exe and dependencies)
├── build/                     # Temporary PyInstaller build files
│
├── README.md
├── main.spec                  # PyInstaller build configuration
├── .gitignore
└── requirements.txt
```

### User Workspace Structure

```
[UserSelectedWorkspace]/
├── [TopicName]/               # Each topic or subject created by the user
│   ├── snapshots/             # Screenshots taken with the snip tool
│   │   └── [time]_[date].jpeg
│   ├── notes/                 # Sticky notes saved as .txt files
│   │   └── [first10letters].txt
│   └── export.quizlet.txt     # Consolidated Quizlet import file for flashcards
│
└── workspace.ini              # Metadata for pinned folders and workspace info
```

---

## Future Improvements

Album v1 lays the foundation for a minimal and functional productivity companion, but there’s room to grow. Some ideas include:

* Toast notifications for confirming actions.
* Drop shadows and improved window polish.
* Editable notes and flashcards.
* User-customizable hotkeys.
* Smoother animations and transitions.
* Theme and accent color support.
* Verified builds for macOS and Linux.
* Improved installer automation for releases.

---

## Contributing

Album was built as a small, contained project — something useful, but also something to learn from. While development time is limited, there’s plenty of room for it to evolve beyond its current form. If you’d like to take it further, improve its code, or expand its design, you’re more than welcome to do so.

Pull requests, feature ideas, or even small fixes are all appreciated. A few more features may be added in time, but if you see potential in Album, don’t hesitate to make it better in my stead.
