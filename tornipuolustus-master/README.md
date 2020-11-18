# Tornipuolustus

Yksinkertainen tornipuolustuspeli, toteutettu Pythonilla + PyQt5:lla. 

# Kuinka pelata

Peliä ohjataan hiirellä. Valinnat tehdään hiiren painikkeilla. Painamalla R näppäintä pelaaja voi aloittaa pelin alusta halutessaan.

Peli alkaa tyhjällä kentällä ja vihollisten joukkoja alkaa ilmestymään välittömästi. Pelaajan tehtävänä on pysäyttää joukkojen eteneminen rakentamalla puolustustorneja jotka ampuvat hyökkääjiä.
Torneja pystyy rakentamaan klikkaamalla ensin Tower - nappulaa alhaalla UI:ssa, ja tämän jälkeen klikkaamalla haluttua paikkaa kentältä (HUOM. torneja pystyy rakentamaan vain tummanharmaisiin neliöihin).

Pelaajalla on aluksi kultaa vain yhteen torniin. Pelaaja saa lisää kultaa jokaisesta tuhotusta vihollisesta. Lisäksi tuhotuista vihollisista saa pisteitä. Pelaajan kierros loppuu jos yksikin vihollinen pääsee maaliin asti.

Selviä mahdollisimman kauan ja koita rikkoa piste-ennätyksesi!

# Ohjelman käynnistys

Kloonaa tämä repository omalle koneellesi ja aja main.py tiedosto Pythonilla. 

PyQt5 tulee olla asennettuna. Jos olet asentanut PIP:n Pythonin (3.5 tai uudempi) yhteydessä, asennus onnistuu komentoriviltä komennolla: pip install pyqt5.

# Tekijät
Koodaus, suunnittelu: Juuso Pulkkinen