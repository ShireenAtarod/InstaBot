# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import csv
import urllib.request
import time
import random
import re
import authentication as auth


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_URL = "https://www.instagram.com/"

        self.driver = webdriver.Chrome('chromedriver.exe')
        time.sleep(2)
        self.login()

    def login(self):
        self.driver.get('{}accounts/login/'.format(self.base_URL))

        time.sleep(2)
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        
        time.sleep(5)
        save = self.find_buttons("button", "Not Now")
        if save:
            save[0].click()
        notif = self.driver.find_element_by_xpath("//button[contains(text(), 'Turn On')]")
        if notif:
            notif.click()

    def nav_to_user(self, user):
        self.driver.get('{}{}/'.format(self.base_URL, user))

    def find_buttons(self, button, button_text):
        buttons = self.driver.find_elements_by_xpath("//{}[contains(text(), '{}')]".format(button, button_text))
        return buttons
    
    def find_hashtag(self, tag):
        self.driver.get('{}explore/tags/{}/'.format(self.base_URL, tag))

    def infinite_scroll(self):
        SCROLL_PAUSE_TIME = 1

        self.last_height = self.driver.execute_script("return document.body.scrollHeight")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

        time.sleep(SCROLL_PAUSE_TIME)

        self.new_height = self.driver.execute_script("return document.body.scrollHeight/2")


        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False


#############  Follow / Unfollow  ############
 
    def follow_unfollow_user(self, user, action):
        buttons = self.find_buttons("button", action)
        if buttons:
            buttons[0].click()
            print("followed")

    def unfollow_user_following(self, user, n):
        self.nav_user(user)
        time.sleep(4)
        self.driver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(4)
        finished = False
        self.scroll_height = self.driver.execute_script("return document.getElementsByClassName('pbNvD')[0].scrollHeight")
        self.new_height = 0
        self.total_height = self.driver.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight")
        i = 0
        while not finished and i < n:
            buttons = self.driver.find_elements_by_xpath("//button[contains(text(), 'Following')]")
            print(len(buttons))
            if buttons:
                buttons.pop()
                for button in buttons:
                    if i < n:
                        i = i + 1 
                        button.click()
                        time.sleep(1)
                        self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
                        time.sleep(1)
                    else:
                        break

            self.new_height += self.scroll_height

            self.driver.execute_script("document.getElementsByClassName('isgrP')[0].scrollTop = {};".format(self.scroll_height))

            time.sleep(1)

            finished = False
            if self.new_height >= self.total_height:
                finished = True

    def follow_user_by_hashtag(self, tag, n):
        self.find_hashtag(tag)
        time.sleep(10)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a').click()
        
        time.sleep(10)
        for i in range(n):
            time.sleep(random.randint(1, 5))
            self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click
            time.sleep(random.randint(5, 20))
            buttons = self.driver.find_elements_by_xpath("//svg[@aria-label='Like']")
            for button in buttons:
                button.click()
            time.sleep(random.randint(3,10))
            self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a').click()
        
        self.find_buttons('button', 'Close').click()

    def followe_user_from_list(self, listname):
        #open the list of users that should not have follow
        with open(f'{auth.username}blacklist.txt') as csvfile:
            notfollow = csvfile.readlines()
        
        #open the list of users that is going to follow
        with open(f'{listname}.csv') as csvfile:
            Users = list(csv.reader(csvfile))[0]           
        
        #list of user we are following but not saved yet
        already_followed = list()
        #number of users we want to followe
        limit = len(Users)
        x = 0
        print(limit)
        
        if len(Users) < limit:
            limit = len(Users)

        for i in range(100, limit):
            if x < 40:
                user = Users[i]
                if user not in notfollow:
                    self.nav_to_user(user)
                    time.sleep(random.randint(7, 20))
                    is_available = self.driver.find_elements_by_xpath("/html/body/div/div[1]/div/div/h2")
                    if not is_available:
                        is_private = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2')
                        if is_private:
                            pass
                        else:
                            has_story = self.driver.find_elements_by_class_name('h5uC0')
                            if has_story:
                                #print("has story")
                                self.watch_user_story()
                            has_post = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text
                            has_post = has_post.replace(",", "")
                            post_no = int(has_post)
                            #print(post_no)

                            n = 0
                            if post_no > 2:
                                n = 3
                            elif post_no > 0:
                                n = post_no                                      
                            
                            if n > 0:
                                try:
                                    self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a').click()
                                except:
                                    self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a').click()
                                for i in range(n):
                                    time.sleep(random.randint(1, 10))
                                    like = self.driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
                                    #like = self.driver.find_elements_by_xpath("//span[@aria-label='Like'][@class='glyphsSpriteHeart__outline__24__grey_9 u-__7']")
                                    if like:
                                        like[0].click()
                                    time.sleep(random.randint(1, 10))
                                    next = self.driver.find_elements_by_class_name('coreSpriteRightPaginationArrow')
                                    if next:
                                        next[0].click()
                                self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()
                                x = x + 1
                                print(x)
                                already_followed.append(user)

                            else:
                                pass

        print(len(already_followed), " followed")
        with open(f'alreadyfollowed_{auth.username}.csv', 'a') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(already_followed)

        print(len(Users), " users remain")

    def unfollow_requested(self, filename, max):
        counter = 0
        allready = list()
        with open(filename) as users:
            for user in users:
                print(counter, user)
                if user != "\n" and counter < max:
                    self.nav_to_user(user.strip("\n"))
                    time.sleep(random.randint(15, 40))
                    button = self.find_buttons("button", "Requested")
                    if button:
                        button[0].click()
                    time.sleep(random.randint(10, 30))
                    button = self.find_buttons("button", "Unfollow")
                    if button:
                        button[0].click()
                    time.sleep(10)
                    counter = counter+1
                    allready.append(user)

        with open(f"{auth.username}blacklist.txt", 'a') as outfile:
            outfile.writelines(allready)
                    

