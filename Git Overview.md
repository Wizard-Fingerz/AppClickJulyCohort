

## 🧠 **GIT & GITHUB CLASS NOTES**

### 1️⃣ **Download & Install Git**

#### **Windows**S

* Visit [https://git-scm.com/downloads](https://git-scm.com/downloads).
* Download the Windows version and follow the installer prompts.
* During installation, select:

  * “Use Git from the Windows Command Prompt.”
  * Default editor (VS Code recommended).
* Verify installation:

  ```bash
  git --version
  ```

#### **Mac**

* Option 1: Install via Homebrew

  ```bash
  brew install git
  ```
* Option 2: Download installer from [git-scm.com/download/mac](https://git-scm.com/download/mac)
* Verify installation:

  ```bash
  git --version
  ```

---

### 2️⃣ **Git Setup (Identity Configuration)**

Before using Git, set your user info (this appears in commits):

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your_email@example.com"
```

To verify:

```bash
git config --list
```

---

### 3️⃣ **Create a New Local Repository**

To initialize a new Git repository in your project folder:

```bash
cd path/to/project
git init
```

This creates a hidden `.git` folder that tracks changes.

---

### 4️⃣ **Stage & Commit Files**

#### **Stage (Add Files)**

Add files to the staging area:

```bash
git add filename
# or all files:
git add .
```

#### **Commit (Save Snapshot)**

Record the staged changes with a message:

```bash
git commit -m "Initial commit"
```

---

### 5️⃣ **GitHub: Push to a Remote Repository**

1. Create a new repository on **GitHub** (without README if already created locally).
2. Connect your local repo to GitHub:

   ```bash
   git remote add origin https://github.com/username/repo-name.git
   ```
3. Push your commits to GitHub:

   ```bash
   git branch -M main
   git push -u origin main
   ```

---

### 6️⃣ **GitHub: Clone (Download) a Repository**

To copy an existing repository to your computer:

```bash
git clone https://github.com/username/repo-name.git
```

This downloads the project and its commit history.

---

### 7️⃣ **Handling Merge Conflicts**

Conflicts happen when two people edit the same line of code.

**Steps to Resolve:**

1. Git marks conflict sections like:

   ```text
   <<<<<<< HEAD
   Your version
   =======
   Other version
   >>>>>>> branch-name
   ```
2. Edit the file to keep the correct content.
3. Mark as resolved:

   ```bash
   git add conflicted-file
   git commit
   ```

---

### 8️⃣ **View Commits & Undo Changes**

#### **View History**

```bash
git log
```

#### **Undo a Staged File**

```bash
git restore --staged filename
```

#### **Undo Last Commit (Keep Changes)**

```bash
git reset --soft HEAD~1
```

#### **Discard Changes**

```bash
git restore filename
```

---

### 9️⃣ **Branches: Create, Switch, Push, Merge, Delete**

#### **Create a Branch**

```bash
git branch feature-branch
```

#### **Switch Branch**

```bash
git checkout feature-branch
# or new syntax
git switch feature-branch
```

#### **Push Branch to GitHub**

```bash
git push -u origin feature-branch
```

#### **Merge Branch into Main**

1. Switch to main:

   ```bash
   git switch main
   ```
2. Merge:

   ```bash
   git merge feature-branch
   ```

#### **Delete Branch**

* Local:

  ```bash
  git branch -d feature-branch
  ```
* Remote:

  ```bash
  git push origin --delete feature-branch
  ```

---

## 💡 **Tips**

* Use `git status` often — it tells you what’s going on.
* Commit frequently with meaningful messages.
* Always pull before pushing (`git pull origin main`) to avoid conflicts.

---
