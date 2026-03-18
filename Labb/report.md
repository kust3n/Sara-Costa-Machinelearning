### Rapport - Rekommendationsystem för filmer


- Introduktion / Problemställning
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

- Data-analys (EDA)
// Separat EDA finns som .ipynb med visualiseringar

Datasetet innehåller ett stort antal filmer där varje film är kopplad till en eller flera genrer. En minimal del av filmerna är sorterade i en (no genres listed) "genre", men jämfört med den totala mängden data påverkar inte detta rekommendationssystemet. 
Analysen visade att vissa genrer som exempelvis Drama och Komedi förekommer betydligt oftare än andra.

Rating-datan visade sig vara ojämnt fördelad, majoriteten av filmerna har ganska få betyg jämfört med ett mindre antal filmer som är mycket mer populära och har många betyg. Det innebär att datamängden är gles, vilket kan göra kollaborativa filtreringsmetoder svårare att använda. Detta var en motivation till varför rating-datan inte användes i detta rekommendationssystem.

Eftersom genrer finns tillgängliga för majoriteten av filmerna valdes dessa som huvudfeatures i rekommendationsmodellen.

- Modell



- Resultat

- Diskussion