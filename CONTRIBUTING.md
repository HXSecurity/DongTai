# Contributing to DongTai IAST

Thank you for considering contributing to DongTai IAST. You can contribute to DongTai IAST in many ways: 

- reporting-issues
- code-contributions

## Bug reports

If you think you have found a bug in DongTai IAST, first make sure that you are testing against the latest version of DongTai IAST - your issue may already have been fixed. If not, please follow the prompts to describe the bug as completely as possible when [submitting the issue](https://github.com/HXSecurity/DongTai/issues/new?assignees=exexute&labels=bug&projects=1&template=bug_report.yaml). 

## Feature requests

If you find yourself wishing for a feature that doesn't exist in DongTai IAST, please [submit your issue](https://github.com/HXSecurity/DongTai/issues/new?assignees=exexute&labels=feature&projects=1&template=feature_request.yaml). We look forward to getting more user’s needs. 

## Contributing code

If you would like to contribute a new feature or a bug fix to DongTai IAST, please discuss your idea first on the Github issue. If there is no Github issue for your idea, please open one. We always pay attention to the issue and provide solutions. If you have never created a pull request before, here is a tutorial on how to create a pull request. 

1. If you want to write code that you would like to contribute to the DongTai IAST, following these guidelines will make it easier for the DongTai IAST development team to review and accept your changes. 

   **Coding Guidelines**

   	- Following the Latest Source Code
   	- Neat code formatting
    - Commits
      	- Look through all of your changes in your patch or pull request before you submit it to us. Make sure that everything you've changed is there for a reason.
      	- Please don't include unfinished work to the patch. Make sure that it doesn't contain any TODO comments. If you added some code and ended up not needing it, please make sure that you delete it before you submit your patch.
      	- Please don't include any changes that affect formatting, fixing "yellow code" (warnings), or code style along with actual changes that fix a bug or implement a feature. No one likes to leave poor code, but remember that having these changes mixed complicates the process of review.
      	- Please don't fix multiple problems within a single patch or pull request.
      	- Please avoid moving or renaming classes unless it is necessary for the fix.

2. Fork the project, clone your fork:

   ```shell
   git clone https://github.com/<your-username>/<repo-name>
   ```

3. If you cloned a while ago, get the latest changes from upstream:

   ```shell
   git checkout main
   git pull upstream main
   git submodule init
   ```

4. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix:

   ```shell
   git checkout -b <topic-branch-name>
   ```

5. Push your topic branch up to your fork:

   ```shell
   git push origin <topic-branch-name>
   ```

6. Open a Pull Request with a clear title and description.

## Contributor Resources

### Contributor Level

- **Contributor** You can become a contributor by submit a valid ISSUE, pass a PR, or answer user’s question in the community
- **maintainers** First, you need to be a contributor; Second, you have submitted important issues /PR or other outstanding contributions; Existing maintainers and core development then discuss whether to allow them to join the maintainer team.
- **core members** Core members need to be maintainers, and then, have their own ideas and insights on the development of the product, can put forward key suggestions or develop related functions; The existing core members discuss together and decide whether to allow them to join the core team.

