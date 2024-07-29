import os
import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from utils import *
pd.set_option('mode.chained_assignment', None)


def main():
    write_log("Starting the program")

    # load the driver
    driver = webdriver.Chrome()

    # Load environment variables
    load_dotenv()

    # Load the spreadsheet
    write_log("Loading the spreadsheet")
    xlsx = pd.ExcelFile('FILES.xlsx')

    # Load a sheet into a DataFrame by its name
    df_score = pd.read_excel(xlsx, sheet_name=0)
    df_comment = pd.read_excel(xlsx, sheet_name=1, header=1)

    count_cohort = df_score['Nama'].count()
    count_column_have_score = len(df_score.columns) - 3

    # Get email and password
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    write_log("Logging in")
    login(driver, email, password)

    write_log("Navigating to the evaluation page")
    write_log("=====================================")
    see_more_and_evaluation(driver)

    # sanitize check
    write_log("Sanitize check")
    checking_before_execute(driver, df_score, df_comment)
    write_log("Sanitize check finished")
    write_log("=====================================")

    # this is the main loop to process the students
    for i in range(1, count_cohort + 1):
        write_log(f"{i} - Processing Student - Start")
        name_score = click_students(driver, df_score, idx=i)

        # process the score and comment for each student
        for j in range(1, count_column_have_score + 1):
            process_score_comment_students(driver, name_score, df_comment, idx=j, idx_student=i)

        # save to draft and confirm draft
        draft_and_confirm(driver, count_column_have_score)

        write_log(f"{i} - Processing Student - Finish")
        write_log("=====================================")

    driver.quit()
    write_log("Program finished")
    

if __name__ == "__main__":
    main()