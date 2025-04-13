#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".

with open("/Dokumente/100 Days of Code (Python)/Day 24/Input/Letters/starting_letter.txt", mode="r") as letter:
    letter_text = letter.read()
    with open("/Dokumente/100 Days of Code (Python)/Day 24/Input/Names/invited_names.txt", mode="r") as names:
        name_list = names.readlines()
        for name in name_list:
            stripped_name = name.strip()
            letter_new = letter_text.replace("[name]", stripped_name)
            with open(f"/Dokumente/100 Days of Code (Python)/Day 24/Output/ReadyToSend/letter_for_{stripped_name}.text", mode="w") as save:
                save.write(letter_new)

#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp