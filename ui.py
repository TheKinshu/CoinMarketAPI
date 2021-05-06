from tkinter import *
from PIL import ImageTk, Image
import os, requests
from io import BytesIO
from CoinMarketAPI import CoinMarketAPI
import time, pyperclip

# Font
LABELFONT = ("Serif", 15, "bold")

# Defining class UI
class UI():

    def __init__(self) -> None:

        self.website = ""

        # Creating windows
        self.window = Tk()
        self.window.title("Crypto Information Finder")
        self.displayArea = PhotoImage(file="./images/background.png")
        self.graph = PhotoImage(file="./images/graph.png")

        self.canvas = Canvas(width=450, height=394, highlightthickness=0, bg="#3587F5")
        self.canvasBackground = self.canvas.create_image(450/2, 197, image=self.displayArea)

        self.titleLabel = self.canvas.create_text(10, 10, text="Crypto Information Finder", fill="#fff", anchor="nw", font=LABELFONT)

        self.nameLabel = self.canvas.create_text(50, 60, text="Name:")
        self.cryptoName = self.canvas.create_text(33, 70, text="None", width=500,anchor='nw')

        self.priceLabel = self.canvas.create_text(200, 60, text="Current Price:")
        self.priceText = self.canvas.create_text(163, 70, text="$0", anchor="nw")

        self.percentLabel = self.canvas.create_text(360,60, text="Percent Change 24hrs:")
        self.percentText = self.canvas.create_text(360,70, text="0%", anchor="n")

        self.capLabel = self.canvas.create_text(65, 95, text="Market Cap:")
        self.marketCap = self.canvas.create_text(33, 105, text="0", width=500,anchor='nw')

        self.lastUpdatedLabel = self.canvas.create_text(200, 95, text="Last Updated:")
        self.lastUpdatedText = self.canvas.create_text(164, 105, text="" , anchor="nw")

        self.graphDisplay = self.canvas.create_image(450/2, 150, image=self.graph)

        self.searchLabel = self.canvas.create_text(20, 280, text="Enter a crypto name:",anchor="nw", fill="#fff")

        self.searchEntry = Entry(width=50)
        self.canvasSearch = self.canvas.create_window(20,300, anchor="nw", window=self.searchEntry)

        self.websiteButton = Button(text="Click to copy Website", width=50, command=self.getWebsite)
        self.canvasButton = self.canvas.create_window(45, 200, anchor="nw", window=self.websiteButton)
        
        self.searchButton = Button(text="Search", width=10, command=self.search)
        self.canvasButton = self.canvas.create_window(350, 295, anchor="nw", window=self.searchButton)

        self.canvas.grid(column=0, row=0, columnspan=2)


        
        self.window.mainloop()
    
    # Search function that calls the search function in the API and sends the name of the crypto -
    # to be search from the input field
    def search(self):
        name = self.searchEntry.get()
        if not name == "":
            api = CoinMarketAPI()
            api.search(str(name).lower())
            self.displayInfo(api.crypto_info)
            self.searchEntry.delete(0, "end")
        else:
            # Pop-up to tell user to enter something
            print("empty")

    # Displays the information that was return from the API class
    def displayInfo(self, crypto_info):
        percentage = round(crypto_info['percent_change_24h'],2)
        self.getGraph(crypto_info['seven_day_graph'])
        self.canvas.itemconfig(self.cryptoName, text=crypto_info['name'])
        self.canvas.itemconfig(self.priceText, text= "%.8f" % crypto_info['price'])
        self.canvas.itemconfig(self.percentText, text="{}%".format(percentage))
        self.canvas.itemconfig(self.marketCap, text=crypto_info['market_cap'])
        self.canvas.itemconfig(self.lastUpdatedText, text=crypto_info['last_updated'][:19])
        self.website = crypto_info['website'][0]
    
    # Give the user the website of the crypto currency
    def getWebsite(self):
        if not self.website == "":
            pyperclip.copy(self.website)

    # Construct a Photo Image base on the url that was recieved from the data
    def getGraph(self, url):
        self.img_url = url
        self.response = requests.get(self.img_url)
        self.response.raise_for_status()
        self.img_data = self.response.content
        self.img = ImageTk.PhotoImage(Image.open(BytesIO(self.img_data)))
        time.sleep(0.1)
        self.graph_it(self.img)

    # Display the graph of the past 7 days of growth
    def graph_it(self, img):
        self.canvas.itemconfig(self.graphDisplay, image=img)