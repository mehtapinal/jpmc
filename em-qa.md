Objective: To verify that the search functionality of the web application is reliable, efficient, and user-friendly.
- Viewport: Desktop web
- Filter: Birthday & Big groups
- Geolocation: London

# High level Test Plan:
This test plan focuses on depth of test cases and not breath(as suggested). The test plan also dwels into more whitebox testing to test APIs, cache and query optimizations

## Overview:
The Restaurant Finder feature on the desktop web allows users to find restaurants in London by applying filters such as price range, cuisine, perfect for, etc. The feature uses Fitz GraphQL API as the API gateway to communicate with backend services such as Basie Search and Contentful. The communication between these services occurs via HTTPS, and protocol buffers are used to serialize and deserialize data between Fitz and Basie.

## Testing Objectives:

* Ensure the Restaurant Finder feature is easy to use and accessible for users.
* Verify that the filtering mechanism is accurate and provides relevant results to users.
* Ensure that the search functionality is responsive and retrieves accurate results.
* Verify that the feature displays the correct information about each restaurant, such as opening hours, menu, location, and contact information.

## Testing Scope:
The following areas should be covered in testing the Restaurant Finder feature:
* Page loading and responsiveness
* Navigation to the Restaurant Finder feature
* Selection of filters and their effects on search results
* Search functionality and its accuracy
* Display of restaurant information

### Out of Scope:
* Testing of features or functionality outside of the scope of the Restaurant Finder, such as user authentication or account management
* Testing of third-party libraries or dependencies used by the application, unless they are critical to the Restaurant Finder feature and need to be explicitly tested
* Testing of non-standard or non-supported web browsers or operating systems.

## Test Cases: Functional tests
Page Loading and Responsiveness
* Verify that the page loads within a reasonable time frame and is responsive to user interactions.
* Ensure that the page layout is consistent across different web browsers and screen sizes.

Navigation to the Restaurant Finder feature
* Verify that the "Find A Place" button is easily accessible and functional.
* Ensure that the user is redirected to the Restaurant Finder page upon clicking the button.


Selection of filters and their effects on search results
* Verify that the filter options are displayed clearly and are easily selectable.
* Ensure that the selected filters are applied correctly and provide relevant search results

Search functionality and its accuracy
* Verify that the search bar is easily accessible and functional.
* Ensure that the search functionality is responsive and retrieves accurate results based on user input.
* We will test different types of searches, such as full-text search, fuzzy search, or boolean search to make sure search resutls are as expected

Display of restaurant information
* Verify that the restaurant information is displayed accurately and clearly.
* Ensure that the information is consistent with the actual restaurant details.

## API Tests: 
* Verify that the API is accessible and returns a valid response
* Verify that the Basie Search service is correctly querying data from Elasticsearch and returning it to Fitz
* Verify that appropriate error messages are displayed if the search page or API encounters errors (e.g. network error, server error, no search results found)
 
## Performance Tests:
* Test the search function with a large dataset and verify that the application returns results in a timely manner
* Test the search function with multiple users and verify that the application can handle high-volume search queries

## Negative Tests:
* Invalid input values: Try to enter invalid values in the search or filter fields, such as non-alphabetic characters in the name field or alphabetic characters in the distance field, and verify that appropriate error messages are displayed.
* Timeout scenarios: In a slow network environment, simulate a timeout scenario and ensure that appropriate error messages are displayed to the user.
* Invalid search queries: Enter invalid search queries, such as special characters or numbers, and verify that appropriate error messages are displayed.
* Enter an empty search query and verify that the application provides helpful feedback to the user
* Out-of-range filter values: Try to filter by price or distance values that are out of range, and verify that appropriate error messages are displayed.

## Compatibility Testing:
* Verify that the search page and API function correctly on the latest versions of major desktop web browsers/OS (Chrome, Firefox, Safari, Edge) / (mac, windows)

## Test Environment:
* The Restaurant Finder feature should be tested on a desktop web browser.
* The testing environment should mimic the production environment as closely as possible, including the infrastructure and backend services. For the purpose of this test, we will use a QA environment to perform testing.
* Build will be deployed automatically via CI/CD pipelines

## Test Execution:
* The test cases should be executed manually to ensure maximum coverage and accuracy.
* Test automation tools such as Cypress will be used to speed up the testing process and automate high-priority test 

Test Reporting:
* Test results should be documented, including any defects or issues found during testing.
* Defects should be reported to the development team for resolution and retested after fixes have been implemented.
* Jira will be used as a tool for creating a Quality Dashboard


## Risk Assessment:
The risk of critical defects affecting the Restaurant Finder feature is considered low, as the feature has been in production for some time and is generally stable.
However, the risk of minor defects affecting the user experience is moderate and should be addressed promptly to maintain user satisfaction.
One challenge to consider is ensuring the validity and correctness of the data generated from the search query. This can be a potential source of issues, especially if the search parameters are complex or the search results are being retrieved from an external API.
Observability:

In order to mitigate the risks, we will improve our monitoring and alerting capabilities.
Monitoring and alerting: Set up monitoring and alerting for the Restaurant Finder feature to detect any anomalies, errors, or performance issues. This can be done using tools like Prometheus, Grafana, and alert managers.
Logging: Ensure that the logs are being generated for the Restaurant Finder feature and they contain all the necessary information required to troubleshoot any issues that may arise.

## QA Resources:

*Test/Automation Engineers:* They will be responsible for creating and executing test cases, both manual and automated, for the feature.

*Performance Engineers:* They will be responsible for testing the performance and scalability of the feature.

*DevOps/Fullstack Engineers:* They will be responsible for setting up the test environment and integrating the test scripts with the CI/CD pipeline using Jenkins


## Conclusion:
Testing the Restaurant Finder feature on the desktop web requires a thorough and systematic approach to ensure the feature's functionality and accuracy.
By focusing on the areas outlined in this test plan, testers can verify that the feature is easy to use, functional, and provides relevant search results to users.


