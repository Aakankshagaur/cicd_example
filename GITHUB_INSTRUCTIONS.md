# GitHub CI/CD Lab Instructions

- [GitHub CI/CD Lab Instructions](#github-cicd-lab-instructions)
  - [Learning objectives](#learning-objectives)
  - [1. Fork the example](#1-fork-the-example)
  - [2. Enable GitHub Actions](#2-enable-github-actions)
  - [3. Check runner availability](#3-check-runner-availability)
  - [4. Add a workflow configuration file](#4-add-a-workflow-configuration-file)
  - [5. Add a simple first job](#5-add-a-simple-first-job)
    - [Inspect the workflow run](#inspect-the-workflow-run)
  - [6. Execute the Python program](#6-execute-the-python-program)
  - [7. Automate unit tests](#7-automate-unit-tests)
  - [8. Investigate a failing test](#8-investigate-a-failing-test)
  - [9. Add linting and parallel execution](#9-add-linting-and-parallel-execution)
  - [10. Configure triggers and conditions](#10-configure-triggers-and-conditions)
  - [11. Call the documentation build and deployment workflow](#11-call-the-documentation-build-and-deployment-workflow)
    - [Check whether Pages is available](#check-whether-pages-is-available)
    - [Inspect the supplied workflow](#inspect-the-supplied-workflow)
    - [Add the documentation workflow](#add-the-documentation-workflow)
    - [Complete configuration](#complete-configuration)
  - [12. Retrieve the documentation artifact](#12-retrieve-the-documentation-artifact)
  - [13. View the deployed documentation (where available)](#13-view-the-deployed-documentation-where-available)
  - [14. Update the documentation and observe the workflow run](#14-update-the-documentation-and-observe-the-workflow-run)
  - [Troubleshooting reference](#troubleshooting-reference)
  - [Useful references](#useful-references)


In this lab you will create a CI/CD pipeline (called a workflow in GitHub) for a small Python project. You will start with a single job, then add automated code checks, tests, documentation generation and, where available, deployment to GitHub Pages.

You do not need to install Python, Git or Docker on your own computer. All the core exercises can be completed through the GitHub web interface. This lab is intended for GitHub.com.

## Learning objectives

By the end of the lab you should be able to:

- Create and edit a GitHub Actions workflow configuration.
- Identify the runner, execution environment and commands used by a job.
- Automate existing development tasks using scripts.
- Interpret job logs and diagnose a failed workflow run.
- Configure parallel jobs, job dependencies, triggers and conditions.
- Call a reusable workflow, retrieve artifacts and, where available, deploy a website.

## 1. Fork the example

1. Sign in to GitHub.com and open the example repository provided in class.
2. Select **Fork** at the top of the repository page.
3. Select your personal account under **Owner**.
4. Keep the repository name or choose your own. A fork of a public repository is public. Do not add confidential information to it.
5. Select **Create fork**.
6. Check that the repository URL now refers to your account, not the original creator's account.

For the purposes of this lab, we will make changes directly to the `main` branch of your fork. Do not create pull requests to the original repository. In a collaborative project, you would normally work on a separate branch and use pull requests.

The repository contains the following files and directories (other files may also be present):

| File or directory | Purpose |
| --- | --- |
| `src/example/hello.py` | A small Python greeting program. |
| `tests/test_hello.py` | Unit tests for the program. |
| `scripts/lint.sh` | Runs the linter (Ruff). |
| `scripts/test.sh` | Runs the unit tests (pytest). |
| `scripts/build_docs.sh` | Builds the Sphinx documentation. |
| `docs/source/` | Documentation source and configuration. |
| `.github/workflows/docs.yml` | Supplied reusable workflow for documentation build and deployment. |
| `pyproject.toml` | Python version, pinned dependencies and tool configuration. |

Open the Python program, tests and scripts to see what they do. You do not need to change them yet. Confirm that `.github/workflows/docs.yml` is present and `.github/workflows/ci.yml` is not. The workflow defined in `docs.yml` does not run independently; you will call it later in the lab.

## 2. Enable GitHub Actions

In your forked repository:

1. Select the **Actions** tab.
2. If GitHub shows a message explaining that workflows are disabled on the fork, select the button to enable workflows (for example, **I understand my workflows, go ahead and enable them**).
3. Navigate to **Settings > Actions > General** if you need to check the repository's Actions permissions.
4. Under **Actions permissions**, ensure that actions and reusable workflows are permitted, including the official `actions/*` actions used in this lab. Save any changes.


## 3. Check runner availability

GitHub.com provides GitHub-hosted runners. Standard hosted runners are available without a compute-minute charge for public repositories. You do not need to register your own runner.

In this lab we will use `ubuntu-latest`, a label that selects a GitHub-hosted Linux execution environment. Unlike GitLab, GitHub Actions requires a runner selection for each ordinary job.

There is no need to enable an instance runner or select an individual machine. The first job in section 5 will confirm that your repository can actually use a hosted runner.


## 4. Add a workflow configuration file

1. Navigate to the **Code** tab in your fork and select the `main` branch.
2. Select **Add file > Create new file**.
3. Enter the following path in the filename field:

   ```text
   .github/workflows/ci.yml
   ```

   If you are already inside `.github/workflows/`, enter only `ci.yml`.

GitHub Actions looks for workflow YAML files directly inside `.github/workflows/`. Unlike GitLab, the filename is not fixed, but the directory is required. Do not edit the supplied `docs.yml` file.

YAML uses indentation to define structure. Use spaces rather than tabs and preserve the indentation in the examples.

## 5. Add a simple first job

Add the following to `.github/workflows/ci.yml`:

```yaml
name: CI/CD Example

on:
  push:
    branches:
      - '**'

permissions:
  contents: read

jobs:
  runner-check:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - run: echo "Runner is working"
      - run: python --version
```

Select **Commit changes**, enter a descriptive commit message such as `Add runner check`, and commit directly to `main`. Make sure you are editing your own fork.

Committing through the web interface updates the remote repository directly. It has a similar effect to committing and pushing a change from a local Git repository.

The `on` section tells GitHub to create a workflow run when a branch is updated. The pattern `'**'` matches all branch names, including names containing slashes. The `permissions` section grants read access to repository contents.

The `runs-on` setting selects the runner environment. The `steps` section defines the operations to execute sequentially within the job. The supplied `setup-python` action selects Python 3.13; a `run` step executes shell commands.

### Inspect the workflow run

1. Navigate to **Actions**.
2. Select the newest run of **CI/CD Example**.
3. Select the `runner-check` job to open its log.
4. Expand the individual steps to inspect their output.

The graph contains one job. The log should show the runner image, job preparation, the Python setup action, execution of the two commands and job cleanup. The setup action may use a cached Python installation or download one.

Look for output similar to:

```text
Runner is working
Python 3.13.x
```

The exact patch version and log messages may differ. GitHub reports success using the job and workflow status indicators.

**Checkpoint:** Confirm that the job and workflow run succeed. Identify the runner environment, Python version and two commands in the log. Do not continue until this works.

If no workflow run appears, check the file path, branch, trigger and Actions settings. If the job remains queued or fails before running your commands, check for hosted runner or account restrictions.

## 6. Execute the Python program

Open `.github/workflows/ci.yml` in the **Code** tab and select the pencil icon to edit it. Replace its contents with:

```yaml
name: CI/CD Example

on:
  push:
    branches:
      - '**'

permissions:
  contents: read

jobs:
  runner-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - run: echo "Runner is working"
      - run: python --version
      - run: python src/example/hello.py
```

Commit to `main`, then inspect the new job log. You should see `Hello, World!`.

GitHub does not automatically check out the repository into the job environment. The new `actions/checkout` step makes your committed source files available to the job. The Python setup action provides the requested Python version. You do not need to clone the repository or install Python on your own computer.

**Checkpoint:** Locate the "Hello, World!" greeting in the job log. The program executed on the runner, not on your computer.

## 7. Automate unit tests

The example repository already contains a script for running the unit tests. Replace the entire contents of `.github/workflows/ci.yml` with:

```yaml
name: CI/CD Example

on:
  push:
    branches:
      - '**'

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install --group dev -e .
      - name: Run tests
        run: bash scripts/test.sh
```

Commit and inspect the new job log. Note that this job will take longer than the previous jobs since it has more to do.

The **Install dependencies** step installs the development tools defined in `pyproject.toml`. The `|` character introduces a multi-line YAML value, allowing multiple shell commands in one step. The final step calls the existing test script rather than repeating its commands in the workflow configuration.

**Checkpoint:** Find the dependency installation output and the pytest summary. All existing tests should pass.

## 8. Investigate a failing test

1. Open `src/example/hello.py` and edit the greeting returned by `greet()`. For example, change `Hello` to `Bonjour`, without changing the function signature.

```py
return f"Bonjour, {name}!"
```

2. Commit the change to `main` with the message `Introduce deliberate test failure`.
3. Open the newest workflow run and its `test` job log.
4. Locate the failed assertion and compare the expected and actual values.

pytest returns a non-zero exit code when tests fail. The step, job and workflow run should therefore fail. The commit itself is still present in the repository: a push-triggered workflow runs after the commit reaches GitHub.

Now restore the original greeting in `src/example/hello.py`, commit the fix, and inspect the next workflow run.

**Checkpoint:** You should have a failed workflow run followed by a successful one. You have diagnosed and fixed a failure without changing the CI/CD configuration.

## 9. Add linting and parallel execution

Replace the contents of `.github/workflows/ci.yml` with:

```yaml
name: CI/CD Example

on:
  push:
    branches:
      - '**'

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install --group dev -e .
      - name: Run linting
        run: bash scripts/lint.sh

  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install --group dev -e .
      - name: Run tests
        run: bash scripts/test.sh
```

Commit and open the workflow run graph.

GitHub Actions does not have GitLab-style stages. These two jobs have no dependency on one another, so they can run independently and in parallel, provided runner capacity is available.

Each job runs in its own environment. The checkout, Python setup and dependency installation steps must therefore be performed for each job. The repeated configuration is intentional for this exercise.

**Checkpoint:** Confirm that both jobs succeed. Inspect their logs and identify the steps that are common to both and those that differ.

## 10. Configure triggers and conditions

The workflow already runs in response to branch pushes. Add a second trigger, `workflow_dispatch`, under the existing `on` section. The updated section should be:

```yaml
on:
  push:
    branches:
      - '**'
  workflow_dispatch:
```

Take care with spacing and alignment. Keep the remainder of the file unchanged. Commit the change. The push should still create a workflow run.

The two triggers permit branch pushes and workflows started manually through the GitHub web interface. Tag pushes, schedules and pull-request-specific events are not configured in this workflow.

To trigger a workflow manually:

1. Navigate to **Actions**.
2. Select **CI/CD Example** in the left-hand list of workflows.
3. Select **Run workflow**.
4. Select `main` and click **Run workflow** again.

The workflow file must be present on the default branch for the manual trigger to be available. (`main` is the default branch here, as is typical, but it is possible to choose a different default branch.)

**Checkpoint:** Confirm that a new workflow run starts without a new commit. Compare its commit ID with the preceding run.

## 11. Call the documentation build and deployment workflow

The next task involves building documentation and, where available, deploying it using GitHub Pages. GitHub Pages is a service for hosting static websites, such as project documentation.

### Check whether Pages is available

1. In your forked repository, navigate to **Settings > Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**, if available. Do not create a workflow from one of the suggested templates: the example repository already supplies one.

GitHub Pages is available for public repositories on GitHub Free. If Pages is unavailable, restricted, or you cannot configure it, do not spend time troubleshooting it. You can complete all the core exercises using the generated documentation artifact instead.

### Inspect the supplied workflow

The example repository contains files to build documentation using Sphinx. You do not need to modify those files, but you can view them in the `docs/` directory.

The repository also contains a predefined reusable workflow in `.github/workflows/docs.yml`. Open it and inspect its two jobs. *Do not edit it for this exercise.* 

(You may notice that the YAML for deploying GitHub Pages is significantly more involved than the equivalent YAML for GitLab Pages.)

- `build-docs` runs the supplied Sphinx build script and saves the HTML as an artifact named `sphinx-docs`. It also uploads a separate Pages-compatible artifact when deployment is enabled and the workflow runs on the default branch.
- `deploy-pages` uses the Pages-compatible artifact to publish the website, but only when deployment is enabled and the workflow runs on the default branch.

The supplied workflow declares `workflow_call` as its trigger. It will not run in response to a push by itself; another workflow must call it. It accepts a boolean input called `deploy-pages` to control publication.

Rather than copying these jobs into the main configuration, we will call the reusable workflow using `uses` at job level. 

### Add the documentation workflow

Add the following at the end of `.github/workflows/ci.yml`, under the existing `jobs` section, at the same indentation level as `lint` and `test`:

```yaml
  docs:
    needs: [lint, test]
    uses: ./.github/workflows/docs.yml
    with:
      deploy-pages: false
```

The `needs` setting requires both validation jobs to succeed before the documentation workflow runs. The `uses` setting references the supplied workflow in the same repository. The `with` section passes an input to that workflow.

If you successfully configured Pages above, replace this `docs` job with the following **before committing**:

```yaml
  docs:
    needs: [lint, test]
    uses: ./.github/workflows/docs.yml
    with:
      deploy-pages: true
    permissions:
      contents: read
      pages: write
      id-token: write
```

The additional permissions allow the called workflow to create a Pages deployment and authenticate it to GitHub. They are not needed for a documentation-only build. The reusable workflow restricts its build job to read access and inherits the calling job's permissions for deployment. *You do not need to create a personal access token*.

If Pages is unavailable, retain the first version with `deploy-pages: false`. The documentation build and artifact will still be generated.

### Complete configuration

Your complete configuration, with Pages disabled, should now be:

```yaml
name: CI/CD Example

on:
  push:
    branches:
      - '**'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install --group dev -e .
      - name: Run linting
        run: bash scripts/lint.sh

  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install --group dev -e .
      - name: Run tests
        run: bash scripts/test.sh

  docs:
    needs: [lint, test]
    uses: ./.github/workflows/docs.yml
    with:
      deploy-pages: false
```

If you enabled Pages, the final `docs` job should instead contain `deploy-pages: true` and the three permissions shown above. All other configuration is identical.

Commit and inspect the workflow graph. You should see the following logical execution order:

- lint, test (parallel jobs)
- docs/build-docs
- docs/deploy-pages (if enabled)

Both validation jobs must succeed before `build-docs` can run. If deployment is enabled, `deploy-pages` then requires the output from `build-docs`.

GitHub displays the jobs of a called workflow as part of the calling workflow run. Their displayed names may be prefixed with `docs /`. A reusable workflow call is not an ordinary job with its own runner; the jobs within the reusable workflow each define their own execution environments.

| Job | Pages enabled (on `main`) | Pages disabled |
| --- | --- | --- |
| `lint` | Runs | Runs |
| `test` | Runs | Runs |
| `build-docs` | Runs | Runs |
| `deploy-pages` | Runs | Skipped |

**Checkpoint:** Confirm that `lint`, `test` and `build-docs` succeed. If you enabled Pages, confirm that `deploy-pages` succeeds as well. If the deployment fails because Pages is unavailable, restore the build-only `docs` job shown above (`deploy-pages: false`, no job-level Pages permissions), commit and confirm that the new run succeeds. Do not modify the supplied reusable workflow.

## 12. Retrieve the documentation artifact

All students should complete this section, regardless of whether Pages is available.

1. Navigate to **Actions** and open the latest successful **CI/CD Example** workflow run.
2. On the run's **Summary** page, locate the **Artifacts** section.
3. Select the artifact named **sphinx-docs** to download it. Do not select `github-pages`, which is the separate deployment artifact.
4. Extract the downloaded ZIP archive on your computer.
5. Open `index.html` in the extracted directory in a browser. The archive contains the contents of `docs/build/html/`, so `index.html` is normally at the root of the extracted artifact.

Sphinx generated the website in the job execution environment. GitHub retained it after the job finished because the supplied configuration uploads an artifact. You do not need Sphinx installed locally to view the HTML.

**Checkpoint:** Locate the API documentation and build provenance. Compare the displayed commit ID with the commit used by the workflow run.

## 13. View the deployed documentation (where available)

If you have disabled Pages deployment, skip this section and proceed to section 14.

After the deployment succeeds, navigate to **Settings > Pages** in your forked repository. Open the website using the URL shown by GitHub (or use the deployment URL shown in the workflow run).

The reusable workflow uploads the HTML using `actions/upload-pages-artifact`. The deployment job uses `actions/deploy-pages` to publish that artifact instead of rebuilding the website. Its `needs` dependency ensures the build finishes first, and its `if` condition restricts deployment to the default branch when publication is enabled.

If the site is not immediately available, check the deployment job and Pages settings. A successful documentation build alone does not mean that the website has been published.

If Pages remains unavailable, return to section 11, disable deployment and confirm the new workflow run succeeds. Continue with section 14 using the documentation artifact instead.

**Checkpoint:** If Pages is available, open your deployed documentation website and locate the API reference and build provenance.

## 14. Update the documentation and observe the workflow run

1. Open `src/example/hello.py`.
2. Modify the `greet()` docstring, leaving the function's behaviour unchanged. For example, add a short explanatory sentence.
3. Commit to `main`.
4. Observe validation and documentation build in the new workflow run.
5. Confirm that the workflow run has succeeded.
6. Inspect the newly generated documentation:
   - If you enabled Pages deployment, reopen your Pages website.
   - Otherwise, download and extract the new `sphinx-docs` artifact as described in section 12.
7. Check that the API reference contains your updated docstring and that the build provenance reflects your latest commit.

You have now implemented continuous integration for the project. A source code change automatically triggered validation checks and a documentation build, producing an artifact without manual intervention.

If you also enabled Pages deployment, you have implemented continuous deployment of the documentation. Changes that pass validation are automatically built and published to the website.

## Troubleshooting reference

| Symptom | What to check |
| --- | --- |
| No workflow run is created | File path `.github/workflows/ci.yml`, selected branch, `on` triggers and Actions settings in your fork. |
| YAML configuration error | Indentation, spelling, job IDs, reusable workflow path and `workflow_call` input names. Check the error displayed by GitHub. |
| Job stays queued or fails before execution | Hosted runner availability, repository or organisation Actions policy, account and usage restrictions. |
| `pip` installation fails | Python version, package availability and dependency group syntax; inspect the installation log. |
| Script or file not found | Checkout step, path, filename, case and checked-out branch. |
| Lint or test fails | Inspect the reported issue, fix the code or test, and commit again. |
| Manual Run workflow button is missing | `workflow_dispatch` is present in the workflow on the default branch and you have write access. |
| Documentation build fails | Inspect Sphinx warnings/errors, imports and build paths. |
| Deployment permissions error | Check the calling `docs` job's permissions and Pages settings; if access is restricted, use the build-only configuration. |
| Pages site does not update | Check the `deploy-pages` input, default branch condition, deployment job and Pages publishing source. |

Avoid making unrelated changes to the YAML when the log identifies a failure in the Python code or documentation. Diagnose the failing component first.

## Useful references

- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Managing GitHub Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- [Manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
- [Reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Downloading workflow artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts)
- [Configuring a publishing source for GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
