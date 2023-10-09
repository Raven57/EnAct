import datetime
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import pandas

options = ChromeOptions()  
options.debugger_address = "127.0.0.1:" + '8888' # Adjust yout devtools port
browser = webdriver.Chrome(service=Service(executable_path="D:\chromedriver.exe"), options=options) # Adjust your chromedriver path

#Read CSV
data = pandas.read_csv('data.csv')

def build_function(ci,co,act,desc,is_off,dt):
    if dt.weekday() == 5 and is_off == True:
        ci = co = act = desc = 'OFF'
    return """
        $.ajax({
                    url: '/LogBook/StudentSave',
                    type: 'POST',
                    data: {
                        model: {
                            ID: curID,
                            LogBookHeaderID: curHeaderID,
                            Date: $("#editDate").val(),
                            Activity: '%s',
                            ClockIn: '%s',
                            ClockOut: '%s',
                            Description: '%s',
                            flagjulyactive: flagjulyactive
                        },

                    },
                    success: function (data) {
                        if (data.json != false) {
                            //alert(data.status);
                            //initMonthTab(curTabHeaderID);
                        }
                        else if (data.json == false) {
                            //alert(data.status);
                        }
                    },
                    error: function () {
                        alert("Application error. Please try again.");
                        //$.fancybox.close();
                    },
                    beforeSend: function () {
                        //showAlert('Loader', 'Loading...');
                    },
                    complete: function () {
                    }
                });
    
    """ % (act,ci,co,desc)

# Find buttons
entry_buttons = browser.find_elements(By.CLASS_NAME,"detailsbtn")

# Make click function to just update data, and not showing anything
browser.execute_script("""window.logBookEdit = function(datarow) {
        $("#editDate").val(datarow.date);
        curID = datarow.id;
        curHeaderID = datarow.logBookHeaderID;
    }
""")
i = 1 # Counter
print("Number of buttons: ",len(entry_buttons))

# Sat OFF?
off = True

# Iterate each button
# print(data)
for btn in entry_buttons:

    print("Editing: ",i)
    browser.execute_script("arguments[0].click();", btn)
    web_date = datetime.datetime.fromisoformat(browser.execute_script('return $("#editDate").val()'))
    idx = 0
    
    for i in range (0,len(data['date'])):
        if web_date.date() == datetime.date.fromisoformat(data['date'][i]):
            idx = i
            break
    
    print("Date: ",web_date.date())
    print("CI: ",data['clockin'][idx])
    print("CO: ",data['clockout'][idx])
    print("Act: ",data['activity'][idx])
    print("Desc: ",data['description'][idx])

    browser.execute_script(build_function(data['clockin'][idx],data['clockout'][idx],data['activity'][idx],data['description'][idx],off,web_date))
    i+=1
