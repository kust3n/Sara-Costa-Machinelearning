### Rapport - Rekommendationsystem för filmer


## 1. Introduktion / Problemställning

Syftet med projektet var att utveckla ett enkelt rekommendationssystem för filmer baserat på dataset från MovieLens.
Rekommendationssystem används idag i många digitala tjänster för att hjälpa användare att hitta relevant innehåll bland stora mängder data.

Målet var att kunna rekommendera fem filmer baserat på en given film användaren skriver in.

Det finns flera metoder att göra detta, men på grund av den stora storleken och glesheten i betygsdatan valdes istället en metod där filmer jämförs utifrån deras genrer. Även användning av tags.csv med någon typ av naturlig språkbehandling och implementera med data från movies.csv hade kunnat ge bra resultat, men valdes bort för att inte göra uppgiften för komplex.

Likhet mellan filmer kan beräknas med cosinusliket:
$$
\text{cosinuslikhet} = \frac{A \cdot B}{||A|| \, ||B||}
$$

Cosinuslikhet används för att mäta hur lika två filmer är baserat på deras genrevektorer.
En K-Nearest Neighbours-modell användes för att hitta de mest liknande filmerna.

---

## 2. Data-analys (EDA) 
*Separat EDA finns som `EDA.ipynb` med visualiseringar.*

Datasetet innehåller totalt **86 537 filmer** och **33 832 162 betyg** från 330 000+ användare. Varje film är kopplad till en eller flera genrer via `movies.csv`. En liten delmängd av filmerna (~7 060 st) saknar genreinformation och är märkta med `(no genres listed)`. Dessa filmer exkluderas från rekommendationssystemet eftersom de inte kan jämföras meningsfullt med övriga filmer.

Analysen visade att vissa genrer är betydligt vanligare än andra. Drama och Komedi dominerar datasetet med 33 681 respektive 22 830 filmer, medan genrer som Film-Noir och IMAX är mycket mer sällsynta.

Rating-datan visade sig vara ojämnt fördelad, majoriteten av filmerna har ganska få betyg jämfört med ett mindre antal filmer som är mycket mer populära och har många betyg. Det innebär att datamängden är gles, vilket kan göra kollaborativa filtreringsmetoder svårare att använda. Detta var en motivation till varför rating-datan inte användes i detta rekommendationssystem.

Taggar från `tags.csv` undersöktes också. Ungefär 60% av filmerna har minst en tagg, vilket innebär ganska bra täckning. Dock är antalet taggar per film generellt lågt, och vissa taggar förekommer i många olika stavningar (ex. "sci-fi", "sci fi", "scifi") men som räknas som separata om ingen pre-processing görs. Sedan är det även en stor andel av taggar som endast används en gång i hela datasetet, vilket inte får någon användning om man vill implementera det i ett rekommendationssystem.

Eftersom genrer finns tillgängliga för majoriteten av filmerna valdes dessa som huvudfeatures i rekommendationsmodellen.

---

## 3. Modell

Filmernas genrer one-hot-enkodas med hjälp av `str.get_dummies(sep="|")` genom pandas. Varje film representeras som en binär vektor med 20 dimensioner (en per genre), där 1 indikerar att filmen tillhör den genren.

**Exempel:**

| Film | Action | Comedy | Drama | Romance | ... |
|---|---|---|---|---|---|
| Toy Story (1995) | 0 | 1 | 0 | 0 | ... |
| Die Hard (1988) | 1 | 0 | 0 | 0 | ... |
| Forrest Gump (1994) | 0 | 0 | 1 | 1 | ... |

En NearestNeighbors-modell från scikit-learn tränas på genre-matrisen med följande parametrar:

- **metric**: `cosine` – mäter likhet via vinkeln mellan genrevektorer
- **algorithm**: `brute` – beräknar distansen till alla filmer och väljer de närmaste; lämpar sig väl för en relativt liten feature-rymd (20 dimensioner)

Vid en sökning returnerar modellen `n + 1` grannar (den första grannen är alltid filmen själv), varefter den ursprungliga filmen filtreras bort och de fem närmaste returneras som rekommendationer.


Systemet är uppdelat i två filer:

- *recommendation_system.py* – ansvarar för dataladdning, feature-engineering och KNN-modellen. Kan importeras som modul eller köras direkt via kommandoraden.
- *app.py* – ett interaktivt Dash-gränssnitt där användaren söker efter en film i en dynamisk dropdown och klickar på en knapp för att få fem rekommendationer. Gör det enklare att hitta filmer jämfört med kommandoraden genom .py filen, som kräver exakt stavning av film plus år. (ger annars error)
Dash-applikationen ansågs mer användarvänligt för att söka runt efter filmer i datasetet.

---

## 4. Resultat

Systemet rekommenderar filmer baserade på genrelikhet. Nedan visas exempel på rekommendationer för ett urval testfilmer:

**Toy Story (1995)** *(Adventure | Animation | Children | Comedy | Fantasy)*

| # | Rekommenderad film |
|---|---|
| 1 | Antz (1998) |
| 2 | Toy Story 2 (1999) |
| 3 | Adventures of Rocky and Bullwinkle, The (2000) |
| 4 | Emperor's New Groove, The (2000) |
| 5 | Monsters, Inc. (2001) |

**The Matrix (1999)** *(Action | Sci-Fi)*

| # | Rekommenderad film |
|---|---|
| 1 | Terminator 2: Judgment Day (1991) |
| 2 | RoboCop (1987) |
| 3 | Total Recall (1990) |
| 4 | Predator (1987) |
| 5 | Universal Soldier (1992) |

Rekommendationerna är tydligt genrekoherenta – animerade familjefilmer rekommenderas till Toy Story, och actionbetonade sci-fi-filmer rekommenderas till The Matrix. Systemet fungerar snabbt och returnerar svar utan märkbar fördröjning.

---

- Diskussion

### Fördelar

- **Full täckning**: Genre-information finns tillgänglig för samtliga ~79 000 filmer som inte saknar genre, vilket ger bred täckning jämfört med tagg- eller betygsbaserade metoder.
- **Effektivt**: Modellen tränas en gång vid start och ger snabba svar vid körning.
- **Tolkningsbart**: Det är enkelt att förstå *varför* en film rekommenderas - de delar genrer.

### Begränsningar

- **Genre är väldigt brett**: Två filmer kan ha identiska genrekombinationer men skilja sig avsevärt i ton, stil och målgrupp (t.ex. en barnserie och en vuxensatiir kan båda vara *Animation | Comedy*).
- **Inga betyg används**: Systemet kan rekommendera filmer med dåliga betyg om de råkar matcha i genre.
- **Filmer utan genre exkluderas**: De ~7 060 filmerna med `(no genres listed)` kan varken sökas på eller rekommenderas.
- **Taggar ignoreras**: `tags.csv` innehåller information som inte utnyttjas. Även om ~60% av filmerna har minst en tagg är antalet taggar per film lågt och vokabulären brusig, vilket gör dem svåra att använda direkt utan pre-processing.

### Vad kan förbättras?

Att kombinera genre-vektorer med TF-IDF-viktat tagg-innehåll hade kunnat ge ännu bättre rekommendationer, men för detta krävs mycket arbete med pre-processing innan datan kan användas effektivt. 
Även användning av KNN för att sortera baserat på betyg, för att säkerställa att välbedömnda filmer prioriteras. Alltså en hybridmodell där genre,betyg och taggar kombineras för att ge unika rekommendationer. 

Dash-applikationen kan uttökas och ha fler funktioner, men i detta projekt hålls endast till att rekommendera 5 filmer. 