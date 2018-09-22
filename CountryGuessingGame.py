#==============================================================================
# Title: County Guessing Game
# Author: Ryan Slater
# Date: 7/28/2017
# Purpose: Game where player guesses as many countries as they can
#==============================================================================

def CountryGuessingGame():
    countryList = ['afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bhutan', 'bolivia', 'bosnia and herzegovina', 'botswana', 'brazil', 'brunei', 'bulgaria', 'burkina faso', 'burma', 'burundi', 'cambodia', 'cameroon', 'canada', 'cabo verde', 'central africian republic', 'chad', 'chile', 'china', 'colombia', 'comoros', 'democratic republic of the congo', 'republic of the congo', 'costa rica', 'cote d\'ivoire', 'croatia', 'cuba', 'curacao', 'cyprus', 'czechia', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'fiji', 'finland', 'france', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'greece', 'grenada', 'guatemala', 'guinea', 'guinea-bissau', 'huyana', 'haiti', 'holy see', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'north korea', 'south korea', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macau', 'macedonia', 'madagascar', 'malawi', 'malasia', 'maldives', 'mali', 'malta', 'marshall islands', 'mauritania', 'mauritius', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'morocco', 'mozambique', 'namibia', 'nauru', 'nepal', 'netherlands', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'norway', 'oman', 'pakistan', 'palau', 'palestinian territories', 'panama', 'papau new guinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal', 'qatar', 'romania', 'russia', 'rwanda', 'saint kitts and nevis', 'saint lucia', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'spain', 'sri lanka', 'sudan', 'south sudan', 'suriname', 'swaziland', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'timor-leste', 'togo', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states of america', 'uruguay', 'uzbekistan', 'vanuatu', 'venezuela', 'vietnam', 'yemen', 'zambia', 'zimbabwe']

    correctGuesses  = []
    turn = 1
    userQuits = False
    while turn <= len(countryList) and userQuits == False:
        print(100*'\n')
        for i in range(len(correctGuesses)):
            if i == len(correctGuesses)-1:
                print(correctGuesses[i])
            else:
                print(correctGuesses[i] + ', ', end='')
        print(str(len(correctGuesses)) + '/' + str(len(countryList)))
        print('Guess a country or enter "quit" to give up:')
        guess = input()
        if guess.lower() == 'quit':
            userQuits == True
            break
        if guess.lower() in countryList:
            correctGuesses.append(guess)
            print('That\'s right!')
        else:
            print('That\'s not a country!')

    if len(correctGuesses) == len(countryList):
        print('Congratulations, you guessed all ' + str(len(countryList)) + ' countries correctly!')
    else:
        print('You guessed ' + str(len(correctGuesses)) + '/' + str(len(countryList)) + ' countries correctly!')

if __name__ == '__main__':
    CountryGuessingGame()