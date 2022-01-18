# Change log

## [1.3.0](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.3.0)-2021-1-15
* Features
   * Added the function of API automatic testing
* Improve
   * Improve the query speed of the vulnerability export interface
   * Improve the problem of missing hints in some content
* Fix
   * Fixed re-dos issue in regex validation
   * Fixed component export csv not correctly carrying UTF-8 BOM
   * Fixed the problem that the prompt information is inconsistent when the project information is modified
   * Fixed some content missing i18n part
   * Fixed the problem of component vulnerability display


## [1.2.0](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.2.0)-2021-12-18
* Features
   * Added license display of components
   * Added a set of interfaces to get the overview list by id
   * Added custom rule batch processing interface
   * Added component export function
* Improve
   * Improved the query speed of the component overview interface
* Fix
   * Fixed a bug that caused vulnerabilities to be undetected by modifying the strategy
   * Fixed the bug that failed to obtain data from the /api/v1/sensitive_info_rule/ page
   * Fixed the bug that the regular check is inconsistent with the engine

## [1.1.4](https://github.com/HXSecurity/DongTai-webapi/releases/tag/v1.1.4)-2021-12-18
* Improve
   * Split and add hooks to accommodate plugin development
* Fix
   * Fixed VulDetail when container is None , argument of type 'NoneType' is not iterable
   * Fixed VulSummary Inappropriate sql query causes API timeout 
   * Fixed The name of the scanning strategy is not brought back when returning
   * Fixed /api/v1/vulns local variable 'result' referenced before assignment
   * Fixed /api/v1/sensitive_info_rule/ fields No indication of range


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
   * Fixed the error that may be caused by agentid when the project is created
   * Fixed a non-atomic error when the project was created
   * Fixed permission errors when deleting data
