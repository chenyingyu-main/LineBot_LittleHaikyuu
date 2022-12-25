from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import string


def get_youtube_video_links(keyword, number):
    # keyword = 'volleyballworld'
    driver = webdriver.Chrome()
    driver.set_window_size(1024, 960)
    driver.get('https://www.youtube.com/' + keyword + '/videos')
    driver.execute_script('window.scrollBy(0, 1000)')
    driver.execute_script('window.scrollBy(0, 1000)')

    video_link_container = []
    num = 0
    for link in driver.find_elements(By.ID, 'video-title-link'):
        l = link.get_attribute('href')
        if num < number:
            video_link_container.append(l)
            num += 1


    video_image_container = []
    num = 0
    image_area = driver.find_elements(By.XPATH, '//*[@id="dismissible"]/ytd-thumbnail/a/yt-image/img')
    for link in image_area:
        l = link.get_attribute('src')
        if num < number:
            video_image_container.append(l)
            num += 1

    video_info = []

    video_info.append(video_link_container)
    video_info.append(video_image_container)
    return(video_info)


