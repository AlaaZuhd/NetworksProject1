from socket import *
import re
import pandas as pd


def mapping(subURL):
    contentType = ""
    # if subURL = "someImageName.png" then contentType = "image/png"
    # else if subURL = "someImageName.jpg then contentType = "image/jpg"
    # else contentType = "text/html"
    print("we are in mapping")
    extention = subURL.split(".")
    if(len(extention) > 1):
        if(extention[1] == "png"):
            contentType = "image/png"
        elif (extention[1] == "jpg"):
            contentType = "image/jpg"
        else:
            contentType = "text/html"

    else:
        contentType = "text/html"
    # working with the name fot he file
    if(subURL == ""):
        subURL = "index.html"

    return [contentType, subURL.strip()]

def getDataOfSmartPhonesFileSorted(fileName):
    df = pd.read_csv("smartPhones.csv")
   # sorted_df
    if (fileName == "SortPrice"):
        sorted_df = df.sort_values(by=["Price"], ascending=True)
    elif (fileName == "SortName"):
        sorted_df = df.sort_values(by=["Name"], ascending=True)
    #sorted_df = sorted_df.astype('string')
    return sorted_df

def main():
    serverPort = 9000
    serverSocket = socket(AF_INET, SOCK_STREAM) # TCP server
    serverSocket.bind(('', serverPort)) # get socket
    serverSocket.listen(1) # server is always listening
    print('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept() # accepting a request
        sentence = connectionSocket.recv(1024).decode() # the request
        # the sentence is the request, we can get the url after the first / in the request
        token = sentence.split("/") # we will get the subURL with a space then HTTP word
        print(token[1])
        subURL = token[1].split(" ") # this is use to get the subURL without
        print("H")
        print(subURL[0]) # if subURL = " " then it's for the localhost:9000/
        print("H")
        contentType, fileName = mapping(subURL[0])
        #contentType = "image/jpg"
        #fileName = "https://png.pngtree.com/element_our/20200610/ourmid/pngtree-social-network-image_2244402.jpg"
        #
        print("We are printing the connectionsocket")
        print(connectionSocket)
        print("We are printing the addr")
        print(addr)
        print("We are printing the sentence")
        print(sentence)
        print("\n\n")
        ip = addr[0] # ip of the client
        port = addr[1] # port of the client
        print("file name is : " + fileName)
        try:
                # check if the request is sortName or sortPrice in this case, we need to sort the file acording to the name or the price then display it
                if(fileName == "SortName" or fileName == "SortPrice"):
                    fileContent = getDataOfSmartPhonesFileSorted(fileName)
                    print(fileContent)
                    fileContent = bytes(fileContent.to_string(), "UTF-8")
                    contentType = "text/plain"
                else:
                    with open(fileName, "rb") as f:
                        fileContent = f.read()

                connectionSocket.send(bytes("HTTP/1.1 200 OK\r\n", "UTF-8"))
                connectionSocket.send(bytes("Content-Type:" + contentType + "\r\n", "UTF-8"))
                connectionSocket.send(bytes("\r\n", "UTF-8"))
                connectionSocket.send(fileContent)
                connectionSocket.close()
        except IOError:
                print ("not found")
                f = open("Error.html", "rb")
                fileContent = f.read()
                connectionSocket.send(bytes("HTTP/1.1 200 OK\r\n", "UTF-8"))
                connectionSocket.send(bytes("Content-Type: text/html\r\n", "UTF-8"))
                connectionSocket.send(bytes("\r\n", "UTF-8"))
                connectionSocket.send(fileContent)
                connectionSocket.close()


main()