#############  Like  ############

    def like_feed(self, n):
        print(n)
        c = 0
        trying = 0
        while c < n and trying < 10:
            LikeButtons = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/section/div[1]/div[2]/div/article[2]/div[3]/section[1]/span[1]/button')
            
            if len(LikeButtons) > 0:
                print("number of available button", len(LikeButtons))
                for button in LikeButtons: 
                    if c < n:
                        try:
                            button.click()
                            time.sleep(random.randint(10, 60))
                            c = c + 1
                            print("liked")
                        except:
                            print("error")
                        time.sleep(random.randint(5, 10))
            else:
                scroll = self.driver.find_elements_by_class_name("Id0Rh")
                trying = trying + 1
                if scroll:
                    self.driver.execute_script("arguments[0].scrollIntoView();", scroll[0])
                    print("scroll")
                time.sleep(random.randint(3, 7))


        print(c," posts liked")

    def hashtag_top_post(self, tag, comments):
        self.find_hashtag(tag)
        time.sleep(random.randint(10, 25))
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a').click()
        for i in range(9):
            time.sleep(random.randint(25,45))
            try:
                self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()

                time.sleep(random.randint(7, 13))
                comment = self.driver.find_elements_by_xpath('//form[@class="X7cDz"]/*[name()="textarea"][@aria-label="Add a comment…"]')
                if comment:
                    comment[0].click()
                    time.sleep(1)
                    self.driver.find_element_by_xpath('//form[@class="X7cDz"]/*[name()="textarea"][@aria-label="Add a comment…"]').send_keys(comments[random.randint(0,len(comments)-1)])
                    time.sleep(random.randint(15, 60))
                    self.find_buttons("button", "Post")[0].click()
                time.sleep(random.randint(10, 35))
            except:
                time.sleep(1)
           
            self.find_buttons("a", "Next")[0].click()
            
    def reply_comment_with_word(self, username, word):
        self.nav_to_user(username)
        post = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a')
        if post:
            post[0].click()
            time.sleep(5)
        for p in range(5):
            time.sleep(random.randint(10, 15))
            plus = self.driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/li/div/button')
            while plus:
                plus[0].click()
                time.sleep(random.randint(5, 23))
                plus = self.driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/li/div/button')
            
            comments = self.driver.find_elements_by_class_name('Mr508')
            if len(comments) > 49:
                print(len(comments))
                keyword = re.compile('(.*?){}(.*?)'.format(word))
                for i in range(len(comments)):
                    comment = self.driver.find_elements_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/ul[{}]/div/li/div/div[1]/div[2]/span'.format(i))
                    if comment:
                        if keyword.search(comment[0].text):
                            reply = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div[1]/ul/ul[{}]/div/li/div/div[1]/div[2]/div/div/button'.format(i))
                            if reply:
                                reply[0].click()
                                self.driver.find_element_by_xpath('//form[@class="Ypffh"]/*[name()="textarea"][@aria-label="Add a comment…"]').send_keys('خوشحال میشیم از مجموعه شال و روسری های ما دید کنید. الان تو تخفیف هم هستیم.')
                                time.sleep(random.randint(15, 60))
                                self.find_buttons("button", "Post")[0].click()
                                print('reply to comment')
                                time.sleep(random.randint(10, 25))
            try:
                self.find_buttons("a", "Next")[0].click()
            except:
                time.sleep(1)            

