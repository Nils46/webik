![Imgur](https://i.imgur.com/MortyMy.png)


Kjeld Roos, Nils Böhne & Boudewijn Welkzijn

Helios is een photo-sharing website, waar de foto centraal staat.


Productvideo
--------


Screenshots
--------


![Imgur](https://i.imgur.com/AkbnywI.png)


Features
--------


* Inloggen

* Uitloggen

* Registreren

* Username, password en biography veranderen

* Gebruikers kunnen een eigen profiel aanmaken

     * Profielfoto uploaden
     
     * GIF zoeken
     
     * Biografie schrijven

* Gebruikers kunnen foto's uploaden in categorieën

* Gebruikers kunnen elkaar volgen/ontvolgen

* Ranglijst met de meest gelikete gebruikers en foto

* Eigen profiel en die van anderen bekijken
     
     * Recente foto's bekijken en downloaden

* Wachtwoorden worden gehasht

* Wachtwoord bij login weergeven


Wegwijs door de repository
--------------------------


*  In /static staat alle stijl, foto's en JavaScript files

      * In /static/GIPHY staan alle profielfoto's

      * In /static/Hotels, /static/Yachts, /static/Cars en /static/Watches staan alle foto's van de desbetreffende categorie

      * In /static/JS zitten de JavaScript files

      * In static/styles.css staat de opmaak van de website
      
* In /templates zitten de .HTML files

     * In /templates/layout.html staat de code van de layout
      
* In /helpers.py staan alle functies die regelmatig worden gebruikt in application.py

* In /application.py wordt de application geïnitialiseerd met alle routing-processen


Taakverdeling
------------------


Boudewijn is voor een groot deel verantwoordelijk voor de GIPHY functie op Helios. Hij heeft hiervoor de achterliggende JavaScript code weten te realiseren. Daarnaast heeft Boudewijn ervoor gezorgd dat zowel de Python als HTML-code er verzorgd uit ziet.

Kjeld heeft zich voornamelijk bezig gehouden met de achterliggende functies van Helios. Hij heeft zo een grote bijdrage geleverd aan de grinder functie, het ranking systeem maar ook aan het uploaden van foto's naar de database. Naast deze functies is Kjeld ook deels verantwoordelijk voor de database in zijn geheel. Voorderest heeft hij kleinere functies zoals het  volgen van gebruikres mogelijk gemaakt.

Nils heeft voornamelijk aan de stijl van Helios gewerkt. Daarnaast heeft hij op het begin het Flask framework van de website klaar gelegd. Het gehele profiel is voor een aanzienlijk deel gemaakt door Nils. Ook heeft hij gezorgd dat het mogelijk is dat gebruikers hun profiel kunnen aanpassen. Voorderest heeft Nils samen met Kjeld de database structuur gebouwd, en geholpen aan functies van zowel Boudewijn als Kjeld.
