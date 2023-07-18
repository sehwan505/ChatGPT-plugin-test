
# Korean Corporate's Disclosure Plugin

This project provides a plugin that returns Korean corporate disclosures. The plugin is designed to offer a simplified interface to fetch and analyze corporate disclosure data from Korean corporations. The application is served using FastAPI and Uvicorn.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.7 or later.
- You have installed FastAPI and Uvicorn. You can install these using pip:

```bash
pip install fastapi uvicorn
```

## Usage

To run the application locally:

1. Clone the repository:

```bash
git clone <repo_link>
```

2. Navigate into the cloned repository:

```bash
cd <repo_name>
```

3. Run the FastAPI application with Uvicorn:

```bash
uvicorn main:app --reload
```

Replace `main:app` with the appropriate module and application names if they're different.

After running the server, you can navigate to `http://localhost:8000` in your web browser to access the API documentation provided by FastAPI.

To use this plugin, make a GET request to the desired endpoint with the required parameters. For instance, to get a list of disclosures for a corporation, send a GET request to `/dart/get_disclosure_list_by_corporate`, passing the corporation's name as a query parameter.

## API Overview

The API offers five primary endpoints:

1. **/dart/get_disclosure_list_by_corporate**: Fetches a list of disclosures for a given corporation.
2. **/dart/get_contents_of_business**: Returns the business part in disclosure contents of a given disclosure ID (rcept_no).
3. **/dart/get_contents_of_investor_protection**: Returns essential information for investors in disclosure contents of a given disclosure ID (rcept_no).
4. **/dart/get_contents_of_management_diagnosis**: Returns the director's management diagnosis and analysis opinion in a given disclosure ID (rcept_no).
5. **/dart/financial_statement**: Fetches the financial statement of a given corporate for a specified year and quarter.

## Responses

The responses from these endpoints are generally in JSON format, providing information such as status, message, and the requested data.

## Dependencies

This project is built on OpenAPI version 3.0.1.

## Project Version

The current version of this project is v1.

## Server

The API is hosted on `https://dart-plugin.com`.

## Contributions

Contributions, issues, and feature requests are welcome.

## License

This project is licensed under the terms of the MIT license.

## Contact

If you have any questions or comments, please feel free to contact us.

## Disclaimer

This plugin does not provide financial advice. Please consult with a financial advisor before making any financial decisions based on the information provided by this plugin.
