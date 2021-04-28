from socket import *
import pandas as pd


# mapping function is used in deducing the content type as illustrated below
def mapping(subURL):
    contentType = ""            # an empty content type initially
    # if subURL = "someImageName.png" then contentType = "image/png"
    # else if subURL = "someImageName.jpg" then contentType = "image/jpg"
    # else contentType = "text/html"
    extention = subURL.split(".")    # getting hte extention from the requested URL
    if(len(extention) > 1):          # the extenion is checked and the type is determined accordingly.
        if(extention[1] == "png"):
            contentType = "image/png"
        elif (extention[1] == "jpg"):
            contentType = "image/jpg"
        else:
            contentType = "text/html"

    # if the extention array is less than one, then either an error or index should be displayed, in both cases the type is text/html
    else:
        contentType = "text/html"
    # working with the name of he file
    if(subURL == ""):
        subURL = "index.html"
    #print(subURL)
    return [contentType, subURL.strip()]   # we return the deduced content type and the required file name.

def getDataOfSmartPhonesFileSorted(fileName):
    df = pd.read_csv("smartPhones.csv")    # getting smart phones data from .csv file
    if (fileName == "SortPrice"):
        sorted_df = df.sort_values(by=["Price"], ascending=True) # sorting a csv file is done easily using data frames.
    elif (fileName == "SortName"):
        sorted_df = df.sort_values(by=["Name"], ascending=True)
    return sorted_df

def main():
    serverPort = 9000                               # the required port number
    serverSocket = socket(AF_INET, SOCK_STREAM)     # TCP server
    serverSocket.bind(('', serverPort))             # get socket
    serverSocket.listen(1)                          # server is always listening
    print('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept() # accepting a request
        sentence = connectionSocket.recv(1024).decode() # the request
        # the sentence is the request, we can get the url after the first / in the request
        token = sentence.split("/")                 # we will get the subURL with a space then HTTP word
      #  print(token[1])
        if len(token)>=2:
            subURL = token[1].split(" ")                # this is used to get the subURL without space
        # print(subURL[0]) # if subURL = " " then it's for the localhost:9000/
        contentType, fileName = mapping(subURL[0])
        # print(connectionSocket)
        # print(addr)
        print(sentence)
        print("----------------------------------------------------------------")
        ip = addr[0] # ip of the client
        port = addr[1] # port of the client
        try:
                # check if the request is sortName or sortPrice in this case, we need to sort the file acording to the name or the price then display it
                if(fileName == "SortName" or fileName == "SortPrice"):
                    fileContent = getDataOfSmartPhonesFileSorted(fileName)
                    # print(fileContent)
                    fileContent = bytes(fileContent.to_string(), "UTF-8")
                    contentType = "text/plain"              # we would be printing the sorted csv file in a text/plain type
                else:
                    #if no errors, and the file name exists, it will be read and saved in fileContent and the response will start based on the deduced content type above.
                    with open(fileName, "rb") as f:
                        fileContent = f.read()
                connectionSocket.send(bytes("HTTP/1.1 200 OK\r\n", "UTF-8"))
                connectionSocket.send(bytes("Content-Type:" + contentType + "\r\n", "UTF-8"))
                connectionSocket.send(bytes("\r\n", "UTF-8"))
                connectionSocket.send(fileContent)
                connectionSocket.close()
        except IOError:
             # in case of errors, a simple html file indicating the error in html type will be sent and the status response will be 404
                fileContent = '<!DOCTYPE html><html><head><title>Error</title> </head><body><h1>Not Found</h1><p id=par> Rawan Yassin &#8594 1182224 &emsp;Alaa Zuhd &#8594 1180865 &emsp;Razan Yassin &#8594 118226 <style >p#par{font-weight: bold;}</style></p>   <p>The IP is &#8594 '+ str(ip)+'</p> <p>The Port number is &#8594 '+str(port)+'</p></body></html>'
                print(fileContent)
                connectionSocket.send(bytes("HTTP/1.1 404 Not Found \r\n", "UTF-8"))
                connectionSocket.send(bytes("Content-Type: text/html\r\n", "UTF-8"))
                connectionSocket.send(bytes("\r\n", "UTF-8"))
                connectionSocket.send(bytes(fileContent, "UTF-8"))
                connectionSocket.close()

# calling the main procedure
main()