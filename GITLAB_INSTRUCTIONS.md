# GitLab CI/CD Lab Instructions

- [GitLab CI/CD Lab Instructions](#gitlab-cicd-lab-instructions)
  - [Learning objectives](#learning-objectives)
  - [1. Fork the example](#1-fork-the-example)
  - [2. Enable CI/CD](#2-enable-cicd)
  - [3. Check for an instance runner](#3-check-for-an-instance-runner)
  - [4. Add a pipeline configuration file](#4-add-a-pipeline-configuration-file)
  - [5. Add a simple first job](#5-add-a-simple-first-job)
  - [6. Execute the Python program](#6-execute-the-python-program)
  - [7. Automate unit tests](#7-automate-unit-tests)
  - [8. Investigate a failing test](#8-investigate-a-failing-test)
  - [9. Add linting and parallel execution](#9-add-linting-and-parallel-execution)
  - [10. Configure triggers and rules](#10-configure-triggers-and-rules)
  - [11. Include the documentation build and deployment jobs](#11-include-the-documentation-build-and-deployment-jobs)
  - [12. Retrieve the documentation artifact](#12-retrieve-the-documentation-artifact)
  - [13. View the deployed documentation (optional)](#13-view-the-deployed-documentation-optional)
  - [14. Update the documentation and observe the pipeline](#14-update-the-documentation-and-observe-the-pipeline)
  - [Useful references](#useful-references)


In this lab you will create a CI/CD pipeline for a small Python project. You will start with a single job, then add automated code checks, tests, documentation generation and deployment to GitLab Pages.

You do not need to install Python, Git or Docker on your own computer. All the core exercises can be completed through the GitLab web interface.

## Learning objectives

By the end of the lab you should be able to:

- Create and edit a GitLab CI/CD configuration.
- Identify the runner, execution environment and commands used by a job.
- Automate existing development tasks using scripts.
- Interpret job logs and diagnose a failed pipeline.
- Configure parallel jobs, stages, triggers and conditions.
- Include an existing CI/CD configuration, retrieve artifacts and deploy a website.

## 1. Fork the example

1. Sign in to GitLab and open the example repository provided in class.
2. Select **Fork** at the top of the project page.
3. Select your own namespace under **Project URL**.
4. Keep the project name or choose your own.
5. Select **Fork project**.
6. Check that the project URL now refers to your namespace, not the instructor's namespace.

For the purposes of this lab, we will make changes directly to the `main` branch of your fork. Do not create merge requests to the original project. In a collaborative project, you would normally work on a separate branch and use merge requests.

The repository contains the following files and directories (other files may also be present):

| File or directory | Purpose |
| --- | --- |
| `src/example/hello.py` | A small Python greeting program. |
| `tests/test_hello.py` | Unit tests for the program. |
| `scripts/lint.sh` | Runs the linter (Ruff). |
| `scripts/test.sh` | Runs the unit tests (pytest). |
| `scripts/build_docs.sh` | Builds the Sphinx documentation. |
| `docs/source/` | Documentation source and configuration. |
| `deploy/gitlab-pages.yml` | Supplied documentation build and deployment jobs. |
| `pyproject.toml` | Python version, pinned dependencies and tool configuration. |

Note that the directory `.github` and its contents are not required for the GitLab version of this lab and may safely be deleted.

Open the Python program, tests and scripts in the repository to see what they do. You do not need to change them yet.

## 2. Enable CI/CD

In your forked project:

1. Navigate to **Settings > General**.
2. Expand **Visibility, project features, permissions**.
3. In the **Repository** section, ensure CI/CD is enabled.
4. Select **Save changes** if you changed any settings.
5. Check that the **Build** menu is visible in the left-hand sidebar.

## 3. Check for an instance runner

1. Navigate to **Settings > CI/CD** and expand **Runners**.
2. Open the **Instance** tab and check that instance runners are available and **Turn on instance runners for this project** is enabled. Optionally, you can have a look at the listed runners.

On GitLab.com, untagged jobs are normally assigned to the small hosted Linux x86-64 runner automatically. You do not need to register your own runner or select a specific runner. (NOTE: Account verification and available compute minutes may affect access.)

If using self-hosted GitLab, an eligible project or group runner can also be used. The runner must accept untagged jobs (or be configured with the appropriate tags) and support the specified container images. If there is no suitable runner, you will not be able to continue with the current lab. You may need to use GitLab.com or the GitHub version of the lab instead.

## 4. Add a pipeline configuration file

1. Navigate to **Code > Repository** and select the `main` branch.
2. At the repository root, select the **+** icon and then **New file**.
3. Name the file exactly:

   ```text
   .gitlab-ci.yml
   ```

This file must be at the same level as `README.md`. GitLab looks for this particular filename by default, so take care with the spelling.

YAML uses indentation to define structure. Use spaces rather than tabs and preserve the indentation in the examples.

## 5. Add a simple first job

Add the following to `.gitlab-ci.yml`:

```yaml
runner-check:
  image: python:3.13-slim
  script:
    - echo "Runner is working"
    - python --version
```

Select **Commit changes**, enter a descriptive commit message such as `Add runner check`, and commit to `main`. Make sure you are editing your own fork.

Committing through the web interface updates the remote repository directly. It has a similar effect to committing and pushing a change from a local Git repository.

With this basic configuration, a push to the branch triggers a pipeline automatically.

Inspect the pipeline:

1. Navigate to **Build > Pipelines**.
2. Open the newest pipeline by selecting its status or ID.
3. Select the `runner-check` job to open its log.

The pipeline contains one job in the default `test` stage. The job log should show runner and executor information, preparation of the Python container image, retrieval of the repository, execution of the two commands and cleanup.

Look for output similar to:

```text
Runner is working
Python 3.13.x
Job succeeded
```

The exact patch version and log messages may differ. The image may be pulled or already available to the runner.

**Checkpoint:** Confirm that the job and pipeline succeed. Identify the runner, executor, Python version and the two commands in the log. Do not continue until this works.

If there is no pipeline, check the filename, branch and CI/CD settings. If the job is pending, check runner availability and account or quota restrictions.

## 6. Execute the Python program

Open `.gitlab-ci.yml`, select **Edit > Edit single file**, and add one more command:

```yaml
runner-check:
  image: python:3.13-slim
  script:
    - echo "Runner is working"
    - python --version
    - python src/example/hello.py
```
This command will run the Python code in the file "hello.py", which you can view in the repo.

Commit to `main`, then inspect the new job log. You should see `Hello, World!`.

Notice that you did not have to manually clone the repository or install Python. GitLab prepared the execution environment and made the repository available to the job.

**Checkpoint:** Locate the greeting in the job log. The program executed on the runner, not on your computer.

## 7. Automate unit tests

The example repository already contains a script for running the unit tests. Replace the entire contents of `.gitlab-ci.yml` with:

```yaml
test:
  image: python:3.13-bookworm
  before_script:
    - python --version
    - python -m pip install --upgrade pip
    - python -m pip install --group dev -e .
  script:
    - bash scripts/test.sh
```
This will install the development dependencies specified in `pyproject.toml`, including `pytest`. It will then run the code in the script `test.sh`.

Commit and inspect the new job log.

The `before_script` commands install the development tools defined in `pyproject.toml`. The `script` command calls the existing test script. The full Python image is used from this point onwards because the later documentation build also needs Git for provenance.

**Checkpoint:** Find the dependency installation output and the pytest summary. All existing tests should pass.

## 8. Investigate a failing test

1. Open `src/example/hello.py` and edit the greeting returned by `greet()`. For example, change `Hello` to `Bonjour`, without changing the function signature.
2. Commit the change to `main` with the message `Introduce deliberate test failure`.
3. Open the newest pipeline and its `test` job log.
4. Locate the failed assertion and compare the expected and actual values.

pytest returns a non-zero exit code when tests fail. The job and pipeline should therefore fail. The commit itself is still present in the repository: a push-triggered pipeline runs after the commit reaches GitLab.

Now restore the original greeting in `src/example/hello.py`, commit the fix, and inspect the next pipeline.

**Checkpoint:** You should have a failed pipeline followed by a successful pipeline. You have diagnosed and fixed a failure without changing the CI/CD configuration.

## 9. Add linting and parallel execution

Replace the contents of `.gitlab-ci.yml` with:

```yaml
stages:
  - validate

default:
  image: python:3.13-bookworm
  before_script:
    - python --version
    - python -m pip install --upgrade pip
    - python -m pip install --group dev -e .

lint:
  stage: validate
  script:
    - bash scripts/lint.sh

test:
  stage: validate
  script:
    - bash scripts/test.sh
```

Commit and open the pipeline graph. (Go to **Build > Pipelines** and then click on the pipeline entry there.)

The `default` section supplies common configuration to both jobs, avoiding repetition. This does not mean that dependencies are installed only once: each job prepares its own execution environment.

Both jobs belong to the `validate` stage, so they can run independently and in parallel, provided runner capacity is available. Neither job depends on the other.

**Checkpoint:** Confirm that both jobs succeed. Inspect their logs and identify the commands that are common to both and those that differ.

## 10. Configure triggers and rules

Add the following at the top of `.gitlab-ci.yml`, above `stages:`. Keep all the existing content.

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH'
    - if: '$CI_PIPELINE_SOURCE == "web" && $CI_COMMIT_BRANCH'
```

Commit the change. The push should still create a pipeline.

`workflow: rules` controls whether a pipeline is created. These rules permit branch pushes and pipelines started manually through the GitLab web interface. Other sources, including schedules, tags and merge-request-specific pipelines, are not enabled by these rules.

To trigger a pipeline manually:

1. Navigate to **Build > Pipelines**.
2. Select **New pipeline**.
3. Select `main` and run the pipeline.

**Checkpoint:** Confirm that a new pipeline runs without a new commit. Compare its commit ID with the preceding pipeline.

## 11. Include the documentation build and deployment jobs
he next task involves building documentation and, where available, deploying it using GitLab Pages.

GitLab Pages is a service for hosting static websites, such as project documentation.

To check whether Pages is available for your project, go to **Settings > General > Visibility, project features, permissions** and ensure Pages is enabled.

Pages may not be available on all GitLab instances. If you cannot enable Pages, you can still complete the documentation build and artifact retrieval exercises. Instructions for disabling the deployment job are provided below.

The example repository contains files to build "read the docs" style documentation using the `sphinx` document builder. You do not need to modify those files, but you can view them in the `/docs` folder if you wish.

The repo also contains a predefined CI/CD configuration in `deploy/gitlab-pages.yml`. Open it and inspect its two jobs. *Do not edit it for this exercise*.

- `build-docs` runs the supplied Sphinx build script and saves the HTML as an artifact.
- `deploy-pages` retrieves that artifact and publishes the website, but only on the default branch.

Rather than copying these jobs into the main configuration, use `include` to incorporate them.

Add the following at the top of `.gitlab-ci.yml`:

```yaml
include:
  - local: 'deploy/gitlab-pages.yml'
```

Also extend the existing `stages` section to include `build` and `deploy`. *Make both changes in the same commit*. Your complete configuration should now be:

```yaml
include:
  - local: 'deploy/gitlab-pages.yml'

workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH'
    - if: '$CI_PIPELINE_SOURCE == "web" && $CI_COMMIT_BRANCH'

stages:
  - validate
  - build
  - deploy

default:
  image: python:3.13-bookworm
  before_script:
    - python --version
    - python -m pip install --upgrade pip
    - python -m pip install --group dev -e .

lint:
  stage: validate
  script:
    - bash scripts/lint.sh

test:
  stage: validate
  script:
    - bash scripts/test.sh
```
**Only if you were unable to enable Pages**, add the following to the end of your root `.gitlab-ci.yml` file before comitting. This overrides the rules for the deploy-pages job defined in the included configuration. GitLab will not add this job to the pipeline, but the documentation build job will still run and produce an artifact.

```yml
deploy-pages:
  rules:
    - when: never
```

GitLab incorporates the included configuration into the root configuration before creating a single pipeline. 

Commit and inspect the pipeline. You should see the following logical execution order:

|Stage|	Pages enabled	|Pages unavailable|
|--|--|--|
|validate|	lint, test|	lint, test|
|build|	build-docs|	build-docs|
|deploy	|deploy-pages	|Not included|


Both validation jobs must succeed before `build-docs` can run. `deploy-pages` then requires the output from `build-docs`.

Under **Build > Pipeline editor**, open the **Full configuration** tab to inspect the combined YAML. (GitLab may show an additional system-managed Pages deployment job or status here.)

**Checkpoint:** Checkpoint: Confirm that the lint, test and build-docs jobs have succeeded. If you have enabled Pages deployment, also confirm that the deploy-pages job has succeeded.

Your pipeline should succeed regardless of whether you have included the deployment job.

## 12. Retrieve the documentation artifact

1. Open the latest pipeline and select the `build-docs` job.
2. Locate the job artifacts and select **Download** (or use the artifact download control on the pipeline page).
3. Extract the downloaded archive on your computer.
4. Open `docs/build/html/index.html` from the extracted files in a browser.

Sphinx generated the website in the job execution environment. GitLab retained it after the job finished because the supplied configuration defines an artifact. You do not need Sphinx installed locally to view the HTML.

**Checkpoint:** Locate the API documentation and build provenance. Compare the displayed commit ID with the commit used by the pipeline.

## 13. View the deployed documentation (optional)

If you have disabled the deploy-pages job because GitLab Pages is unavailable, skip this exercise and proceed to section 14.

After the deployment succeeds, navigate to Deploy > Pages in your forked project. Open the website using the URL shown by GitLab. If prompted, sign in with an account that has access to the site.

The included configuration uses pages.publish to publish the generated HTML directory. Its deployment job retrieves the documentation artifact instead of rebuilding the website. The job-level rule limits deployment to the default branch.

If the site is not immediately available, check the Pages deployment status and refresh after deployment completes.

If deployment fails because Pages is unavailable, return to section 11 and follow the instructions for disabling the deployment job. Commit the updated configuration and confirm that the new pipeline succeeds.

Checkpoint: Open your deployed documentation website and locate the API reference and build provenance.

## 14. Update the documentation and observe the pipeline

1. Open `src/example/hello.py`.
2. Modify the `greet()` docstring, leaving the function's behaviour unchanged. For example, add a short explanatory sentence.
3. Commit to `main`.
4. Observe validation and documentation build in the new pipeline.
5. Confirm that the pipeline has succeeded.
6. Inspect the newly generated documentation:
   - If you have enabled Pages deployment, reopen your Pages website.
   - Otherwise, download and extract the new documentation artifact.
7. Check that the API reference contains your updated docstring and that the build provenance reflects your latest commit.

You have now implemented continuous integration for the project. A source code change automatically triggered validation checks and a documentation build, producing an artifact without any manual intervention.

If you also enabled Pages deployment, you have implemented continuous deployment of the documentation. Changes that pass validation are automatically built and published to the website.

## Useful references

- [GitLab CI/CD YAML reference](https://docs.gitlab.com/ci/yaml/)
- [GitLab pipeline editor](https://docs.gitlab.com/ci/pipeline_editor/)
- [GitLab runners](https://docs.gitlab.com/ci/runners/runners_scope/)
- [GitLab-hosted Linux runners](https://docs.gitlab.com/ci/runners/hosted_runners/linux/)
- [GitLab workflow rules](https://docs.gitlab.com/ci/yaml/workflow/)
- [GitLab includes](https://docs.gitlab.com/ci/yaml/includes/)
- [GitLab job artifacts](https://docs.gitlab.com/ci/jobs/job_artifacts/)
- [GitLab Pages](https://docs.gitlab.com/user/project/pages/)
