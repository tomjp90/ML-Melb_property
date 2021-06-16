import numpy as np

def rand_header():
      #----------------------------- RANDOMLY CREATE A 'USER' -------------------------------------------
      rand = np.random.randint(6)
      headers_list = [{'User-Agent': 'Chrome/6.1 (Mac; Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102',},
                        {'User-Agent': 'Opera/8.4 (Macintosh; Mac OS X 10_11_6) Kit/538.36 (KHTML, like Gecko) Opera/50.1.3.54'},
                        {'User-Agent': 'Chrome/5.111 (Win; Win OS 10.3) WebKit/537.36 (HTML) Chrome/50.0.21.12'},
                        {'User-Agent': 'Chrome/5.221 (Win; Win OS 10.3) WebKit/537.36 (KHTML, like Gecko) Chrome/5012.0.21.12'},
                        {'User-Agent': 'Chrome/5.111 (Win; Win OS 10.3) WebKit/537.36 (like Gecko) Chrome/53.0.21.12'},
                        {'User-Agent': 'Chrome/5.111 (Mac; Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102'}
                        ]      
                              
      header = headers_list[rand]

      return header
