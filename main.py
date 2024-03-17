from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# Function to write log with timestamp
def write_log(message):
    """Write log message to the console and log file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(f"log.txt", "a") as log_file:
        log_file.write(log_message + "\n")

def click_element(element):
    element.click()

def login(driver, email, password):
    """login to dashboard using email and password"""
    driver.get('https://mentor.kampusmerdeka.kemdikbud.go.id/')

    email_input = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div/div[2]/div/div/main/div[2]/div[1]/div[2]/input')
    email_input.send_keys(email)

    password_input = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div/div[2]/div/div/main/div[2]/div[2]/div[2]/input')
    password_input.send_keys(password)

    login_button = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div/div[2]/div/div/main/div[3]/div/p')
    click_element(login_button)

def see_more_and_evaluation(driver):
    """after success login to dashboard, click see more and evaluation button to go to evaluation page"""
    # wait for the page to load
    driver.implicitly_wait(10)

    see_more_button = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/p')
    click_element(see_more_button)

    evaluation_button = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[2]')
    click_element(evaluation_button)

def process_score_comment_students(driver, name_score, df_comment, idx, idx_student):
    """
    Process the score and comment for a student based on the given index.

    Args:
        driver: The WebDriver object used for interacting with the web page.
        name_score: A DataFrame containing the scores for each student.
        df_comment: A DataFrame containing the comments for each student.
        idx: The index of the student to process.
        idx_student: The index of the student to process.

    Returns:
        None
    """
    header_name_xpath = f'//*[@id="root"]/div[4]/div/div[3]/div/div[3]/div[2]/div[{idx}]/p'
    header_name = driver.find_element_by_xpath(header_name_xpath).text
    write_log(f"{idx_student} - {idx} - {name_score['Nama'].values[0]} - {header_name} - Start Processing Score and Comment")
                                    
    # Find the score based on header_name
    score = name_score[header_name].values[0]

    # click on score dropdown
    score_dropdown = Select(driver.find_element_by_xpath(f'//*[@id="root"]/div[4]/div/div[3]/div/div[3]/div[2]/div[{idx}]/div/div[1]/div/div[2]/select'))
    score_dropdown.select_by_visible_text(str(score))
    write_log(f"{idx_student} - {idx} - {name_score['Nama'].values[0]} - {header_name} - {score}")

    if score <= 100 and score >= 70:
        # get all column based row value column "Course List" in df_comment
        comment = df_comment[df_comment['Course List'] == header_name].values[0][1]
        write_log(f"{idx_student} - {idx} - {name_score['Nama'].values[0]} - {header_name} - Atas - {comment}")
    else:
        comment = df_comment[df_comment['Course List'] == header_name].values[0][2]
        write_log(f"{idx_student} - {idx} - {name_score['Nama'].values[0]} - {header_name} - Bawah - {comment}")

    comment_area = driver.find_element_by_xpath(f'//*[@id="root"]/div[4]/div/div[3]/div/div[3]/div[2]/div[{idx}]/div/div[2]/div/div[2]/textarea')
    # clear text area so it can be filled with new comment
    comment_area.send_keys(Keys.COMMAND, "a") # change to Keys.CONTROL if you are using Windows
    comment_area.send_keys(Keys.DELETE)
    comment_area.send_keys(comment) # fill text area with new comment
    write_log(f"{idx_student} - {idx} - {name_score['Nama'].values[0]} - {header_name} - Fill Comment")

def click_students(driver, df_score, idx):
    """
    Clicks on a student element identified by the given index and retrieves the corresponding score from the provided DataFrame.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        df_score (DataFrame): The DataFrame containing student scores.
        idx (int): The index of the student element to click.

    Returns:
        DataFrame: The score information for the clicked student.
    """
    name_xpath = f'//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[{idx}]/div[1]/div/p'
    name_in_browser = driver.find_element_by_xpath(name_xpath).text
    write_log(f"{idx} - {name_in_browser.title()} - Get Name")

    # get the score based on name
    name_score = df_score[df_score['Nama'] == name_in_browser.title()]

    asses_xpath = f'//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[{idx}]/div[5]/div'
    asses_button = driver.find_element_by_xpath(asses_xpath)
    click_element(asses_button)
    write_log(f"{idx} - {name_in_browser.title()} - Click Assesment Button")
    
    return name_score
    
def draft_and_confirm(driver):
    """click save to draft and confirm draft button to save the evaluation to draft."""
    save_to_draft_button = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div/div[3]/div/div[3]/div[2]/div[21]/div[1]/div')
    driver.execute_script("arguments[0].click();", save_to_draft_button)

    confirm_draft_button = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div/div[4]/div')
    driver.execute_script("arguments[0].click();", confirm_draft_button)

write_log("Starting the program")
# load the driver
driver = webdriver.Chrome()

# Load the spreadsheet
write_log("Loading the spreadsheet")
xlsx = pd.ExcelFile('ML-59 - Initial Assessment Bangkit 2024 Batch 1.xlsx') # change to your file name

# Load a sheet into a DataFrame by its name
df_score = pd.read_excel(xlsx, sheet_name=0)
df_comment = pd.read_excel(xlsx, sheet_name=1, header=1)

count_cohort = df_score['Nama'].count()
count_column_have_score = len(df_score.columns) - 3 # 3 is the number of columns that are not have score

email = "FILL WITH YOUR EMAIL"
password = "FILL WITH YOUR PASSWORD"

write_log("Logging in")
login(driver, email, password)

write_log("Navigating to the evaluation page")
write_log("=====================================")
see_more_and_evaluation(driver)

# click students
# this is the main loop to process the students
for i in range(1, count_cohort + 1): 
    write_log(f"{i} - Processing Student - Start")
    name_score = click_students(driver, df_score, idx=i)

    # process the score and comment for each student
    for j in range(1, count_column_have_score + 1):
        process_score_comment_students(driver, name_score, df_comment, idx=j, idx_student=i)
    
    # save to draft and confirm draft
    draft_and_confirm(driver)

    write_log(f"{i} - Processing Student - Finish")
    write_log("=====================================")

driver.quit()
write_log("Program finished")
