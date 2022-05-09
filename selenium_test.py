# pip install webdriver-manager
from audioop import add
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import time
import pandas as pd
import random


emojis_prefixes = ["#interesting", "#just", "#learning", "#lost",
                   "#needs", "#question", "#real", "#surprised", "#i", "#lets", "#lightbulb", "#important"]

emojis_hashes = [
    '1edea120-6011-11ec-8fb7-df1993aaa1da',
    '1ee11221-6011-11ec-8fb7-df1993aaa1da',
    '1ede5300-6011-11ec-8fb7-df1993aaa1da',
    '1ede7a10-6011-11ec-8fb7-df1993aaa1da',
    '1ee11220-6011-11ec-8fb7-df1993aaa1da',
    '1ee16040-6011-11ec-8fb7-df1993aaa1da',
    '1ee0eb10-6011-11ec-8fb7-df1993aaa1da',
    '1ee16041-6011-11ec-8fb7-df1993aaa1da',
    '1ee44670-6011-11ec-8fb7-df1993aaa1da',
    '1ede04e0-6011-11ec-8fb7-df1993aaa1da',
    '1edccc60-6011-11ec-8fb7-df1993aaa1da',
    '1ee509c0-6011-11ec-8fb7-df1993aaa1da',
]
NUM_OF_EMOJIS = len(emojis_prefixes)
FIRST_LINE = 53
SECOND_PARA_FIRST_LINE = 76

NB_BOOKMARK_SCRIPT = """
        let s = document.createElement('script');
        s.src= 'https://127.0.0.1:3001/js/bundle.js';
        document.body.append(s);
      """

def add_comment_with_emojis(xpath, comment_content="", emojis_prefix=[], is_first_comment=True):
    """
    :param xpath: the xpath of the text we want to add comment on
    :param comment_content: comment content
    :param emojis_prefix: prefixes of the emojis we want to add to the comment
    :param is_first_comment: boolean flag that indicates rather this is the first comment added to this text or not
    :return: void
    """
    # select some text
    selected_text = driver.find_element(by="xpath", value=xpath)
    actionChains.triple_click(selected_text).perform()
    # add some comment
    # if is_first_comment:
    try:
        input = driver.find_element(
            by="xpath", value="//*[@id='nb-sidebar']/div[7]/div[2]/div/div[2]/div[1]")   
    # else:
    except Exception as e:
        input = driver.find_element(
            by="xpath", value="//*[@id='nb-sidebar']/div[8]/div[2]/div/div[2]/div[1]")
    input.send_keys(comment_content)
    # input.send_keys(Keys.ENTER)
    for emoji_prefix in emojis_prefix:
        input.send_keys(emoji_prefix)
        input.send_keys(Keys.TAB)
    # if is_first_comment:
    try:
        driver.find_element(
            by="xpath", value="//*[@id='nb-sidebar']/div[7]/div[3]/div[2]/div/button[2]").click()
    # else:
    except Exception as e:
        driver.find_element(
            by="xpath", value="//*[@id='nb-sidebar']/div[8]/div[3]/div[2]/div/button[2]").click()



def add_subset_of_the_emojis(emojis_subset_size, from_line, to_line):
    """
    :param emojis_subset_size: max size of the emojis subset we would like to chose from the all emojis
    :param from_line: first line of the text we will paint
    :param to_line: last line of the text we will paint
    :return: void
    This function adds multiple emojis to the doc from @from_line to @to_line, the number of the emojis it adds is
    determined based on @emoji_subset_size
    """
    i = 0
    is_first_comment = True
    while i < emojis_subset_size:
        if i != 0:
            is_first_comment = False
        for j in range(from_line, to_line):
            add_comment_with_emojis("//*[@id='viewer']/div[1]/div[2]/span[" + str(
                j) + "]", emojis_prefix=[emojis_prefixes[i]], is_first_comment=is_first_comment)
            i = i + 1

def populate_func(emojis_subset_size, from_line, to_line, page):
    # random number of comments in each line (1-5)
    # random number of emojis in each line (1-3)
    
    for j in range(from_line, to_line):
        num_of_comments = random.randrange(1,5)
        is_first_comment = True
        i = 0
        while i < num_of_comments:
            num_of_emojis = random.randrange(1,3)
            if i != 0:
                is_first_comment = False
            curr_emojis_prefixes = []
            for k in range(num_of_emojis):
                curr_emojis_prefixes.append(emojis_prefixes[random.randrange(0,11)])
            add_comment_with_emojis("//*[@id='viewer']/div[" + str(page) + "]/div[2]/span[" + str(
                j) + "]", emojis_prefix=curr_emojis_prefixes, is_first_comment=is_first_comment)
            i = i + 1

def setup():
    """
    :return: void
    This is a set up function which is called before we start our test session
    The function used to open the website with the bundle then typing the user + password and then entering the
    doc which we will run our test seesion on
    """
    # ================ setup =====================
    driver.get('https://127.0.0.1:3001/js/bundle.js')
    driver.implicitly_wait(1)  # seconds
    driver.find_element(by="xpath", value="//*[@id='details-button']").click()
    driver.find_element(by="xpath", value="//*[@id='proceed-link']").click()
    driver.execute_script(
        "window.open('https://localhost:8080/', 'secondtab');")
    driver.close()
    driver.switch_to.window("secondtab")
    driver.find_element(by="xpath", value="//*[@id='details-button']").click()
    driver.find_element(by="xpath", value="//*[@id='proceed-link']").click()

    # ================ connection =====================
    input = driver.find_element(by="id", value="login-username")
    input.send_keys("test")
    input = driver.find_element(by="id", value="login-password")
    input.send_keys("123456")
    input.send_keys(Keys.ENTER)

    # ================ enter the reading material =====================
    driver.find_element(
        by="xpath", value="//*[@id='app']/div/div/div[1]/div[2]/div[1]").click()
    driver.find_element(
        by="xpath", value="//*[@id='vgt-table']/tbody/tr[2]/td[2]/span/a").click() 

    driver.execute_script(NB_BOOKMARK_SCRIPT)
    sleep(1)
    # ================ connection =====================
    input = driver.find_element(by="id", value="login-username")
    input.send_keys("test")
    input = driver.find_element(by="id", value="login-password")
    input.send_keys("123456")
    input.send_keys(Keys.ENTER)


def enter_emoji_heatmap_mode():
    """
    :return: void
    This function is used to enter emoji heatmap mode by clicking the relevant button.
    """
    driver.find_element(
        by='xpath', value="//*[@id='nb-sidebar']/div[3]/button[2]").click()


def enter_default_heatmap_mode():
    """
    :return: void
    This function is used to enter default heatmap mode by clicking the relevant button.
    """
    driver.find_element(
        by='xpath', value="//*[@id='nb-sidebar']/div[3]/button[1]").click()

def toggle_heatmap():
    """
    :return: void
    This function is used to toggle heatmap (show and hide) by clicking the relevant button.
    """
    driver.find_element(
        by='xpath', value="//*[@id='nb-sidebar']/div[4]/div/div[1]/span[2]").click()


def hide_and_show_heatmap():
    """
    :return: void
    This function is used to toggle heatmap (show and hide) twice by calling toggle heatmap twice.
    """
    toggle_heatmap()
    # sleep(1)
    toggle_heatmap()


def delete_all_comments():
    """
    :return: void
    This function is used mostly between tests, as the name implies the function deletes all the comments the current
    doc has.
    """
    try:
        while (True):
            driver.find_element(
                by="xpath", value="//*[@id='nb-sidebar']/div[4]/div/div[2]/div[1]").click()
            driver.find_element(
                by="xpath", value="//*[@id='nb-sidebar']/div[5]/div[2]/div/div[1]/div/div").click()
            driver.find_element(
                by="xpath", value="/html/body/div[4]/div[2]/div/div[1]/div[1]/div/div[3]").click()

            # driver.find_element(
            #     by="xpath", value=" //*[@id='popover_7we9qzpkc8']/div/div[1]/div[1]/div/div[3]").click()

    except:
        return


