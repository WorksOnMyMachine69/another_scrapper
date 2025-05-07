from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
import time
import os
import re
from creds import *

TIMEOUT_SHORT = 5
TIMEOUT_LONG = 10
OUT_DIR = "extract/"
JNF_DIR = f"{OUT_DIR}jnf/"
CTC_DIR = f"{OUT_DIR}ctc/"
DT1_DIR = f"{OUT_DIR}dt1/"
DT2_DIR = f"{OUT_DIR}dt2/"
PPT_DIR = f"{OUT_DIR}ppt/"
CSS_DIR = f"{JNF_DIR}css/"
NOT_DIR = f"{OUT_DIR}not/"
DTN_DIR = f"{OUT_DIR}dtn/"

driver = webdriver.Edge()
driver.implicitly_wait(TIMEOUT_LONG)

# login
driver.get("https://erp.iitkgp.ac.in")
driver.find_element(By.ID, "user_id").send_keys(ROLL_NO)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
time.sleep(TIMEOUT_SHORT)
ques = driver.find_element(By.ID, "question").text
driver.find_element(By.ID, "answer").send_keys(SECURITY_ANS[ques])
driver.find_element(By.ID, "getotp").click()

WebDriverWait(driver, TIMEOUT_LONG).until(EC.alert_is_present())
driver.switch_to.alert.accept()

otp = input("Enter OTP to login: ")
driver.find_element(By.ID, "email_otp1").send_keys(otp)
driver.find_element(By.ID, "loginFormSubmitButton").click()
time.sleep(TIMEOUT_SHORT)

# inside table
driver.get("https://erp.iitkgp.ac.in/TrainingPlacementSSO/TPStudent.jsp")
print("Login Sucessful!")
print("Loading profiles...")
time.sleep(TIMEOUT_LONG)

page_index = driver.find_element(By.CLASS_NAME, "ui-paging-info")
entry_count = int(page_index.text.split()[-1].replace(",", ""))
print(f"Total profiles: {entry_count}")


comp_df = pd.DataFrame(
    columns=[
        "Company",
        "Role",
        "CTC",
        "Additional Details 1",
        "Additional Details 2",
        "PPT",
        "Resume Upload Start",
        "Resume Upload End",
        "Interview/Selection",
    ]
)

comp_ids = []

curr_available = int(page_index.text.split()[3])
for idx in range(entry_count):
    while idx + 1 > curr_available:
        driver.find_element(By.ID, "grid37").send_keys(Keys.PAGE_DOWN)
        time.sleep(TIMEOUT_SHORT)
        page_index = driver.find_element(By.XPATH, '//*[@id="pager37_right"]/div')
        curr_available = int(page_index.text.split()[3])

    comp_name = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[2]').text
    comp_anch = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[5]/a')
    jnf_idx = comp_anch.get_attribute("onclick")[10:-2].replace('"', "").split(",")
    comp_role = comp_anch.text
    comp_ids.append(jnf_idx)
    comp_cost = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[7]').text
    comp_det1 = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[3]').text
    comp_det2 = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[9]').text
    comp_pptx = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[4]').text
    comp_resi = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[11]').text
    comp_reso = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[12]').text
    comp_intv = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[13]').text

    comp_df.loc[len(comp_df)] = [
        comp_name,
        f'<a href="{JNF_DIR}{idx+1}.html">{comp_role}</a>',
        f'<a href="{CTC_DIR}{idx+1}.html">{comp_cost}</a>',
        f'<a href="{DT1_DIR}{idx+1}.pdf">Show</a>' if len(comp_det1) else "",
        f'<a href="{DT2_DIR}{idx+1}.pdf">Show</a>' if len(comp_det2) else "",
        f'<a href="{PPT_DIR}{idx+1}.pdf">Show</a>' if len(comp_pptx) else "",
        comp_resi,
        comp_reso,
        comp_intv,
    ]
    print(f"Found profile {idx+1:3d}/{entry_count}: {comp_name}: {comp_role}")

os.makedirs(JNF_DIR, exist_ok=True)
os.makedirs(CTC_DIR, exist_ok=True)
os.makedirs(DT1_DIR, exist_ok=True)
os.makedirs(DT2_DIR, exist_ok=True)
os.makedirs(PPT_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)


cookies = driver.get_cookies()
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie["name"], cookie["value"])

# get the style sheet
response = session.get("https://erp.iitkgp.ac.in/TrainingPlacementSSO/css/style1_1.css")
with open(f"{CSS_DIR}style1_1.css", "wb") as file:
    file.write(response.content)

