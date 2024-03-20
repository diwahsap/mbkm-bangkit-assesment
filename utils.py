import platform
from datetime import datetime
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
    """click an element. Sometimes click() method doesn't work, so we need to use execute_script() method."""
    element.click()

def execute_click(driver, element):
    """Executes a JavaScript click event on the given element.

    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        element (WebElement): The element to click.

    Returns:
        None
    """
    driver.execute_script("arguments[0].click();", element)

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

    see_more_button = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/p')
    click_element(see_more_button)

    evaluation_button = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div[3]/div[2]')
    click_element(evaluation_button)

def compare_student(driver, df_score):
    """
    Compare the student information in the browser with the student information in the df_score DataFrame.

    Args:
        driver: The WebDriver object used to interact with the browser.
        df_score: The DataFrame containing the student information.

    Returns:
        None
    """
    write_log("Start comparing student in browser and df_score")

    get_student_number_in_browser = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/p/span')
    
    text = get_student_number_in_browser.text  # 'xx active participants'
    count_student_browser = int(text.split()[0])  # xx number
    # check the number of active participants
    write_log(f"There are {count_student_browser} students in the browser.")

    count_student_in_df = df_score['Nama'].count()
    write_log(f"There are {count_student_in_df} students in the df_score.")

    if count_student_browser == count_student_in_df:
        write_log("Total Student in Browser and Total Student in df_score is SAME.")
    else:
        write_log("Total Student in Browser and Total Student in df_score is DIFFERENT. Don't worry, we will process it anyway.")

    browser_student_name = [] # list to store student name in browser
    # get the student_name in browser
    for i in range(1, count_student_browser + 1):
        name_xpath = f'//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[{i}]/div[1]/div/p'
        name_in_browser = driver.find_element_by_xpath(name_xpath).text
        browser_student_name.append(name_in_browser)
    
    # compare student name in browser and student name in df_score
    student_name_in_df = df_score['Nama'].tolist()

    if sorted(browser_student_name) == sorted(student_name_in_df):
        write_log("Student name in Browser and Student Name in df_score is SAME")
    else:
        write_log("Student name in Browser and Student Name in df_score is DIFFERENT. Don't worry, we will process it anyway.")

def compare_skills_name(driver, df_score, df_comment):
    """
    Compare the skills names between different sources.

    Args:
        driver: The Selenium WebDriver instance.
        df_score: The DataFrame containing the score data.
        df_comment: The DataFrame containing the comment data.

    Returns:
        None
    """
    write_log("Start comparing skills name in browser, df_score, and df_comment")

    count_student_skill_df_score = len(df_score.columns) - 3

    student_skill_browser = []
    for i in range(1, count_student_skill_df_score + 1):
        skill_name_xpath = f'//*[@id="root"]/div[4]/div/div[3]/div/div[3]/div[2]/div[{i}]/p'
        skill_in_browser = driver.find_element_by_xpath(skill_name_xpath).text
        student_skill_browser.append(skill_in_browser)

    student_skill_sheet1 = sorted(df_score.columns.tolist()[3:]) 
    student_skill_sheet2 = sorted(df_comment["Course List"].tolist())
    if student_skill_sheet1 == student_skill_sheet2 == sorted(student_skill_browser):
        write_log("Student skills name in Browser, df_score, and df_comment is SAME")
    else:
        write_log("Student skills name in Browser, df_score, and df_comment is DIFFERENT. Don't worry, we will process it anyway.")

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

    # make the column in name_score to lower case
    name_score.columns = name_score.columns.str.lower()
    name_score.rename(columns = {'nama':'Nama'}, inplace = True) 

    # Find the score based on header_name (case insensitive)
    score = name_score[header_name.lower()].values[0]

    # click on score dropdown
    score_dropdown = Select(driver.find_element_by_xpath(f'//*[@id="root"]/div[4]/div/div[3]/div/div[3]/div[2]/div[{idx}]/div/div[1]/div/div[2]/select'))
    score_dropdown.select_by_visible_text(str(score))
    write_log(f"{idx_student} - {idx} - {name_score['Nama'].values[0]} - {header_name} - {score}")

    if score <= 100 and score >= 70:
        # get all column based row value column "Course List" in df_comment (case insensitive)
        comment = df_comment[df_comment['Course List'].str.lower() == header_name.lower()].values[0][1]
        write_log(f"{idx_student} - {idx} - {name_score['Nama'].values[0]} - {header_name} - Atas - {comment}")
    else:
        comment = df_comment[df_comment['Course List'].str.lower() == header_name.lower()].values[0][2]
        write_log(f"{idx_student} - {idx} - {name_score['Nama'].values[0]} - {header_name} - Bawah - {comment}")

    comment_area = driver.find_element_by_xpath(f'//*[@id="root"]/div[4]/div/div[3]/div/div[3]/div[2]/div[{idx}]/div/div[2]/div/div[2]/textarea')
    # clear text area so it can be filled with new comment
    if platform.system() == "Darwin":
        comment_area.send_keys(Keys.COMMAND, "a")
    else:
        comment_area.send_keys(Keys.CONTROL, "a")
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

    # get the score based on name (case insensitive)
    name_score = df_score[df_score['Nama'].str.lower() == name_in_browser.lower()]

    asses_xpath = f'//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[{idx}]/div[5]/div'
    asses_button = driver.find_element_by_xpath(asses_xpath)
    execute_click(driver, asses_button)
    write_log(f"{idx} - {name_in_browser.title()} - Click Assesment Button")
    
    return name_score
    
def checking_before_execute(driver, df_score, df_comment):
    """
    Perform pre-execution checks before executing a task.

    Args:
        driver: The WebDriver instance used for browser automation.
        df_score: The DataFrame containing score data.
        df_comment: The DataFrame containing comment data.

    Returns:
        None
    """
    compare_student(driver, df_score)

    asses_xpath = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[1]/div[5]/div')
    execute_click(driver, asses_xpath)

    compare_skills_name(driver, df_score, df_comment)

    go_back_xpath = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div/div[5]/div/div/div/div/div/div')
    execute_click(driver, go_back_xpath)

def draft_and_confirm(driver, count_column_have_score):
    """click save to draft and confirm draft button to save the evaluation to draft.
    
    Args:
        driver (WebDriver): The WebDriver instance used for browser automation.
        count_column_have_score (int): count of assesment. Need for get xpath draft button. 
                            +3 based by count of container.
                            ML is 18 assesement, MD is 14. 
                            18 + 3 = 21, xpath code for draft ml
                            14 + 3 = 17, xpath code fro draft md
        
    Returns:
        None
    """
    save_to_draft_button = driver.find_element_by_xpath(f'//*[@id="root"]/div[4]/div/div[3]/div/div[3]/div[2]/div[{count_column_have_score + 3}]/div[1]/div')
    execute_click(driver, save_to_draft_button)

    confirm_draft_button = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div[2]/div/div[4]/div')
    execute_click(driver, confirm_draft_button)