def timeit(method):
    """
    :param method: Test function which we would like to asses is duration time.
    :return: void
    This is a decorator function which we use to log the duration of each test
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' %
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


def add_x_comments_to_y_different_lines(x, y):
    """
    :param x: number of comments we would like to add to the doc
    :param y: number of lines we would like to add comments to(staring from FIRST_LINE)
    :return: void
    This function adds @x comments to @y lines starting from FIRST_LINE
    """
    for i in range(y):
        add_comment_with_emojis(
            xpath="//*[@id='viewer']/div[1]/div[2]/span[" + str(FIRST_LINE + i) + "]", comment_content="comment")
        for j in range(x - 1):
            add_comment_with_emojis(xpath="//*[@id='viewer']/div[1]/div[2]/span[" + str(
                FIRST_LINE + i) + "]", comment_content="comment", is_first_comment=False)


def go_throw_all_emoji_filters_one_by_one(sleep_time_between_filters):
    """
    :param sleep_time_between_filters: boolean flag which we use
    :return: void
    This function is used to check the heatmap with different emojis filters.
    It filter the comments based on all the emojis, one by one with option to wait @sleep_time_between_filters
    seconds in between.
    """
    driver.find_element(
        by="xpath", value="//*[@id='nb-sidebar']/div[2]/div/div[2]/div").click()
    for emoji_hash in emojis_hashes:
        driver.find_element(
            by="xpath", value="//*[@id='filter-hashtag-" + emoji_hash + "']").click()
        sleep(sleep_time_between_filters)
        driver.find_element(
            by="xpath", value="//*[@id='filter-hashtag-" + emoji_hash + "']").click()
    driver.find_element(
        by="xpath", value="//*[@id='viewer']/div[1]/div[2]").click()
    sleep(sleep_time_between_filters)


class TestNB(unittest.TestCase):
    # @timeit
    # def test_AA_populate_with_comments(self):
    #     enter_emoji_heatmap_mode()
    #     for i in range(2,8):
    #         populate_func(
    #             NUM_OF_EMOJIS, 80, 91, i)

    @timeit
    def test_A_toggle_between_heatmap_modes(self):
        """
        :return: void
        basic test which checks the new button of emoji heatmap mode,
        it does so by toggling heatmap mode twice
        """
        enter_emoji_heatmap_mode()
        enter_default_heatmap_mode()

    @timeit
    def test_B_enter_emoji_heatmap_mode(self):
        """
        :return: void
        basic test which checks the new button of emoji heatmap mode, it does so by entering emoji heatmap mode
        """
        enter_emoji_heatmap_mode()

    @timeit
    def test_C_add_different_subsets_of_the_emojis_different_lines(self):
        """
        :return: void
        Test is adding subsets of the emojis (from size 0 to |all emojis| to different lines
        """
        for i in range(len(emojis_prefixes)):
            add_subset_of_the_emojis(i, FIRST_LINE, FIRST_LINE + i + 1)
            enter_emoji_heatmap_mode()
            # sleep(1)
            enter_default_heatmap_mode()
            # sleep(1)
            delete_all_comments()

    @timeit
    def test_D_add_different_subsets_of_the_emojis_same_line(self):
        """
        :return: void
        Test is adding subsets of the emojis (from size 0 to |all emojis| to FIRST_LINE
        """
        for i in range(len(emojis_prefixes)):
            add_subset_of_the_emojis(i, FIRST_LINE, FIRST_LINE + 1)
            enter_emoji_heatmap_mode()
            # sleep(1)
            enter_default_heatmap_mode()
            # sleep(1)
            delete_all_comments()

    @timeit
    def test_E_add_all_kind_of_emojis_different_lines_with_filters(self):
        """
        :return: void
        Test is adding comments with all the possible emojis to different lines
        Then it filter the comment based on all the emojis (one by one)
        """
        add_subset_of_the_emojis(
            NUM_OF_EMOJIS, FIRST_LINE, FIRST_LINE + NUM_OF_EMOJIS)
        enter_emoji_heatmap_mode()
        # sleep(3)
        go_throw_all_emoji_filters_one_by_one(0)
        enter_default_heatmap_mode()
        # sleep(3)

    @timeit
    def test_F_add_all_kind_of_emojis_same_line_with_filters(self):
        """
        :return: void
        Test is adding comments with all the possible emojis to FIRST_LINE
        Then it filter the comment based on all the emojis (one by one)
        """
        add_subset_of_the_emojis(
            NUM_OF_EMOJIS, FIRST_LINE, FIRST_LINE + 1)
        enter_emoji_heatmap_mode()
        # sleep(3)
        go_throw_all_emoji_filters_one_by_one(0)
        enter_default_heatmap_mode()
        # sleep(3)

    @timeit
    def test_G_add_comment_with_multiple_emojis(self):
        """
        :return: void
        Test is adding all comment with subset of the emojis from size 0 to |all emojis| (multiple emojis in the same
        comment)
        """
        for i in range(1, len(emojis_prefixes) + 1):
            add_comment_with_emojis("//*[@id='viewer']/div[1]/div[2]/span[" + str(FIRST_LINE + i) + "]",
                                    "This is a comment with " + str(i) + " emojis", emojis_prefix=emojis_prefixes[0:i])
        # sleep(3)

    # @timeit
    # def test_H_add_comment_without_emojis(self):
    #     """
    #     :return: void
    #     basic test which adds comment without emojis
    #     """
    #     enter_default_heatmap_mode()
    #     add_comment_with_emojis(
    #         "//*[@id='viewer']/div[1]/div[2]/span[82]", "This is a comment without emojis")
    #     # sleep(3)

    # @timeit
    # def test_I_add_comment_go_page_back_and_return(self):
    #     """
    #     :return: void
    #     Test is adding 1 comment, then go page back and page foreword to check that the comment still exists
    #     """
    #     enter_default_heatmap_mode()
    #     add_comment_with_emojis(
    #         "//*[@id='viewer']/div[1]/div[2]/span[77]", "This is a comment without emojis")
    #     driver.back()
    #     driver.find_element(
    #         by="xpath", value="//*[@id='vgt-table']/tbody/tr[1]/td[2]/span/a").click()
    #     # sleep(3)

    # @timeit
    # def test_J_add_3_comments_to_3_different_lines_then_toggle_heatmap_twice(self):
    #     """
    #     :return: void
    #     Test add 3 comments to 3 different lines and the toggle heatmap mode twice
    #     """
    #     enter_default_heatmap_mode()
    #     add_x_comments_to_y_different_lines(3, 3)
    #     hide_and_show_heatmap()

    # @timeit
    # def test_K_add_3_comments_to_10_different_lines(self):
    #     """
    #     :return: void
    #     Test add 3 comments to 10 different lines (performance check)
    #     """
    #     add_x_comments_to_y_different_lines(3, 10)
    #     driver.execute_script(
    #         "window.scrollTo(0,document.body.scrollHeight)")

    # @timeit
    # def test_L_add_10_comments_to_10_different_lines_and_scroll_to_bottom(self):
    #     """
    #     :return: void
    #     Test add 10 comments to 10 different lines and then scroll the page to the bottom(performance check)
    #     """
    #     add_x_comments_to_y_different_lines(10, 10)
    #     driver.execute_script(
    #         "window.scrollTo(0,document.body.scrollHeight)")

    # @timeit
    # def test_M_stress_1000_comments_same_line(self):
    #     """
    #     :return: void
    #     Test add 1000 comments to FIRST_LINE (performance check)
    #     """
    #     add_comment_with_emojis(
    #         xpath="//*[@id='viewer']/div[1]/div[2]/span[67]", comment_content="comment")
    #     for i in range(1000):
    #         add_comment_with_emojis(
    #             xpath="//*[@id='viewer']/div[1]/div[2]/span[67]", comment_content="comment", is_first_comment=False)
    #     delete_all_comments()

    def tearDown(self):
        """
        :return: void
        We use tear down function to clean our side effects between tests.
        """
        sleep(5)
        delete_all_comments()

    @classmethod
    def tearDownClass(cls):
        print("\nAll Tests PASS")
        driver.close()


def auto_generate_comments_from_xlsx(path):
    """
    :param path: path to the xlsx file which contains the comments we want to add to the doc.
    :return: void
    """
    print(path)
    df = pd.read_excel(path)
    print(df)
    for i in range(len(df)):
        # print(df["text"][i])
        print(df["EMOJI_PREFIX"][i])
        add_comment_with_emojis("//*[@id='viewer']/div[1]/div[2]/span[" + str(SECOND_PARA_FIRST_LINE + i) + "]",
                                df["text"][i], emojis_prefix=[df["EMOJI_PREFIX"][i]])


if __name__ == '__main__':
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    actionChains = ActionChains(driver)
    setup()
    delete_all_comments()
    # auto_generate_comments_from_xlsx("/Users/nivdan/Downloads/student-ce-data.xlsx")

    unittest.main()