for idx in range(entry_count):
    namex = comp_df.iloc[idx, 0]
    rolex = comp_df.iloc[idx, 1].split(">")[1].split("<")[0]
    print(f"Scrapping profile {idx+1:3d}/{entry_count}: {namex}: {rolex}")

    # Extract ids
    jnf_idx = comp_ids[idx][0]
    com_idx = comp_ids[idx][1]
    yopx = comp_ids[idx][2]
    jnfx = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/TPJNFView.jsp?jnf_id={jnf_idx}&com_id={com_idx}&yop={yopx}&user_type=SU&rollno={ROLL_NO}"
    ctcx = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/JnfMoreDet.jsp?mode=jnfMoreDet&rollno={ROLL_NO}&year={yopx}&com_id={com_idx}&jnf_id={jnf_idx}"
    dt1x = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/AdmFilePDF.htm?type=COM&year={yopx}&com_id={com_idx}"
    dt2x = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/AdmFilePDF.htm?type=JNF&year={yopx}&jnf_id={jnf_idx}&com_id={com_idx}"
    pptx = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/AdmFilePDF.htm?type=PPT&year={yopx}&com_id={com_idx}"

    # GET all sources
    jnfx = session.get(jnfx)
    ctcx = session.get(ctcx)

    if len(comp_df.iloc[idx, 3]):
        driver.get(dt1x)
        for e in reversed(driver.requests):
            if e.url == dt1x:
                dt1x = e.response
                break

    if len(comp_df.iloc[idx, 4]):
        driver.get(dt2x)
        for e in reversed(driver.requests):
            if e.url == dt2x:
                dt2x = e.response
                break

    if len(comp_df.iloc[idx, 5]):
        driver.get(pptx)
        for e in reversed(driver.requests):
            if e.url == pptx:
                pptx = e.response
                del driver.requests
                break

    # Save responses
    with open(f"{JNF_DIR}{idx+1}.html", "w", encoding="UTF-8") as file:
        file.write(re.sub(rf"\b{ROLL_NO}\b", "", jnfx.text))
    with open(f"{CTC_DIR}{idx+1}.html", "w", encoding="UTF-8") as file:
        file.write(ctcx.text)
    if len(comp_df.iloc[idx, 3]):
        with open(f"{DT1_DIR}{idx+1}.pdf", "wb") as file:
            file.write(dt1x.body)
    if len(comp_df.iloc[idx, 4]):
        with open(f"{DT2_DIR}{idx+1}.pdf", "wb") as file:
            file.write(dt2x.body)
    if len(comp_df.iloc[idx, 5]):
        with open(f"{PPT_DIR}{idx+1}.pdf", "wb") as file:
            file.write(pptx.body)


comp_df.sort_values(by="Company", inplace=True)
comp_df.index = range(1, entry_count + 1)
comp_df.to_csv(f"{OUT_DIR}companies.csv", index=False)
comp_df.to_html("index_companies.html", render_links=True, escape=False)
print("Company profile scrapping complete!")
print(f"Table saved to {OUT_DIR}companies.csv and index_companies.html\n")


driver.get("https://erp.iitkgp.ac.in/TrainingPlacementSSO/Notice.jsp")
print("Loading notices...")
time.sleep(TIMEOUT_LONG)
page_index = driver.find_element(By.XPATH, '//*[@id="pager54_right"]/div')
entry_count = int(page_index.text.split()[-1].replace(",", ""))
print(f"Total notices: {entry_count}")


notice_df = pd.DataFrame(
    columns=[
        "Subject",
        "Company",
        "Notice",
        "Time",
        "Attachments",
        "IDFR",
    ]
)


curr_available = int(page_index.text.split()[3])
for idx in range(entry_count):
    while idx + 1 > curr_available:
        driver.find_element(By.XPATH, '//*[@id="grid54"]').send_keys(Keys.PAGE_DOWN)
        time.sleep(TIMEOUT_SHORT)
        page_index = driver.find_element(By.XPATH, '//*[@id="pager54_right"]/div')
        curr_available = int(page_index.text.split()[3].replace(",", ""))

    if driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[3]').text != "PLACEMENT":
        print(f"Found notice {idx+1:4d}/{entry_count}: skipped!")
        continue

    notice_subj = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[4]').text
    notice_comp = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[5]').text
    notice_anch = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[6]/a')
    notice_idfr = notice_anch.get_attribute("onclick")[11:-2].replace('"', "")
    notice_cont = notice_anch.text[:80]
    notice_time = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[8]').text
    notice_file = driver.find_element(By.XPATH, f'//*[@id="{idx}"]/td[9]').text

    notice_df.loc[len(notice_df)] = [
        notice_subj,
        notice_comp,
        f'<a href="{NOT_DIR}{idx+1}.html">{notice_cont}</a>',
        notice_time,
        f'<a href="{DTN_DIR}{idx+1}.pdf">Show</a>' if len(notice_file) else "",
        f"{notice_idfr},{idx+1}",
    ]
    print(f"Found notice {idx+1:4d}/{entry_count}: {notice_comp}: {notice_subj}")

cookies = driver.get_cookies()
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie["name"], cookie["value"])

os.makedirs(NOT_DIR, exist_ok=True)
os.makedirs(DTN_DIR, exist_ok=True)

for index, row in notice_df.iterrows():
    # Prepare sources
    idfx = row["IDFR"].split(",")
    yopx = idfx[0]
    nidx = idfx[1]
    notx = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/ShowContent.jsp?year={yopx}&id={nidx}"
    dtnx = f"https://erp.iitkgp.ac.in/TrainingPlacementSSO/AdmFilePDF.htm?type=NOTICE&year={yopx}&id={nidx}"

    notx = session.get(notx)
    if len(row["Attachments"]):
        driver.get(dtnx)
        for e in reversed(driver.requests):
            if e.url == dtnx:
                dtnx = e.response
                del driver.requests
                break

    print(
        f'Scrapping notice {index+1:4d}/{len(notice_df)} {row["Company"]}: {row["Subject"]}'
    )
    # Save responses
    with open(f"{NOT_DIR}{idfx[2]}.html", "w", encoding="UTF-8") as file:
        file.write(notx.text)
    if len(row["Attachments"]):
        with open(f"{DTN_DIR}{idfx[2]}.pdf", "wb") as file:
            file.write(dtnx.body)


notice_df.index = range(1, len(notice_df) + 1)
notice_df.drop("IDFR", axis=1, inplace=True)
notice_df.to_csv(f"{OUT_DIR}notices.csv", index=False)
notice_df.to_html("index_notices.html", render_links=True, escape=False)
print("Notice scrapping complete!")
print(f"Table saved to {OUT_DIR}notices.csv and index_notices.html")

driver.quit()
