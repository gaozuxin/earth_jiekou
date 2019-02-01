def plu_data(barcodeString):
    a, b, c, d = 0,0,0,0
    barcodeString = barcodeString[0: 17]
    charArray = list(barcodeString)
    # // Step 1: Sum all of the digits in the odd positions together.
    # for (i = barcodeString.length() - 1; i >= 0; i = i - 2):
    #     if (charArray[i] > '9' || charArray[i] < '0') {
    #         return (char) 0;
    #     }
    #     a = a + charArray[i] - 48;
    # }
    i = len(barcodeString) - 1
    while (i >= 0):
        if (charArray[i] > '9' or charArray[i] < '0'):
            return 0

        a = a +ord(charArray[i]) - 48
        i = i - 2
    # // Step 2: Mutliply the sum from Step 1 by 3.
    a = a * 3
    # // Step 3: Sum all of the digits in the even positions together.
    # for (i = barcodeString.length() - 2; i >= 0; i = i - 2) {
    #     if (charArray[i] > '9' || charArray[i] < '0') {
    #         return (char) 0;
    #     }
    #     b = b + charArray[i] - 48;
    # }
    index = len(barcodeString) - 2
    while (index >= 0):
        if (charArray[index] > '9' or charArray[index] < '0'):
            return 0
        b = b + ord(charArray[index]) - 48
        index = index - 2

    # // Step 4: Sum together the results from Step 2 and Step 3.
    c = a + b
    # // Step 5: Subtract the sum from the next highest multiple of 10.
    d = c % 10
    if (d != 0):
        d = 10 - d
    return(chr(d + 48))  # 返回校验码


if __name__ == '__main__':
    skuid =17923
    weight = '00500'
    barcodeString = "99%s%s12345"%(skuid,weight)
    dt = plu_data(barcodeString)
    print(barcodeString+dt)
    barcodeString1 = "99%s0258012345"%skuid
    dt = plu_data(barcodeString1)
    print(barcodeString1+dt)
    # barcodeString2 = "99%s0085612345"%skuid
    # dt = plu_data(barcodeString2)
    # print(barcodeString2+dt)



