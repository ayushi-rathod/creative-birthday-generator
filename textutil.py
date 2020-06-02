def breakTextIntoLines(txt):
    lines = txt.split('.')
    f_txt = []
    for line in lines:
        if len(line) > 60:
            # f_txt.append(line[:60])
            for i in range(0, len(line), 60):
                f_txt.append(line[i: i+60])
        else:
            f_txt.append(line)
    # return f_txt, (85 * len(f_txt))
    return '\n'.join(f_txt), (110 * len(f_txt))

# a = "Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro. Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro.\n Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro.Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro.Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro.Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro.Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro.Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro.Prateek UserFriend 10 This is a greeting from a brother. Happy Birthdayy my bro."
# b = breakTextIntoLines(a)
# print(len(b))
# height = 100 * len(b)
# print(b)
