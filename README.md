# Automated Student Evaluation for Kampus Merdeka (MBKM)
> Bangkit Academy 2024 H1

## Overview
This project automates the initial assessment process for mentors to evaluate mentees in the [Kampus Merdeka (MBKM)](https://mentor.kampusmerdeka.kemdikbud.go.id/) program.

## Instalation
1. Clone this repository. Unzip and go to directory.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Download the [appropriate WebDriver for Selenium](https://www.lambdatest.com/learning-hub/install-selenium-python) (e.g., ChromeDriver) and place it in your PATH.
4. Ensure that the `spreadsheet (xlsx)` containing student information is present in the root directory. Don't forget to change xlsx file path at line 20 in `main.py` file.
5. Please fill the `.env` files with the following variables:
```
EMAIL=your_email@example.com
PASSWORD=your_password
```
6. Run the main.py script using `python main.py`.
7. The program will automatically log in to the specified website, navigate to the evaluation page, and process each student's score and comments.
8. Upon completion, the program will generate logs detailing the execution process.

## Files
- `main.py`: Contains the main program logic for automating the student evaluation process.
- `utils.py`: Provides various utility functions used in the automation process, such as logging, clicking elements, login, comparison checks, and more.
- `.env`: Contains your email and password used for logging into the dashboard. Ensure that you provide the correct credentials in this file.
- `file.xlsx`: Spreadsheet containing student information.

## Notes
This project assumes familiarity with web automation using Selenium and basic Python programming. If you have problem or (new) idea, you can contact me at dim.mas.ws@gmail.com or @diwahsap (Discord).