#############  Watch Story  ############
 
    def reply_story(self):
        reply = self.driver.find_elements_by_class_name("Xuckn")
        if reply:
            reply[0].click()
            time.sleep(2)
            reply[0].send_keys("👍👍👍")

    def watch_following_stories(self):
        self.driver.get(self.base_URL)
        time.sleep(5)
        notif = self.driver.find_elements_by_xpath("//button[contains(text(), 'Turn On')]")
        if notif:
            notif[0].click()
        time.sleep(2)
        story = self.driver.find_elements_by_class_name("_1rQDQ ")
        if story:
            story[0].click()
        else:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[1]/div[1]/div/div/div/div/ul/li[3]/div/button').click()
            
        time.sleep(1)
         
    def watch_tag_stories(self, tag):
        self.find_hashtag(tag)
        time.sleep(random.randint(15, 60))
        story = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/header/div[1]')
        if story:
            story.click()
            time.sleep(4)
            counter = self.driver.find_elements_by_class_name("_7zQEa")
            for i in range(len(counter)):
                if 1 == 1:
                    print("reply")
                    self.reply_story()
                video = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/div/div/section/div[2]/div[1]/div/div/video')
                time.sleep(5)
                if video:
                    nextstory = self.driver.find_elements_by_class_name("ow3u_")
                    if nextstory:
                        nextstory[0].click()

    def watch_user_story(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/div/div').click()
        time.sleep(4)
        next = self.driver.find_elements_by_class_name('coreSpriteRightChevron')
        while next:
            next[0].click()
            time.sleep(4)
            next = self.driver.find_elements_by_class_name('coreSpriteRightChevron')

#############  Download  ############
    def download_user_images(self, user): 
        self.nav_user(user)
        time.sleep(2)

        img_srcs = []
        finished = False
        while not finished:
            finished = self.infinite_scroll() # scroll down
            img_srcs.extend([img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')]) # scrape srcs

        img_srcs = list(set(img_srcs)) # clean up duplicates

        for idx, src in enumerate(img_srcs):
            self.download_image(src, idx, user)

    def download_image(self, src, image_filename, folder):
        folder_path = './{}'.format(folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename = 'image_{}.jpg'.format(image_filename)
        urllib.request.urlretrieve(src, '{}/{}'.format(folder, img_filename))

    def user_followers_list(self, username):
        self.nav_to_user(username)
        time.sleep(2)
        followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text
        followers = followers.replace(",", "")
        print(followers)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        time.sleep(5)
        names = list()

        notfinish = self.driver.find_elements_by_class_name('oMwYe')
        tryno = 0
        while len(notfinish) > 0 or tryno < 5:
            if not len(notfinish) > 0:
                time.sleep(2)
                tryno = tryno + 1
            else:
                tryno = 0
                self.driver.execute_script("arguments[0].scrollIntoView();", notfinish[0])
                time.sleep(2)
            notfinish = self.driver.find_elements_by_class_name('oMwYe')
        
        Users = list()
        names = self.driver.find_elements_by_class_name('FPmhX')
        print(len(names))
        for name in names:
            Users.append(name.text)

        with open('{}.csv'.format(username), 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(Users)

    def user_following_list(self, username):
        self.nav_to_user(username)
        time.sleep(2)
        followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text
        followers = followers.replace(",", "")
        print(followers)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(5)
        names = list()

        notfinish = self.driver.find_elements_by_class_name('oMwYe')
        tryno = 0
        while len(notfinish) > 0 or tryno < 5:
            if not len(notfinish) > 0:
                tryno = tryno + 1
                time.sleep(2)
            else:
                tryno = 0
                self.driver.execute_script("arguments[0].scrollIntoView();", notfinish[0])
                time.sleep(2)
            notfinish = self.driver.find_elements_by_class_name('oMwYe')
        
        Users = list()
        names = self.driver.find_elements_by_class_name('FPmhX')
        print(len(names))
        for name in names:
            Users.append(name.text)
            if (len(Users) % 100) == 0:
                print(len(Users))
        print(len(Users))
        try:
            with open('{}.csv'.format(username)) as csvfile:
                mylist = list(csv.reader(csvfile))[0] 
            mylist.extend(Users)
            Users = list()
            Users = mylist
            print(len(Users))
        except:
            print("there wasn't another list")
        with open('{}.csv'.format(username), 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(Users)

    def finish(self):
       self.driver.close()



############ Others #############

    def check_numbers(self, numbers):
        Users = list()
        self.driver.get('{}accounts/login/'.format(self.base_URL))
        time.sleep(2)
        for number in numbers:
            self.driver.find_element_by_name('username').send_keys(number)
            self.driver.find_element_by_name('password').send_keys("123456")
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
            time.sleep(10)
            error = self.driver.find_elements_by_id('slfErrorAlert').text
            if error == 'Sorry, your password was incorrect. Please double-check your password.':
                Users.append(number)


if __name__ == "__main__":   
    igBot = InstagramBot(auth.username, auth.password)

    time.sleep(1)

    # Sample task: like 9 top posts of the specifed hashtags and leave a random comment.
    tags=['کتاب_روانشناسی', 'خرید_کتاب','هاروکی_موراکامی', 'گابریل_گارسیا_مارکز', 'اسکات_فیتز_جرالد']
    comments = ['حال و هوای خودتو کتابخونه‌تو با یه تخفیف حسابی و کلی کتاب جدید عوض کن. دایرکت بده تا لیست تخفیف‌ها رو برات بفرستم 😉', 'می‌دونستی مجموعه‌های کتاب‌های یک نویسنده تو انتشارات نوای مکتوب تخفیف دائمی و ارسال رایگان داره؟', 'دو تا پست آخرمون رو چک کن و کتاب بعدی‌تو از ما بخر ']

    for i in range(len(tags)):
        time.sleep(random.randint(30, 180))
        igBot.hashtag_top_post(tags[i], comments)
    
