# Change log

## [1.1.3](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.1.3)-2021-12-03

* Function
   * Projects are now sorted according to the time of obtaining component and vulnerability information
   * Added scan template policy management
   * Increase the vulnerability active verification switch (including global and project level)
* Improve
   * Component information now adds component path
   * Improved the original paging logic
   * Improved the original data verification to adapt to the boundary value
   * The agent name now gives priority to the alias when binding the agent
* Fix
   * Fix the error that may be caused by agentid when the project is created
   * Fixed a non-atomic error when the project was created
   * Fix permission errors when deleting data
