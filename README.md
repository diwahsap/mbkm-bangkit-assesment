# MBKM EvalAuto: Streamlined Mentor Evaluation System

## Overview
MBKM EvalAuto is an automation tool designed to simplify the evaluation process for mentors in the Kampus Merdeka (MBKM) program. It efficiently transfers initial and final evaluation scores from Bangkit Academy's Google Sheet (xlsx) directly into the MBKM platform. This automation significantly reduces the time and effort required for mentors to input scores manually, ensuring accuracy and consistency in the evaluation process.

> [!IMPORTANT]  
> **Final Evaluation Bangkit Academy 2024 H1**
> 
> New Version: Uses only Requests library and can run on Google Colab (no Selenium required)
> 
> [Google Colab Notebook](https://colab.research.google.com/drive/1EU8QpHNQ9MAIkXLFQMgWIBIwH6S3Acbx?authuser=0#scrollTo=cHUTbzz1quiI) - [Video Tutorial](https://youtu.be/mABOxEzuEtY)

> [!CAUTION]
> The previous version using Selenium is now DEPRECATED. Please use the new tutorial above!

## New Method (Recommended)
1. Open the [Google Colab Notebook](https://colab.research.google.com/drive/1EU8QpHNQ9MAIkXLFQMgWIBIwH6S3Acbx?authuser=0#scrollTo=cHUTbzz1quiI).
2. Follow the instructions in the notebook to run the automated evaluation process.
3. Watch the [Video Tutorial](https://youtu.be/mABOxEzuEtY) for a step-by-step guide.

## Additional Resources
- Bangkit Academy 2024 H1 - [Medium Article](https://diwahsap.medium.com/input-manual-otomatisasi-saja-7884f5366667)
- [Demo Video](https://youtu.be/zaWto1B92jg?si=ULhmLlDvguXPXTLg)

## Notes
This project now uses a simpler approach with the Requests library, making it easier to run and maintain. If you encounter any issues or have ideas for improvement, please contact the author at dim.mas.ws@gmail.com or @diwahsap on Discord.

---

> [!NOTE]
> The following information is for the deprecated version and is kept for reference purposes only.

## Deprecated Method (Not Recommended)

### Installation
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

### Files
- `main.py`: Contains the main program logic for automating the student evaluation process.
- `utils.py`: Provides various utility functions used in the automation process.
- `.env`: Contains your email and password used for logging into the dashboard.
- `file.xlsx`: Spreadsheet containing student information.
