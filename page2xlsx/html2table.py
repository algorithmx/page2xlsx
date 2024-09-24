from bs4 import BeautifulSoup
import pandas as pd

class jiuyangongshe:
    fn = ''
    date = ''

    def __init__(self, date):
        self.date = date
        self.fn = self.date + '.html'
        self.url = 'https://www.jiuyangongshe.com/action/' + self.date
        self.output = self.fn.replace('html','xlsx')

    def section_to_df(self, section):
        #data_v = list(section.attrs.keys())[0]
        first_block = section.find('div', {'class': 'hsh-flex-upDown jc-bline'})
        topic = first_block.find('div', {'class': 'fs18-bold lf'}).text.strip()
        second_block = section.find('div', {'class': 'table-box'})
        if second_block is None:
            return None
        #table_header = second_block.find('div', {'class': 'th-box hsh-flex-both'})
        table_rows = second_block.find('ul', {'class': 'td-box'}).find_all('li', {'class': 'row drvi straight-line'})
        # print('+++++++++++++++++++++++++++++++\nTopic ', topic)
        # print("Number of rows: ", len(table_rows))
        rows = []
        for row in table_rows:
            # print('---------------------------')
            row_content = row.find('div', {'class': 'hsh-flex-both alcenter'})
            stock_name = [cell.text.strip() for cell in  row_content.find_all('div',{'class': 'shrink fs15-bold'})]
            # print(stock_name)
            if len(stock_name)==0:
                # print("1")
                continue
            stock_symbol = [cell.text.strip() for cell in  row_content.find_all('div',{'class': 'shrink fs12-bold-ash force-wrap'})]
            if len(stock_symbol)==0:
                # print("2")
                continue
            stock_price = [cell.text.strip() for cell in  row_content.find_all('div',{'class': 'shrink number'})]
            if len(stock_price)==0:
                # print("3")
                continue
            stock_pct = [cell.text.strip() for cell in  row_content.find_all('div',{'class': 'shrink cred'})]
            if len(stock_pct)==0:
                # print("4")
                continue
            stock_time = [cell.text.strip() for cell in  row_content.find_all('div',{'class': 'shrink fs15'})]
            if len(stock_time)==0:
                # print("5")
                continue
            stock_info = [cell.text.strip() for cell in  row_content.find_all('pre',{'class': 'pre'})]
            if len(stock_info)==0:
                # print("6")
                continue
            rows.append({'topic': topic, 'name':stock_name[0], 'symbol':stock_symbol[0], 'price':stock_price[0], 'pct':stock_pct[0], 'time':stock_time[0], 'info':stock_info[0]})
        # print('+++++++++++++++++++++++++++++++\n')
        return pd.DataFrame(rows)

    def transform_dataframe(self, df):
        # Split the 'info' column on the first newline character
        df['info0'] = df['info'].apply(lambda x: x.split('\n')[0] if '\n' in x else x)
        df['info1'] = df['info'].apply(lambda x: x.split('\n', 1)[1] if '\n' in x else '')
        # Drop the original 'info' column
        df = df.drop(columns=['info'])
        return df

    def html2table(self) -> None:
        with open(self.fn,'r') as f:
            html_source = f.read()
        soup = BeautifulSoup(html_source, 'html.parser')
        section_block = soup.find_all('ul', {'class': 'module-box jc0'})
        sections = section_block[0].find_all('li', {'class': 'module'})
        df_list = [self.section_to_df(s) for s in sections[1:]]
        df_all = pd.concat([df for df in df_list if df is not None])
        df_all_1 = self.transform_dataframe(df_all)
        print("saving page as: ", self.output)
        df_all_1.to_excel(self.output, index=False)

    # write a function to lauch the browser, load a given page and save the page as local html.
    def save_page(self) -> None:
        import os
        if os.path.isfile(self.fn):
            print('file exists: ', self.fn)
            return
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from time import sleep
        # configure the webdriver to use Chrome from path .env/bin/chromedriver
        driver = webdriver.Chrome()
        # open the page url in the browser
        print('open page: ', self.url)
        driver.get(self.url)
        driver.implicitly_wait(1)
        sleep(1)
        # click the place for the element <div data-v-15040e9e="">全部异动解析</div> using find_element with By.XPATH
        try:
            driver.find_element(By.XPATH, '//div[@class="yd-tabs_item is-top" and @data-v-15040e9e]/div[@data-v-15040e9e and text()="全部异动解析"]').click()
            sleep(10)
        except Exception as e:
            print(e)
        print('page loaded: ', driver.title)
        with open(self.fn, "w") as f:
            f.write(driver.page_source)
        driver.quit()
